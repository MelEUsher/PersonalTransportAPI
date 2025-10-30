"""Router for rental-related API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories import bike_repo, rental_repo
from app.schemas.rental_schema import RentalCreate, RentalRead
from app.services import rental_service

router = APIRouter(prefix="/api/rentals", tags=["rentals"])


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    """Return responses that adhere to the shared error contract."""
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


@router.post("", response_model=RentalRead)
def create_rental(
    payload: RentalCreate, db: Session = Depends(get_db)
) -> RentalRead | JSONResponse:
    """
    Validate a rental request, compute pricing, and persist the rental record.
    """
    try:
        days = rental_service.validate_range(payload.start_date, payload.end_date)
    except ValueError as exc:
        return _error_response(status.HTTP_400_BAD_REQUEST, "INVALID_RANGE", str(exc))

    bike = bike_repo.get_bike_by_id(db, payload.bike_id)
    if bike is None:
        return _error_response(status.HTTP_404_NOT_FOUND, "NOT_FOUND", "Bike not found")

    try:
        if not rental_service.is_bike_available(
            bike, payload.start_date, payload.end_date
        ):
            return _error_response(
                status.HTTP_409_CONFLICT,
                "UNAVAILABLE",
                "Bike is not available for the selected dates.",
            )
    except ValueError as exc:
        return _error_response(status.HTTP_400_BAD_REQUEST, "INVALID_RANGE", str(exc))

    total_price_cents = rental_service.compute_total_price_cents(
        bike.rate_per_day_cents, days
    )

    create_schema = payload.model_copy(update={"total_price_cents": total_price_cents})
    rental = rental_repo.create_rental(db, create_schema)
    return rental


@router.get("/{rental_id}", response_model=RentalRead)
def get_rental(
    rental_id: int, db: Session = Depends(get_db)
) -> RentalRead | JSONResponse:
    """Retrieve a rental record by its identifier."""
    rental = rental_repo.get_rental_by_id(db, rental_id)
    if rental is None:
        return _error_response(
            status.HTTP_404_NOT_FOUND, "NOT_FOUND", "Rental not found"
        )
    return rental
