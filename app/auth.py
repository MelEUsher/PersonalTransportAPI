"""Authentication utilities for securing API write operations."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User

logger = logging.getLogger("app.auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable must be configured.")


def get_password_hash(password: str) -> str:
    """Hash a plaintext password for storage."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validate a plaintext password against a stored hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        return False


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token for the supplied subject identifier."""
    expire_delta = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + expire_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _get_user_by_email(db: Session, email: str) -> User | None:
    """Return a user by email or None."""
    result = db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


def _get_user_by_id(db: Session, user_id: int) -> User | None:
    """Return a user by primary key or None."""
    return db.get(User, user_id)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Return the authenticated user when credentials are valid."""
    user = _get_user_by_email(db, email)
    if user is None:
        logger.warning("Login attempt with unknown email: %s", email)
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning("Invalid password attempt for email: %s", email)
        return None
    return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """Validate request bearer token and return the associated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        logger.warning("Failed token decode: %s", exc)
        raise credentials_exception from exc

    subject = payload.get("sub")
    if subject is None:
        logger.warning("Token missing subject claim.")
        raise credentials_exception

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        logger.warning("Token subject is not a valid user id: %s", subject)
        raise credentials_exception from exc

    user = _get_user_by_id(db, user_id)
    if user is None:
        logger.warning("Token subject not found: %s", user_id)
        raise credentials_exception

    return user


__all__ = [
    "authenticate_user",
    "create_access_token",
    "get_current_user",
    "get_password_hash",
    "verify_password",
]
