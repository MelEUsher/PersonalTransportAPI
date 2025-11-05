"""Shared pytest fixtures for backend tests."""
from __future__ import annotations

import asyncio
import os
import sys
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure authentication layer has required secret during tests.
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

from app.auth import get_current_user
from app.db import Base, get_db
from app.models.user import User
from app.routers import bikes, rentals

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def create_test_database() -> Iterator[None]:
    """Create all tables in an in-memory database for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Iterator[Session]:
    """Provide a transactional database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session_, transaction_) -> None:  # type: ignore[unused-ignore]
        if transaction_.nested and transaction_._parent is not None:
            session_.begin_nested()

    session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Construct a lightweight FastAPI app for integration tests."""
    test_app = FastAPI(title="Test Personal Transport API")
    test_app.include_router(bikes.router)
    test_app.include_router(rentals.router)
    return test_app


@pytest.fixture()
def test_user(db_session: Session) -> User:
    """Create a persisted user record for authenticated requests."""
    user = User(
        name="Test User",
        email=f"tester+{uuid.uuid4().hex}@example.com",
        hashed_password="hashed-password",
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture()
def override_dependencies(app: FastAPI, db_session: Session, test_user: User) -> Iterator[None]:
    """Override global dependencies with test equivalents."""
    def _get_db() -> Iterator[Session]:
        yield db_session

    def _get_current_user() -> User:
        return test_user

    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[get_current_user] = _get_current_user
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture()
def async_client(app: FastAPI, override_dependencies: None) -> Iterator[AsyncClient]:
    """Provide an HTTPX async client bound to the FastAPI test app."""
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://testserver")
    try:
        yield client
    finally:
        asyncio.run(client.aclose())
