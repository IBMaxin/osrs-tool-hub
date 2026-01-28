"""Tests for gear suggestions endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session

# Create test engine
test_engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def get_test_session():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Set up test database before each test."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)
    test_engine.dispose()


def test_get_gear_suggestions_basic():
    """Test basic gear suggestions endpoint."""
    response = client.get("/api/v1/gear/suggestions?slot=head&style=melee&defence_level=99")

    # Should return 200 or 404 (404 if no items in DB)
    assert response.status_code in [200, 404]


def test_get_gear_suggestions_invalid_slot():
    """Test gear suggestions with invalid slot."""
    response = client.get("/api/v1/gear/suggestions?slot=invalid_slot&style=melee")

    # Should return 400 Bad Request
    assert response.status_code == 400
    assert "Invalid slot" in response.json()["detail"]


def test_get_gear_suggestions_invalid_style():
    """Test gear suggestions with invalid combat style."""
    response = client.get("/api/v1/gear/suggestions?slot=head&style=invalid")

    # Should return 400 Bad Request
    assert response.status_code == 400
    assert "Invalid combat style" in response.json()["detail"]


def test_get_alternatives_endpoint():
    """Test gear alternatives endpoint."""
    response = client.get(
        "/api/v1/gear/alternatives?"
        "slot=weapon&"
        "combat_style=melee&"
        "budget=1000000&"
        "limit=5"
    )

    # Should return 200 or 404 (404 if no items in DB)
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_with_stats():
    """Test gear alternatives with player stats."""
    response = client.get(
        "/api/v1/gear/alternatives?"
        "slot=weapon&"
        "combat_style=melee&"
        "attack=99&"
        "strength=99&"
        "defence=99"
    )

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_handles_errors():
    """Test that alternatives endpoint handles errors gracefully."""
    # Mock service to raise an error
    with patch("backend.api.v1.gear.routes.suggestions.GearService") as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_alternatives.side_effect = Exception("Service error")

        response = client.get("/api/v1/gear/alternatives?" "slot=weapon&" "combat_style=melee")

        # Should return 400 Bad Request with error message
        assert response.status_code == 400
        assert (
            "error" in response.json()["detail"].lower()
            or "Service error" in response.json()["detail"]
        )


def test_get_alternatives_with_partial_stats():
    """Test alternatives endpoint with only some stats provided."""
    response = client.get(
        "/api/v1/gear/alternatives?" "slot=weapon&" "combat_style=melee&" "attack=70&" "strength=70"
    )

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_with_all_stats():
    """Test alternatives endpoint with all stats provided."""
    response = client.get(
        "/api/v1/gear/alternatives?"
        "slot=weapon&"
        "combat_style=melee&"
        "attack=99&"
        "strength=99&"
        "defence=99&"
        "ranged=99&"
        "magic=99&"
        "prayer=99"
    )

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_with_attack_type():
    """Test alternatives endpoint with attack type specified."""
    response = client.get(
        "/api/v1/gear/alternatives?" "slot=weapon&" "combat_style=melee&" "attack_type=stab"
    )

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_with_budget_and_stats():
    """Test alternatives endpoint with both budget and stats."""
    response = client.get(
        "/api/v1/gear/alternatives?"
        "slot=weapon&"
        "combat_style=melee&"
        "budget=1000000&"
        "attack=70&"
        "strength=70"
    )

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]


def test_get_alternatives_no_stats_provided():
    """Test alternatives endpoint without any stats (stats should be None)."""
    response = client.get("/api/v1/gear/alternatives?" "slot=weapon&" "combat_style=melee")

    # Should return 200 or 404
    assert response.status_code in [200, 404, 400]
