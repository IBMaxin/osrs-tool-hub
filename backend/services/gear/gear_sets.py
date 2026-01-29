"""Gear set CRUD operations."""

import json
from typing import Optional
from sqlmodel import Session, select

from backend.models import GearSet, Item
from backend.services.gear.pricing import get_item_cost


def create_gear_set(
    session: Session,
    name: str,
    items: dict[int, int],
    description: Optional[str] = None,
) -> GearSet:
    """
    Create a new gear set.

    Args:
        session: Database session
        name: Name of the gear set
        items: Dict of item_id -> quantity
        description: Optional description

    Returns:
        Created gear set
    """
    # Calculate total cost from DB (use low/buy price for gear set cost)
    total_cost = 0
    for item_id, quantity in items.items():
        item = session.get(Item, item_id)
        if item:
            total_cost += get_item_cost(session, item) * quantity

    gear_set = GearSet(
        name=name,
        description=description,
        items=json.dumps(items),
        total_cost=total_cost,
    )

    session.add(gear_set)
    session.commit()
    session.refresh(gear_set)

    return gear_set


def get_all_gear_sets(session: Session) -> list[GearSet]:
    """
    Get all gear sets.

    Args:
        session: Database session

    Returns:
        List of all gear sets
    """
    statement = select(GearSet).order_by(GearSet.created_at.desc())
    return list(session.exec(statement).all())


def get_gear_set_by_id(session: Session, gear_set_id: int) -> Optional[GearSet]:
    """
    Get gear set by ID.

    Args:
        session: Database session
        gear_set_id: Gear set ID

    Returns:
        Gear set or None if not found
    """
    return session.get(GearSet, gear_set_id)


def delete_gear_set(session: Session, gear_set_id: int) -> bool:
    """
    Delete a gear set.

    Args:
        session: Database session
        gear_set_id: Gear set ID

    Returns:
        True if deleted, False if not found
    """
    gear_set = session.get(GearSet, gear_set_id)
    if gear_set:
        session.delete(gear_set)
        session.commit()
        return True
    return False
