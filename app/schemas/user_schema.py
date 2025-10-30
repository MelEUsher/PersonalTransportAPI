"""Pydantic schemas for user data transfer."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """Schema for creating a user."""

    name: str
    email: str
    phone: str | None = None


class UserRead(BaseModel):
    """Schema for reading user data."""

    id: int
    name: str
    email: str
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


__all__ = ["UserCreate", "UserRead"]
