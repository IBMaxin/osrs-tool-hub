"""Item pricing utilities."""
from sqlmodel import Session, select

from backend.models import Item, PriceSnapshot


def get_item_price(session: Session, item: Item) -> int:
    """
    Get the current price of an item from PriceSnapshot or fallback to value.

    Args:
        session: Database session
        item: Item to get price for

    Returns:
        Item price in GP
    """
    price_snapshot = session.exec(
        select(PriceSnapshot).where(PriceSnapshot.item_id == item.id)
    ).first()

    if price_snapshot and price_snapshot.high_price:
        return price_snapshot.high_price
    return item.value or 0


def get_item_cost(session: Session, item: Item) -> int:
    """
    Get buy/low price for an item (for gear set total cost).

    Uses PriceSnapshot.low_price, Item.low_price, or value.

    Args:
        session: Database session
        item: Item to get cost for

    Returns:
        Item cost in GP
    """
    price_snapshot = session.exec(
        select(PriceSnapshot).where(PriceSnapshot.item_id == item.id)
    ).first()
    if price_snapshot and price_snapshot.low_price is not None:
        return price_snapshot.low_price
    if item.low_price is not None:
        return item.low_price
    return item.value or 0
