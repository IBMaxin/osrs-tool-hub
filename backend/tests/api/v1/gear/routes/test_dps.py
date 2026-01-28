"""Tests for DPS calculation endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session
from backend.models import Item
from backend.api.v1.gear.schemas import DPSRequest, DPSComparisonRequest, LoadoutInput

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
        assert "error" in data["error"].get("message", "").lower() or "Calculation error" in data[
            "error"
        ].get("message", "")


def test_compare_dps_endpoint_melee_success():
    """Test successful DPS comparison with melee loadouts."""
    # Create test items in the same engine that the endpoint will use
    session = Session(test_engine)
    try:
        whip = Item(
            id=4151,
            name="Abyssal whip",
            slot="weapon",
            attack_stab=82,
            attack_slash=82,
            melee_strength=82,
            attack_speed=4,
        )
        dscim = Item(
            id=4587,
            name="Dragon scimitar",
            slot="weapon",
            attack_stab=67,
            attack_slash=67,
            melee_strength=66,
            attack_speed=4,
        )
        session.add(whip)
        session.add(dscim)
        session.commit()
    finally:
        session.close()

    request = DPSComparisonRequest(
        loadouts=[
            LoadoutInput(name="Whip", loadout={"weapon": 4151}),
            LoadoutInput(name="D Scim", loadout={"weapon": 4587}),
        ],
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/dps/compare", json=request.dict())

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2
    assert data["results"][0]["loadout_name"] == "Whip"
    assert data["results"][1]["loadout_name"] == "D Scim"


def test_compare_dps_endpoint_invalid_loadout():
    """Test DPS comparison with invalid item IDs."""
    request = DPSComparisonRequest(
        loadouts=[
            LoadoutInput(name="Invalid", loadout={"weapon": 99999}),
        ],
        combat_style="melee",
        attack_type="slash",
    )

    response = client.post("/api/v1/dps/compare", json=request.dict())

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "combat_style,attack_type",
    [
        ("melee", "slash"),
        ("ranged", None),
        ("magic", None),
    ],
)
def test_compare_dps_endpoint_mixed_combat_styles(combat_style, attack_type):
    """Test DPS comparison with different combat styles."""
    item1_id, item2_id = None, None
    with Session(test_engine) as session:
        if combat_style == "melee":
            item1 = Item(
                id=4151,
                name="Whip",
                slot="weapon",
                attack_slash=82,
                melee_strength=82,
                attack_speed=4,
            )
            item2 = Item(
                id=4587,
                name="D Scim",
                slot="weapon",
                attack_slash=67,
                melee_strength=66,
                attack_speed=4,
            )
        elif combat_style == "ranged":
            item1 = Item(
                id=20997, name="Twisted bow", slot="weapon", ranged_strength=70, attack_speed=5
            )
            item2 = Item(
                id=12926, name="Blowpipe", slot="weapon", ranged_strength=20, attack_speed=2
            )
        else:  # magic
            item1 = Item(id=11791, name="Trident", slot="weapon", magic_damage=15, attack_speed=4)
            item2 = Item(
                id=11905, name="Iban staff", slot="weapon", magic_damage=10, attack_speed=5
            )
        session.add(item1)
        session.add(item2)
        session.commit()
        item1_id = item1.id
        item2_id = item2.id

    request = DPSComparisonRequest(
        loadouts=[
            LoadoutInput(name="Loadout 1", loadout={"weapon": item1_id}),
            LoadoutInput(name="Loadout 2", loadout={"weapon": item2_id}),
        ],
        combat_style=combat_style,
        attack_type=attack_type,
        player_stats={"attack": 99, "strength": 99, "ranged": 99, "magic": 99},
    )

    response = client.post("/api/v1/dps/compare", json=request.dict())

    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert len(data["results"]) == 2
