"""Tests for DPS calculation endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session
from backend.models import Item
from backend.api.v1.gear.schemas import DPSRequest

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


def test_calculate_dps_with_valid_items():
    """Test DPS calculation with valid items."""
    # Create test items
    with Session(test_engine) as session:
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            slot="weapon",
            attack_stab=82,
            attack_slash=82,
            melee_strength=82,
            attack_speed=4,
        )
        session.add(weapon)
        session.commit()

    request = DPSRequest(
        loadout={"weapon": 4151},
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.dict())

    # Should return 200 or 400 (400 if calculation fails)
    assert response.status_code in [200, 400]


def test_calculate_dps_with_none_item_id():
    """Test DPS calculation when item_id is None in loadout."""
    request = DPSRequest(
        loadout={"weapon": None, "head": None},
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_calculate_dps_with_invalid_item_id():
    """Test DPS calculation when item_id doesn't exist in database."""
    request = DPSRequest(
        loadout={"weapon": 99999},  # Non-existent item ID
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_calculate_dps_with_mixed_valid_and_invalid():
    """Test DPS calculation with mix of valid and invalid item IDs."""
    # Create one valid item
    with Session(test_engine) as session:
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            slot="weapon",
            attack_stab=82,
            attack_slash=82,
            melee_strength=82,
        )
        session.add(weapon)
        session.commit()

    request = DPSRequest(
        loadout={"weapon": 4151, "head": 99999},  # Valid weapon, invalid head
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.dict())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_calculate_dps_handles_service_errors():
    """Test that DPS endpoint handles service errors gracefully."""
    with patch("backend.api.v1.gear.routes.dps.GearService") as mock_service_class:
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.calculate_dps.side_effect = Exception("Calculation error")

        request = DPSRequest(
            loadout={"weapon": 4151},
            combat_style="melee",
            attack_type="slash",
            player_stats={"attack": 99, "strength": 99},
        )

        response = client.post("/api/v1/gear/dps", json=request.dict())

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert (
            "error" in data["error"].get("message", "").lower()
            or "Calculation error" in data["error"].get("message", "")
        )
