"""Application entrypoint for the Personal Transport API FastAPI backend."""
from __future__ import annotations

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.rate_limiter import limiter
from app.routers import auth as auth_router
from app.routers import bikes, payments, rentals

# Configure logging early so security events are captured.
logging.basicConfig(level=logging.INFO)

# Load environment variables from a .env file if present.
load_dotenv()

app = FastAPI(title="Personal Transport API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://thefreerangedev.com",
        "http://localhost:5173",
    ],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router.router)
app.include_router(bikes.router)
app.include_router(payments.router)
app.include_router(rentals.router)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Simple health check endpoint used by monitoring and smoke tests."""
    return {"status": "ok"}
