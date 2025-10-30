"""Repository helpers for bike persistence operations."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bike import AvailabilityStatus, Bike
from app.schemas.bike_schema import BikeCreate


def create_bike(db: Session, schema: BikeCreate) -> Bike:
    """Persist a new bike based on the provided schema."""
    bike = Bike(**schema.model_dump())
    db.add(bike)
    db.commit()
    db.refresh(bike)
    return bike


def get_bike_by_id(db: Session, bike_id: int) -> Bike | None:
    """Return a bike by its primary key."""
    return db.get(Bike, bike_id)


def get_all_bikes(db: Session) -> list[Bike]:
    """Return all bikes."""
    result = db.execute(select(Bike))
    return result.scalars().all()


def get_available_bikes(db: Session) -> list[Bike]:
    """Return only bikes that are currently available for rental."""
    result = db.execute(
        select(Bike).where(Bike.availability_status == AvailabilityStatus.AVAILABLE)
    )
    return result.scalars().all()


__all__ = ["create_bike", "get_bike_by_id", "get_all_bikes", "get_available_bikes"]
