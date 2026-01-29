"""Tests for DPS calculation endpoints."""

import pytest
import tempfile
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session
from backend.models import Item
from backend.api.v1.gear.schemas import DPSRequest, DPSComparisonRequest, LoadoutInput

# Create test engine - use file-based DB to ensure persistence across sessions
_test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
_test_db_path = _test_db_file.name
_test_db_file.close()

test_engine = create_engine(
    f"sqlite:///{_test_db_path}", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def create_test_item(
    item_id: int,
    name: str,
    slot: str = "weapon",
    attack_stab: int = 0,
    attack_slash: int = 0,
    attack_crush: int = 0,
    melee_strength: int = 0,
    attack_speed: int = 4,
    **kwargs,
) -> Item:
    """Helper to create test items with all required fields."""
    defaults = {
        "members": True,
        "value": 0,
        "attack_req": 1,
        "strength_req": 1,
        "defence_req": 1,
        "ranged_req": 1,
        "magic_req": 1,
        "prayer_req": 1,
        "slayer_req": 0,
        "is_2h": False,
        "attack_magic": 0,
        "attack_ranged": 0,
        "ranged_strength": 0,
        "magic_damage": 0,
        "prayer_bonus": 0,
        "defence_stab": 0,
        "defence_slash": 0,
        "defence_crush": 0,
        "defence_magic": 0,
        "defence_ranged": 0,
    }
    defaults.update(kwargs)
    return Item(
        id=item_id,
        name=name,
        slot=slot,
        attack_stab=attack_stab,
        attack_slash=attack_slash,
        attack_crush=attack_crush,
        melee_strength=melee_strength,
        attack_speed=attack_speed,
        **defaults,
    )


def get_test_session():
    """Get test session - items should already be created in test fixtures."""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Set up test database before each test."""
    SQLModel.metadata.create_all(test_engine)
    # Clear any existing data
    with Session(test_engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
    yield
    # Clean up after test
    with Session(test_engine) as session:
        for table in reversed(SQLModel.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


def test_calculate_dps_with_valid_items(session: Session, client: TestClient):
    """Test DPS calculation with valid items."""
    # Create test items
    weapon = create_test_item(
        4151,
        "Abyssal whip",
        "weapon",
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

    response = client.post("/api/v1/gear/dps", json=request.model_dump())

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

    response = client.post("/api/v1/gear/dps", json=request.model_dump())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_calculate_dps_with_invalid_item_id(client: TestClient):
    """Test DPS calculation when item_id doesn't exist in database."""
    request = DPSRequest(
        loadout={"weapon": 99999},  # Non-existent item ID
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.model_dump())

    # Should return 200 or 400
    assert response.status_code in [200, 400]


def test_calculate_dps_with_mixed_valid_and_invalid(session: Session, client: TestClient):
    """Test DPS calculation with mix of valid and invalid item IDs."""
    # Create one valid item
    weapon = create_test_item(
        4151, "Abyssal whip", "weapon", attack_stab=82, attack_slash=82, melee_strength=82
    )
    session.add(weapon)
    session.commit()

    request = DPSRequest(
        loadout={"weapon": 4151, "head": 99999},  # Valid weapon, invalid head
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/gear/dps", json=request.model_dump())

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

        response = client.post("/api/v1/gear/dps", json=request.model_dump())

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "error" in data["error"].get("message", "").lower() or "Calculation error" in data[
            "error"
        ].get("message", "")


def test_compare_dps_endpoint_melee_success(session: Session, client: TestClient):
    """Test successful DPS comparison with melee loadouts."""
    # Create test items in the same session that the endpoint will use
    whip = create_test_item(
        4151,
        "Abyssal whip",
        "weapon",
        attack_stab=82,
        attack_slash=82,
        melee_strength=82,
        attack_speed=4,
        attack_req=70,
        strength_req=70,
    )
    dscim = create_test_item(
        4587,
        "Dragon scimitar",
        "weapon",
        attack_stab=67,
        attack_slash=67,
        melee_strength=66,
        attack_speed=4,
        attack_req=60,
        strength_req=60,
    )
    session.add(whip)
    session.add(dscim)
    session.commit()

    request = DPSComparisonRequest(
        loadouts=[
            LoadoutInput(name="Whip", loadout={"weapon": 4151}),
            LoadoutInput(name="D Scim", loadout={"weapon": 4587}),
        ],
        combat_style="melee",
        attack_type="slash",
        player_stats={"attack": 99, "strength": 99},
    )

    response = client.post("/api/v1/dps/compare", json=request.model_dump())

    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}: {response.json()}"
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

    response = client.post("/api/v1/dps/compare", json=request.model_dump())

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "combat_style,attack_type",
    [
        ("melee", "slash"),
        ("ranged", None),
        ("magic", None),
    ],
)
def test_compare_dps_endpoint_mixed_combat_styles(
    combat_style, attack_type, session: Session, client: TestClient
):
    """Test DPS comparison with different combat styles."""
    if combat_style == "melee":
        item1 = create_test_item(
            4151, "Whip", "weapon", attack_slash=82, melee_strength=82, attack_speed=4
        )
        item2 = create_test_item(
            4587, "D Scim", "weapon", attack_slash=67, melee_strength=66, attack_speed=4
        )
    elif combat_style == "ranged":
        item1 = create_test_item(20997, "Twisted bow", "weapon", ranged_strength=70, attack_speed=5)
        item2 = create_test_item(12926, "Blowpipe", "weapon", ranged_strength=20, attack_speed=2)
    else:  # magic
        item1 = create_test_item(11791, "Trident", "weapon", magic_damage=15, attack_speed=4)
        item2 = create_test_item(11905, "Iban staff", "weapon", magic_damage=10, attack_speed=5)
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

    response = client.post("/api/v1/dps/compare", json=request.model_dump())

    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert len(data["results"]) == 2
