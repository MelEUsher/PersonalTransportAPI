from __future__ import annotations

import asyncio

from sqlalchemy.orm import Session

from app.models.bike import AvailabilityStatus, Bike


def test_list_available_bikes_returns_only_available(
    async_client, db_session: Session
) -> None:
    available_bike = Bike(
        name="City Cruiser",
        type="city",
        rate_per_day_cents=1500,
        availability_status=AvailabilityStatus.AVAILABLE,
    )
    unavailable_bike = Bike(
        name="Mountain Master",
        type="mountain",
        rate_per_day_cents=2000,
        availability_status=AvailabilityStatus.UNAVAILABLE,
    )
    db_session.add_all([available_bike, unavailable_bike])
    db_session.flush()

    response = asyncio.run(async_client.get("/api/bikes"))

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {
            "id": available_bike.id,
            "name": "City Cruiser",
            "type": "city",
            "rate_per_day_cents": 1500,
            "availability_status": AvailabilityStatus.AVAILABLE.value,
        }
    ]
