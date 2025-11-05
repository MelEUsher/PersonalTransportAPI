from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy.orm import Session

from app.models.bike import AvailabilityStatus, Bike
from app.models.rental import Rental
from app.models.user import User


def _create_bike(db_session: Session) -> Bike:
    bike = Bike(
        name="Road Runner",
        type="road",
        rate_per_day_cents=2500,
        availability_status=AvailabilityStatus.AVAILABLE,
    )
    db_session.add(bike)
    db_session.flush()
    # rental_service expects a 'status' attribute; mirror production data eagerly.
    bike.status = bike.availability_status.value  # type: ignore[attr-defined]
    return bike


def test_create_rental_returns_created_record(
    async_client, db_session: Session, test_user: User
) -> None:
    bike = _create_bike(db_session)
    payload = {
        "bike_id": bike.id,
        "user_id": test_user.id,
        "start_date": date(2024, 7, 1).isoformat(),
        "end_date": date(2024, 7, 3).isoformat(),
        "total_price_cents": 0,
    }

    response = asyncio.run(async_client.post("/api/rentals", json=payload))

    assert response.status_code == 200, response.json()
    body = response.json()
    assert body["bike_id"] == bike.id
    assert body["user_id"] == test_user.id
    assert body["total_price_cents"] == bike.rate_per_day_cents * 2


def test_get_rental_returns_existing_record(
    async_client, db_session: Session, test_user: User
) -> None:
    bike = _create_bike(db_session)
    rental = Rental(
        bike_id=bike.id,
        user_id=test_user.id,
        start_date=date(2024, 7, 5),
        end_date=date(2024, 7, 6),
        total_price_cents=2500,
    )
    db_session.add(rental)
    db_session.flush()

    response = asyncio.run(async_client.get(f"/api/rentals/{rental.id}"))

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == rental.id
    assert body["bike_id"] == bike.id
    assert body["user_id"] == test_user.id
