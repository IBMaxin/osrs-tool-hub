"""Gear set models."""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class GearSet(SQLModel, table=True):
    """Gear set model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    items: str  # JSON string of item IDs and quantities
    total_cost: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
