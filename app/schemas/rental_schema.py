"""Pydantic schemas for rental data transfer."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class RentalCreate(BaseModel):
    """Schema for creating a rental."""

    bike_id: int
    user_id: int
    start_date: date
    end_date: date | None = None
    total_price_cents: int


class RentalRead(BaseModel):
    """Schema for reading rental data."""

    id: int
    bike_id: int
    user_id: int
    start_date: date
    end_date: date | None
    total_price_cents: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


__all__ = ["RentalCreate", "RentalRead"]
