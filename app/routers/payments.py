"""Router for payment processing endpoints secured by authentication."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, PositiveInt
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["payments"])

_oauth2_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
_AUTH_REQUIRED_DETAIL = "Authentication required for payment processing"


class PaymentRequest(BaseModel):
    """Payload accepted by the stubbed payment processor."""

    rental_id: PositiveInt
    amount_cents: PositiveInt


class PaymentResponse(BaseModel):
    """Stub response returned after a successful payment."""

    status: str = "success"
    transaction_id: str
    detail: str = "Payment processed successfully (stub)."


def _require_authenticated_user(
    token: Annotated[str | None, Depends(_oauth2_optional)],
    db: Session = Depends(get_db),
) -> User:
    """Return the authenticated user or raise 403 when unavailable."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=_AUTH_REQUIRED_DETAIL
        )

    try:
        return get_current_user(token=token, db=db)
    except HTTPException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=_AUTH_REQUIRED_DETAIL
        ) from exc


@router.post("", response_model=PaymentResponse)
def process_payment(
    payload: PaymentRequest,
    current_user: User = Depends(_require_authenticated_user),
) -> PaymentResponse:
    """Simulate payment processing for authenticated users only."""
    transaction_id = f"stub-{uuid.uuid4().hex[:12]}"
    detail = (
        "Payment processed successfully (stub) "
        f"for rental {payload.rental_id} by user {current_user.id}."
    )
    return PaymentResponse(transaction_id=transaction_id, detail=detail)
