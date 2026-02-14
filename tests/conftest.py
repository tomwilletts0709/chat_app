"""Pytest fixtures for chat app tests."""
import os
# Set test DB before any chat_app imports
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chat_app.db import Base, get_db
from chat_app.main import app
from chat_app.auth import get_current_user
from chat_app.models import User
from fastapi.testclient import TestClient


def _mock_get_current_user():
    """Return a fake user for testing protected routes."""
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed",
    )


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(test_engine):
    """Create a test client with overridden DB and auth dependencies."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = _mock_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
