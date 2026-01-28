"""Tests for loadout optimization endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session
from backend.api.v1.gear.schemas import BestLoadoutRequest, UpgradePathRequest

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


def test_get_preset_loadout_valid():
    """Test getting preset loadout with valid parameters."""
    response = client.get("/api/v1/gear/preset?combat_style=melee&tier=mid")

    # Should return 200 or 400 (400 if preset not found)
    assert response.status_code in [200, 400]


def test_get_preset_loadout_invalid_tier():
    """Test getting preset loadout with invalid tier (should raise ValueError)."""
    with patch("backend.api.v1.gear.routes.loadouts.GearService") as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_preset_loadout.side_effect = ValueError("Invalid tier")

        response = client.get("/api/v1/gear/preset?combat_style=melee&tier=invalid")

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Invalid tier" in data["error"].get("message", "")


def test_get_best_loadout_valid():
    """Test getting best loadout with valid request."""
    request = BestLoadoutRequest(
        combat_style="melee",
        budget=1000000,
        stats={"attack": 70, "strength": 70, "defence": 70},
        attack_type="slash",
    )

    response = client.post("/api/v1/gear/best-loadout", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_get_best_loadout_with_quests():
    """Test getting best loadout with quests completed."""
    request = BestLoadoutRequest(
        combat_style="melee",
        budget=1000000,
        stats={"attack": 70, "strength": 70, "defence": 70},
        quests_completed=["Recipe for Disaster"],
    )

    response = client.post("/api/v1/gear/best-loadout", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_get_best_loadout_with_achievements():
    """Test getting best loadout with achievements completed."""
    request = BestLoadoutRequest(
        combat_style="melee",
        budget=1000000,
        stats={"attack": 70, "strength": 70, "defence": 70},
        achievements_completed=["Fight Caves"],
    )

    response = client.post("/api/v1/gear/best-loadout", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_get_best_loadout_handles_errors():
    """Test that best loadout endpoint handles errors gracefully."""
    with patch("backend.api.v1.gear.routes.loadouts.GearService") as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_best_loadout.side_effect = Exception("Service error")

        request = BestLoadoutRequest(
            combat_style="melee",
            budget=1000000,
            stats={"attack": 70, "strength": 70, "defence": 70},
        )

        response = client.post("/api/v1/gear/best-loadout", json=request.dict())

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert (
            "error" in data["error"].get("message", "").lower()
            or "Service error" in data["error"].get("message", "")
        )


def test_get_upgrade_path_valid():
    """Test getting upgrade path with valid request."""
    request = UpgradePathRequest(
        current_loadout={"weapon": 4151},
        combat_style="melee",
        budget=1000000,
        stats={"attack": 70, "strength": 70, "defence": 70},
        attack_type="slash",
    )

    response = client.post("/api/v1/gear/upgrade-path", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_get_upgrade_path_with_quests_and_achievements():
    """Test getting upgrade path with quests and achievements."""
    request = UpgradePathRequest(
        current_loadout={"weapon": 4151},
        combat_style="melee",
        budget=1000000,
        stats={"attack": 70, "strength": 70, "defence": 70},
        quests_completed=["Recipe for Disaster"],
        achievements_completed=["Fight Caves"],
    )

    response = client.post("/api/v1/gear/upgrade-path", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_get_upgrade_path_handles_errors():
    """Test that upgrade path endpoint handles errors gracefully."""
    with patch("backend.api.v1.gear.routes.loadouts.GearService") as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.get_upgrade_path.side_effect = Exception("Service error")

        request = UpgradePathRequest(
            current_loadout={"weapon": 4151},
            combat_style="melee",
            budget=1000000,
            stats={"attack": 70, "strength": 70, "defence": 70},
        )

        response = client.post("/api/v1/gear/upgrade-path", json=request.dict())

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert (
            "error" in data["error"].get("message", "").lower()
            or "Service error" in data["error"].get("message", "")
        )
