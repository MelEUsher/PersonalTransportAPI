"""Pydantic schemas for bike data transfer."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.models.bike import AvailabilityStatus


class BikeCreate(BaseModel):
    """Schema for creating a bike."""

    name: str
    type: str
    rate_per_day_cents: int
    availability_status: AvailabilityStatus


class BikeRead(BaseModel):
    """Schema for reading bike data."""

    id: int
    name: str
    type: str
    rate_per_day_cents: int
    availability_status: AvailabilityStatus

    model_config = ConfigDict(from_attributes=True)


__all__ = ["BikeCreate", "BikeRead"]
