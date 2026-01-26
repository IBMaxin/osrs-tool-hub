"""Flipping models."""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Flip(SQLModel, table=True):
    """Flip tracking model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int
    item_name: str
    buy_price: int
    sell_price: int
    profit: int
    profit_percent: float
    volume: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
