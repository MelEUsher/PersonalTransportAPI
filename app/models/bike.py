"""Bike model definitions."""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .rental import Rental


class AvailabilityStatus(str, Enum):
    """Enumerated values for bike availability."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class Bike(Base):
    """Bike available for rental."""

    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    rate_per_day_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    availability_status: Mapped[AvailabilityStatus] = mapped_column(
        SqlEnum(
            AvailabilityStatus,
            name="availability_status",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
    )

    rentals: Mapped[list["Rental"]] = relationship("Rental", back_populates="bike")
