"""Rental model definitions."""
from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db import Base

if TYPE_CHECKING:
    from .bike import Bike
    from .user import User


class Rental(Base):
    """Rental record connecting users and bikes."""

    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey("bikes.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    bike: Mapped["Bike"] = relationship("Bike", back_populates="rentals")
    user: Mapped["User"] = relationship("User", back_populates="rentals")
