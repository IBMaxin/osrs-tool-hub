"""Integration tests for slayer location API endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.db.session import get_session
from backend.models import Monster, SlayerTask, SlayerMaster


# Test engine for integration tests
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


def get_test_session():
    """Override get_session dependency for testing."""
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up test database before each test."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def sample_task():
    """Create sample task data for integration tests."""
    with Session(test_engine) as session:
        # Create monster
        monster = Monster(
            id=1,
            name="Abyssal demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150,
            defence_level=60,
            magic_level=1,
            ranged_level=1,
            defence_stab=20,
            defence_slash=20,
            defence_crush=20,
            defence_magic=20,
            defence_ranged=20,
            is_slayer_monster=True
        )
        session.add(monster)
        session.commit()
        
        # Create task
        task = SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=monster.id,
            category="Abyssal demons",
            quantity_min=120,
            quantity_max=185,
            weight=12,
            is_skippable=True,
            is_blockable=True
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return task.id


def test_get_task_location_success(sample_task):
    """Test successful GET request to location endpoint."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verify response structure
    assert "task_id" in data
    assert "monster_name" in data
    assert "category" in data
    assert "master" in data
    assert "locations" in data
    assert "alternatives" in data
    assert "strategy" in data
    assert "weakness" in data
    assert "items_needed" in data
    assert "attack_style" in data
    assert "has_detailed_data" in data
    
    # Verify data types
    assert isinstance(data["task_id"], int)
    assert isinstance(data["monster_name"], str)
    assert isinstance(data["locations"], list)
    assert isinstance(data["alternatives"], list)
    assert isinstance(data["strategy"], str)
    assert isinstance(data["weakness"], list)
    assert isinstance(data["items_needed"], list)
    assert isinstance(data["has_detailed_data"], bool)
    
    # Verify specific data
    assert data["task_id"] == sample_task
    assert data["monster_name"] == "Abyssal demon"
    assert data["category"] == "Abyssal demons"
    assert data["master"] == "duradel"


def test_get_task_location_with_locations(sample_task):
    """Test that locations array is properly structured."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    locations = data["locations"]
    
    # Should have at least one location
    assert len(locations) > 0
    
    # Verify location structure
    first_location = locations[0]
    assert "name" in first_location
    assert "requirements" in first_location
    assert "multi_combat" in first_location
    assert "cannon" in first_location
    assert "safespot" in first_location
    assert "notes" in first_location
    assert "pros" in first_location
    assert "cons" in first_location
    assert "best_for" in first_location
    
    # Verify data types in location
    assert isinstance(first_location["name"], str)
    assert isinstance(first_location["requirements"], list)
    assert isinstance(first_location["multi_combat"], bool)
    assert isinstance(first_location["cannon"], bool)
    assert isinstance(first_location["safespot"], bool)
    assert isinstance(first_location["notes"], str)
    assert isinstance(first_location["pros"], list)
    assert isinstance(first_location["cons"], list)
    assert isinstance(first_location["best_for"], str)


def test_get_task_location_not_found():
    """Test 404 response for non-existent task."""
    response = client.get("/api/v1/slayer/location/99999")
    
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Task not found"


def test_get_task_location_invalid_id():
    """Test 422 response for invalid task ID format."""
    response = client.get("/api/v1/slayer/location/invalid")
    
    # FastAPI returns 422 for validation errors
    assert response.status_code == 422


def test_get_task_location_response_headers(sample_task):
    """Test that response includes proper headers."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    # Verify content type
    assert "application/json" in response.headers["content-type"]


def test_get_task_location_with_strategy(sample_task):
    """Test that strategy field is populated."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Abyssal demons should have strategy data
    assert len(data["strategy"]) > 0
    assert "Arclight" in data["strategy"]


def test_get_task_location_with_weaknesses(sample_task):
    """Test that weaknesses are included."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Abyssal demons weak to Slash and Demonbane
    assert "Slash" in data["weakness"]
    assert "Demonbane" in data["weakness"]


