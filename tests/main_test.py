"""Tests for main API endpoints."""
from fastapi.testclient import TestClient

from chat_app.main import app


def test_read_root():
    """Root endpoint returns hello world."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"hello": "world"}


def test_list_chats_empty(client):
    """List chats returns empty list when no chats exist."""
    response = client.get("/chats")
    assert response.status_code == 200
    assert response.json() == []
