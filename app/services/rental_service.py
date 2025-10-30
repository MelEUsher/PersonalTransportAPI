"""Business logic for validating rentals and computing pricing."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any


_MAX_RENTAL_DAYS = 3


def _normalize_date(value: Any, field_name: str) -> date:
    """Convert supported date/datetime inputs to a date instance."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    raise ValueError(f"{field_name} must be a date or datetime instance")


def validate_range(start_date: Any, end_date: Any) -> int:
    """Validate that the rental falls within the allowed 1–3 day window."""
    start = _normalize_date(start_date, "start_date")
    end = _normalize_date(end_date, "end_date")

    days = (end - start).days
    if days <= 0:
        raise ValueError("end_date must be after start_date")
    if days > _MAX_RENTAL_DAYS:
        raise ValueError("Rental duration must be between 1 and 3 days")

    return days


def compute_total_price_cents(rate_per_day_cents: int, days: int) -> int:
    """Calculate total price using a per-day rate and validated day count."""
    if not isinstance(rate_per_day_cents, int):
        raise ValueError("rate_per_day_cents must be an integer")
    if rate_per_day_cents < 0:
        raise ValueError("rate_per_day_cents must be zero or greater")

    if not isinstance(days, int):
        raise ValueError("days must be an integer")
    if days <= 0:
        raise ValueError("days must be greater than zero")
    if days > _MAX_RENTAL_DAYS:
        raise ValueError("days must not exceed 3")

    return rate_per_day_cents * days


def is_bike_available(bike: Any, start_date: Any, end_date: Any) -> bool:
    """Return True when bike status is 'available' and rental dates are valid."""
    validate_range(start_date, end_date)

    status: Any
    if hasattr(bike, "status"):
        status = getattr(bike, "status")
    elif isinstance(bike, dict) and "status" in bike:
        status = bike["status"]
    else:
        raise ValueError("bike must expose a 'status' attribute or key")

    return str(status).lower() == "available"
