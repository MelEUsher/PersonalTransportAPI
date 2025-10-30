"""Repository helpers for user persistence operations."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate


def create_user(db: Session, schema: UserCreate) -> User:
    """Persist a new user based on the provided schema."""
    user = User(**schema.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Return a user by their primary key."""
    return db.get(User, user_id)


def get_all_users(db: Session) -> list[User]:
    """Return all users."""
    result = db.execute(select(User))
    return result.scalars().all()


__all__ = ["create_user", "get_user_by_id", "get_all_users"]
