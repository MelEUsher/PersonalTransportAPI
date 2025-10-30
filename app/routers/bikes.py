"""Router for bike-related API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.bike_repo import get_available_bikes
from app.schemas.bike_schema import BikeRead

router = APIRouter(prefix="/api/bikes", tags=["bikes"])


@router.get("", response_model=list[BikeRead])
def list_available_bikes(db: Session = Depends(get_db)) -> list[BikeRead]:
    """Return all bikes currently available for rental."""
    return get_available_bikes(db)

