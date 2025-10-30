"""Repository helpers for rental persistence operations."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.rental import Rental
from app.schemas.rental_schema import RentalCreate


def create_rental(db: Session, schema: RentalCreate) -> Rental:
    """Persist a new rental based on the provided schema."""
    rental = Rental(**schema.model_dump())
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental


def get_rental_by_id(db: Session, rental_id: int) -> Rental | None:
    """Return a rental by its primary key."""
    return db.get(Rental, rental_id)


def get_all_rentals(db: Session) -> list[Rental]:
    """Return all rentals."""
    result = db.execute(select(Rental))
    return result.scalars().all()


__all__ = ["create_rental", "get_rental_by_id", "get_all_rentals"]
