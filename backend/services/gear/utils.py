"""Utility functions for gear service."""

from typing import Optional
from sqlmodel import Session, select
from sqlalchemy import func

from backend.models import Item


def find_item_by_name(session: Session, item_name: str) -> Optional[Item]:
    """
    Find an item by name (case-insensitive, partial match).

    Args:
        session: Database session
        item_name: Item name to search for

    Returns:
        Item if found, None otherwise
    """
    # Try exact match first (case-insensitive) - using LOWER for SQLite compatibility
    items = session.exec(select(Item).where(func.lower(Item.name) == item_name.lower())).all()

    if items:
        return items[0]

    # Try partial match (case-insensitive)
    items = session.exec(
        select(Item).where(func.lower(Item.name).like(f"%{item_name.lower()}%"))
    ).all()

    if items:
        # Return the first match (prefer shorter names for better matches)
        return min(items, key=lambda x: len(x.name))

    return None
