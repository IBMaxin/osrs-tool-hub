"""Watchlist models for tracking items and price alerts."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class WatchlistItem(SQLModel, table=True):
    """Watchlist item model for tracking items with alert rules."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User identifier (UUID from localStorage)")
    item_id: int = Field(index=True, description="OSRS item ID")
    item_name: str = Field(description="Item name for display")
    alert_type: str = Field(
        description="Alert type: 'price_below', 'price_above', or 'margin_above'"
    )
    threshold: int = Field(description="Threshold value for alert (price or margin in GP)")
    is_active: bool = Field(default=True, index=True, description="Whether the alert is active")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_triggered_at: Optional[datetime] = Field(
        default=None, description="Last time this alert was triggered"
    )


class WatchlistAlert(SQLModel, table=True):
    """Watchlist alert model for tracking triggered alerts."""

    id: Optional[int] = Field(default=None, primary_key=True)
    watchlist_item_id: int = Field(
        index=True, foreign_key="watchlistitem.id", description="Reference to watchlist item"
    )
    triggered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        description="When the alert was triggered",
    )
    current_value: int = Field(description="Current value that triggered the alert")
    threshold_value: int = Field(description="Threshold value that was crossed")
    message: str = Field(description="Alert message")
