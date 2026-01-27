"""Tests for slayer API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.db.session import get_session
from backend.models import SlayerMaster, SlayerTask, Monster

# Create test engine
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
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


def test_get_slayer_masters():
    """Test getting list of slayer masters."""
    response = client.get("/api/v1/slayer/masters")
    
    # Should return 200
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_master_tasks_with_data():
    """Test getting tasks for a master when data exists."""
    # Create test data
    with Session(test_engine) as session:
        monster = Monster(
            id=1,
            name="Abyssal Demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150
        )
        session.add(monster)
        
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
    
    response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
    
    # Should return 200
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "monster_name" in data[0]
        assert "task_id" in data[0]


def test_get_task_advice_valid():
    """Test getting advice for a valid task with query parameters."""
    # Create test data
    with Session(test_engine) as session:
        monster = Monster(
            id=2,
            name="Waterfiend",
            combat_level=115,
            hitpoints=120,
            slayer_xp=128
        )
        session.add(monster)
        session.commit()
        
        task = SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=monster.id,
            category="Waterfiends",
            quantity_min=130,
            quantity_max=170,
            weight=8,
            is_skippable=True,
            is_blockable=True
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id
    
    # Call with query parameters
    response = client.get(
        f"/api/v1/slayer/advice/{task_id}",
        params={"slayer_level": 85, "combat_level": 110}
    )
    
    # Should return 200
    assert response.status_code == 200
    data = response.json()
    # Check for correct response structure
    assert "recommendation" in data
    assert "reason" in data
    assert "task" in data
    assert data["task"] == "Waterfiend"
    assert data["recommendation"] in ["DO", "SKIP", "BLOCK"]


def test_get_task_advice_with_defaults():
    """Test getting advice using default query parameters."""
    # Create test data
    with Session(test_engine) as session:
        monster = Monster(
            id=3,
            name="Abyssal demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150
        )
        session.add(monster)
        session.commit()
        
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
        task_id = task.id
    
    # Call without query parameters (should use defaults)
    response = client.get(f"/api/v1/slayer/advice/{task_id}")
    
    # Should return 200 with default values
    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert data["recommendation"] == "DO"  # Abyssal demons should be DO


def test_get_task_advice_not_found():
    """Test getting advice for non-existent task."""
    response = client.get(
        "/api/v1/slayer/advice/99999",
        params={"slayer_level": 85, "combat_level": 110}
    )
    
    # Should return 404 Not Found
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_task_advice_invalid_stats():
    """Test that advice endpoint validates stat ranges."""
    # Test slayer level too high
    response = client.get(
        "/api/v1/slayer/advice/1",
        params={"slayer_level": 100, "combat_level": 110}
    )
    assert response.status_code == 422  # Validation error
    
    # Test combat level too low
    response = client.get(
        "/api/v1/slayer/advice/1",
        params={"slayer_level": 85, "combat_level": 2}
    )
    assert response.status_code == 422  # Validation error
