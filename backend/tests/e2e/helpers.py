"""Shared utilities and helpers for E2E tests."""

from typing import Dict, Any, Optional
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot, Monster, SlayerTask, SlayerMaster


def assert_successful_response(response, expected_status: int = 200) -> Dict[str, Any]:
    """Assert response is successful and return JSON data."""
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )
    return response.json()


def assert_error_response(response, expected_status: int) -> Dict[str, Any]:
    """Assert error response and return JSON data."""
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )
    return response.json()


def create_test_item(
    session: Session,
    item_id: int,
    name: str,
    high_price: int,
    low_price: int,
    members: bool = True,
    **kwargs,
) -> Item:
    """Create a test item in the database."""
    item = Item(
        id=item_id,
        name=name,
        members=members,
        limit=kwargs.get("limit", 70),
        value=kwargs.get("value", high_price),
        high_price=high_price,
        low_price=low_price,
        high_time=kwargs.get("high_time", 1700000000),
        low_time=kwargs.get("low_time", 1700000000),
        buy_limit=kwargs.get("buy_limit", 70),
        icon_url=kwargs.get("icon_url"),
    )
    session.add(item)
    session.commit()
    return item


def create_test_price_snapshot(
    session: Session,
    item_id: int,
    high_price: int,
    low_price: int,
    high_volume: int = 1000,
    low_volume: int = 1000,
    **kwargs,
) -> PriceSnapshot:
    """Create a test price snapshot in the database."""
    snapshot = PriceSnapshot(
        item_id=item_id,
        high_price=high_price,
        low_price=low_price,
        high_volume=high_volume,
        low_volume=low_volume,
        high_time=kwargs.get("high_time", 1700000000),
        low_time=kwargs.get("low_time", 1700000000),
    )
    session.add(snapshot)
    session.commit()
    return snapshot


def create_test_monster(
    session: Session,
    monster_id: int,
    name: str,
    combat_level: int,
    hitpoints: int,
    slayer_xp: float,
    **kwargs,
) -> Monster:
    """Create a test monster in the database."""
    from backend.models import Monster

    monster = Monster(
        id=monster_id,
        name=name,
        combat_level=combat_level,
        hitpoints=hitpoints,
        slayer_xp=slayer_xp,
        defence_level=kwargs.get("defence_level", 1),
        is_demon=kwargs.get("is_demon", False),
        is_dragon=kwargs.get("is_dragon", False),
        is_slayer_monster=kwargs.get("is_slayer_monster", True),
    )
    session.add(monster)
    session.commit()
    return monster


def create_test_slayer_task(
    session: Session,
    master: SlayerMaster,
    monster_id: int,
    category: str,
    quantity_min: int,
    quantity_max: int,
    weight: int,
    **kwargs,
) -> SlayerTask:
    """Create a test slayer task in the database."""
    task = SlayerTask(
        master=master,
        monster_id=monster_id,
        category=category,
        quantity_min=quantity_min,
        quantity_max=quantity_max,
        weight=weight,
        is_skippable=kwargs.get("is_skippable", True),
        is_blockable=kwargs.get("is_blockable", True),
    )
    session.add(task)
    session.commit()
    return task


def get_task_id_from_response(client: TestClient, master: SlayerMaster) -> Optional[int]:
    """Get the first task ID from a master's task list."""
    response = client.get(f"/api/v1/slayer/tasks/{master.value}")
    if response.status_code == 200:
        tasks = response.json()
        if tasks and len(tasks) > 0:
            return tasks[0].get("task_id")
    return None
