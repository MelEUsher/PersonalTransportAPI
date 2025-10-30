from datetime import date, datetime, timedelta
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.rental_service import (
    compute_total_price_cents,
    is_bike_available,
    validate_range,
)


class BikeStub:
    def __init__(self, status: str) -> None:
        self.status = status


def test_validate_range_returns_days_for_valid_window():
    start = date(2024, 6, 1)
    end = date(2024, 6, 3)

    result = validate_range(start, end)

    assert result == 2


@pytest.mark.parametrize(
    "start_offset,end_offset,expected_days",
    [
        (0, 1, 1),
        (0, 3, 3),
    ],
)
def test_validate_range_accepts_datetime(start_offset, end_offset, expected_days):
    start = datetime(2024, 6, 1) + timedelta(days=start_offset)
    end = datetime(2024, 6, 1) + timedelta(days=end_offset)

    result = validate_range(start, end)

    assert result == expected_days


@pytest.mark.parametrize(
    "start_offset,end_offset,message",
    [
        (0, 0, "end_date must be after start_date"),
        (1, 0, "end_date must be after start_date"),
        (0, 4, "Rental duration must be between 1 and 3 days"),
    ],
)
def test_validate_range_raises_for_invalid_windows(start_offset, end_offset, message):
    start = date(2024, 6, 1) + timedelta(days=start_offset)
    end = date(2024, 6, 1) + timedelta(days=end_offset)

    with pytest.raises(ValueError, match=message):
        validate_range(start, end)


def test_compute_total_price_cents_multiplies_rate_and_days():
    total = compute_total_price_cents(1500, 3)

    assert total == 4500


@pytest.mark.parametrize(
    "rate,days,message",
    [
        ("1500", 2, "rate_per_day_cents must be an integer"),
        (-10, 2, "rate_per_day_cents must be zero or greater"),
        (1500, 0, "days must be greater than zero"),
        (1500, 4, "days must not exceed 3"),
    ],
)
def test_compute_total_price_cents_validates_inputs(rate, days, message):
    with pytest.raises(ValueError, match=message):
        compute_total_price_cents(rate, days)


def test_is_bike_available_returns_true_for_available_bike():
    bike = BikeStub("available")

    available = is_bike_available(bike, date(2024, 6, 1), date(2024, 6, 2))

    assert available is True


def test_is_bike_available_handles_dicts():
    bike = {"status": "UNAVAILABLE"}

    available = is_bike_available(bike, date(2024, 6, 1), date(2024, 6, 2))

    assert available is False


def test_is_bike_available_raises_when_status_missing():
    bike = object()

    with pytest.raises(ValueError, match="status"):
        is_bike_available(bike, date(2024, 6, 1), date(2024, 6, 2))


def test_is_bike_available_reuses_validate_range():
    bike = BikeStub("available")

    with pytest.raises(ValueError, match="Rental duration"):
        is_bike_available(bike, date(2024, 6, 1), date(2024, 6, 5))
