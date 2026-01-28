"""Tests for slayer API endpoints."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import SlayerMaster, SlayerTask, Monster


def test_get_slayer_masters(client: TestClient):
    """Test getting list of slayer masters."""
    response = client.get("/api/v1/slayer/masters")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_master_tasks_with_data(client: TestClient, session: Session):
    """Test getting tasks for a master when data exists."""
    # Create test data using session fixture from conftest
    monster = Monster(id=1, name="Abyssal Demon", combat_level=124, hitpoints=150, slayer_xp=150)
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
        is_blockable=True,
    )
    session.add(task)
    session.commit()

    response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "monster_name" in data[0]
    assert "task_id" in data[0]


def test_get_task_advice_valid(client: TestClient, session: Session):
    """Test getting advice for a valid task with query parameters."""
    # Create test data
    monster = Monster(id=2, name="Waterfiend", combat_level=115, hitpoints=120, slayer_xp=128)
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
        is_blockable=True,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    task_id = task.id

    # Call with query parameters
    response = client.get(
        f"/api/v1/slayer/advice/{task_id}", params={"slayer_level": 85, "combat_level": 110}
    )

    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert "reason" in data
    assert "task" in data
    assert data["task"] == "Waterfiend"
    assert data["recommendation"] in ["DO", "SKIP", "BLOCK"]


def test_get_task_advice_with_defaults(client: TestClient, session: Session):
    """Test getting advice using default query parameters."""
    # Create test data
    monster = Monster(id=3, name="Abyssal demon", combat_level=124, hitpoints=150, slayer_xp=150)
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
        is_blockable=True,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    task_id = task.id

    # Call without query parameters (should use defaults)
    response = client.get(f"/api/v1/slayer/advice/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert "recommendation" in data
    assert data["recommendation"] == "DO"  # Abyssal demons should be DO


def test_get_task_advice_not_found(client: TestClient):
    """Test getting advice for non-existent task."""
    response = client.get(
        "/api/v1/slayer/advice/99999", params={"slayer_level": 85, "combat_level": 110}
    )

    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert "not found" in data["error"].get("message", "").lower()


def test_get_task_advice_invalid_stats(client: TestClient):
    """Test that advice endpoint validates stat ranges."""
    # Test slayer level too high
    response = client.get(
        "/api/v1/slayer/advice/1", params={"slayer_level": 100, "combat_level": 110}
    )
    assert response.status_code == 422  # Validation error

    # Test combat level too low
    response = client.get("/api/v1/slayer/advice/1", params={"slayer_level": 85, "combat_level": 2})
    assert response.status_code == 422  # Validation error