def test_get_task_location_multiple_locations(sample_task):
    """Test that multiple locations are returned."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    locations = data["locations"]
    
    # Abyssal demons should have 2 locations
    assert len(locations) == 2
    
    location_names = [loc["name"] for loc in locations]
    assert "Slayer Tower" in location_names
    assert "Catacombs of Kourend" in location_names


def test_get_task_location_with_requirements(sample_task):
    """Test that location requirements are properly formatted."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    locations = data["locations"]
    
    # Find Catacombs location
    catacombs = next(
        (loc for loc in locations if loc["name"] == "Catacombs of Kourend"),
        None
    )
    
    assert catacombs is not None
    assert "20% Arceuus favour" in catacombs["requirements"]


def test_get_task_location_pros_and_cons(sample_task):
    """Test that pros and cons are included."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    locations = data["locations"]
    
    # All locations should have pros and cons
    for location in locations:
        assert "pros" in location
        assert "cons" in location
        assert isinstance(location["pros"], list)
        assert isinstance(location["cons"], list)


def test_get_task_location_with_alternatives():
    """Test task with alternative monsters (Gargoyles -> Grotesque Guardians)."""
    with Session(test_engine) as session:
        # Create Gargoyle monster
        monster = Monster(
            id=2,
            name="Gargoyle",
            combat_level=111,
            hitpoints=105,
            slayer_xp=105,
            defence_level=80,
            magic_level=1,
            ranged_level=1,
            defence_stab=50,
            defence_slash=50,
            defence_crush=50,
            defence_magic=50,
            defence_ranged=50,
            is_slayer_monster=True
        )
        session.add(monster)
        session.commit()
        
        # Create Gargoyle task
        task = SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=monster.id,
            category="Gargoyles",
            quantity_min=110,
            quantity_max=170,
            weight=7,
            is_skippable=True,
            is_blockable=True
        )
        session.add(task)
        session.commit()
        
        task_id = task.id
    
    response = client.get(f"/api/v1/slayer/location/{task_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Should have alternatives
    assert len(data["alternatives"]) > 0
    
    # Verify alternative structure
    alternative = data["alternatives"][0]
    assert "name" in alternative
    assert "notes" in alternative
    assert "Grotesque Guardians" in alternative["name"]


def test_get_task_location_with_items_needed():
    """Test task with required items (Gargoyles -> Rock hammer)."""
    with Session(test_engine) as session:
        # Create Gargoyle monster
        monster = Monster(
            id=3,
            name="Gargoyle",
            combat_level=111,
            hitpoints=105,
            slayer_xp=105,
            defence_level=80,
            magic_level=1,
            ranged_level=1,
            defence_stab=50,
            defence_slash=50,
            defence_crush=50,
            defence_magic=50,
            defence_ranged=50,
            is_slayer_monster=True
        )
        session.add(monster)
        session.commit()
        
        # Create Gargoyle task
        task = SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=monster.id,
            category="Gargoyles",
            quantity_min=110,
            quantity_max=170,
            weight=7,
            is_skippable=True,
            is_blockable=True
        )
        session.add(task)
        session.commit()
        
        task_id = task.id
    
    response = client.get(f"/api/v1/slayer/location/{task_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Gargoyles require rock hammer
    assert "Rock hammer" in data["items_needed"]


def test_get_task_location_detailed_data_flag(sample_task):
    """Test has_detailed_data flag is accurate."""
    response = client.get(f"/api/v1/slayer/location/{sample_task}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Abyssal demons has detailed location data
    assert data["has_detailed_data"] is True


def test_get_task_location_no_detailed_data():
    """Test task with no detailed location data."""
    with Session(test_engine) as session:
        # Create unknown monster
        monster = Monster(
            id=4,
            name="Unknown Monster",
            combat_level=50,
            hitpoints=50,
            slayer_xp=50,
            defence_level=30,
            magic_level=1,
            ranged_level=1,
            defence_stab=10,
            defence_slash=10,
            defence_crush=10,
            defence_magic=10,
            defence_ranged=10,
            is_slayer_monster=True
        )
        session.add(monster)
        session.commit()
        
        # Create task
        task = SlayerTask(
            master=SlayerMaster.TURAEL,
            monster_id=monster.id,
            category="Unknown Category",
            quantity_min=10,
            quantity_max=20,
            weight=5,
            is_skippable=True,
            is_blockable=False
        )
        session.add(task)
        session.commit()
        
        task_id = task.id
    
    response = client.get(f"/api/v1/slayer/location/{task_id}")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Should have no detailed data
    assert data["has_detailed_data"] is False
    assert data["locations"] == []
    assert data["strategy"] == ""
