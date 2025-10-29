"""Database configuration and session management utilities."""
from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Load environment variables early so DATABASE_URL is available.
load_dotenv()


class Base(DeclarativeBase):
    """Declarative base class for SQLAlchemy models."""


def _sqlite_connect_args(database_url: str) -> dict[str, bool]:
    """Return SQLite-specific engine arguments when applicable."""
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=_sqlite_connect_args(DATABASE_URL),
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session scoped to the request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
