"""Authentication routes for user registration and login."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import auth as auth_utils
from app.db import get_db
from app.models.user import User
from app.rate_limiter import limiter

logger = logging.getLogger("app.auth")

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    """Payload for registering a new account."""

    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=50)


class RegisterResponse(BaseModel):
    """Response returned after a successful registration."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class LoginRequest(BaseModel):
    """Payload for authenticating an existing account."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    """Response containing issued JWT credentials."""

    access_token: str
    token_type: str = "bearer"


def _user_exists(db: Session, email: str) -> bool:
    """Return True when a user already exists with the supplied email."""
    result = db.execute(select(User.id).where(User.email == email))
    return result.scalar_one_or_none() is not None


@router.post("/register", response_model=RegisterResponse)
@limiter.limit("5/minute")
def register_account(
    payload: RegisterRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    """Create a new user account with hashed password storage."""
    if _user_exists(db, payload.email):
        logger.warning("Registration attempt for existing email: %s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists.",
        )

    hashed_password = auth_utils.get_password_hash(payload.password)
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed_password,
        phone=payload.phone,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("Registered new user: %s", user.email)
    return RegisterResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate credentials and issue a bearer token."""
    user = auth_utils.authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_utils.create_access_token(subject=str(user.id))
    logger.info("Successfully authenticated user: %s", user.email)
    return TokenResponse(access_token=token)
