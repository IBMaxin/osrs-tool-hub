"""Watchlist service for managing item watchlists and price alerts."""

from datetime import datetime
from typing import List

from sqlmodel import Session, select

from backend.models import WatchlistItem, WatchlistAlert, Item, PriceSnapshot
from backend.services.flipping import calculate_tax


class WatchlistService:
    """Service for managing watchlists and alerts."""

    def __init__(self, session: Session):
        """
        Initialize watchlist service.

        Args:
            session: Database session
        """
        self.session = session

    def add_to_watchlist(
        self,
        user_id: str,
        item_id: int,
        alert_type: str,
        threshold: int,
    ) -> WatchlistItem:
        """
        Add an item to the user's watchlist with alert rules.

        Args:
            user_id: User identifier
            item_id: OSRS item ID
            alert_type: Alert type ('price_below', 'price_above', 'margin_above')
            threshold: Threshold value for alert (price or margin in GP)

        Returns:
            Created WatchlistItem object

        Raises:
            ValueError: If alert_type is invalid or item not found
        """
        if alert_type not in ("price_below", "price_above", "margin_above"):
            raise ValueError(
                f"Invalid alert_type: {alert_type}. Must be 'price_below', 'price_above', or 'margin_above'"
            )

        if threshold <= 0:
            raise ValueError("Threshold must be greater than 0")

        # Get item name from database
        item = self.session.get(Item, item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")

        item_name = item.name

        # Check if watchlist item already exists for this user/item/alert_type
        existing = self.session.exec(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.item_id == item_id,
                WatchlistItem.alert_type == alert_type,
                WatchlistItem.is_active.is_(True),
            )
        ).first()

        if existing:
            # Update existing watchlist item
            existing.threshold = threshold
            existing.last_triggered_at = None  # Reset trigger time
            self.session.add(existing)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        # Create new watchlist item
        watchlist_item = WatchlistItem(
            user_id=user_id,
            item_id=item_id,
            item_name=item_name,
            alert_type=alert_type,
            threshold=threshold,
            is_active=True,
        )

        self.session.add(watchlist_item)
        self.session.commit()
        self.session.refresh(watchlist_item)

        return watchlist_item

    def get_watchlist(self, user_id: str, include_inactive: bool = False) -> List[WatchlistItem]:
        """
        Get user's watchlist.

        Args:
            user_id: User identifier
            include_inactive: If True, include inactive watchlist items

        Returns:
            List of WatchlistItem objects
        """
        query = select(WatchlistItem).where(WatchlistItem.user_id == user_id)

        if not include_inactive:
            query = query.where(WatchlistItem.is_active.is_(True))

        query = query.order_by(WatchlistItem.created_at.desc())

        watchlist_items = self.session.exec(query).all()
        return list(watchlist_items)

    def remove_from_watchlist(self, watchlist_item_id: int, user_id: str) -> bool:
        """
        Remove an item from the watchlist (deactivate it).

        Args:
            watchlist_item_id: Watchlist item ID
            user_id: User identifier (for security check)

        Returns:
            True if removed, False if not found

        Raises:
            ValueError: If watchlist item doesn't belong to user
        """
        watchlist_item = self.session.get(WatchlistItem, watchlist_item_id)

        if not watchlist_item:
            return False

        if watchlist_item.user_id != user_id:
            raise ValueError("Watchlist item does not belong to user")

        # Deactivate instead of deleting (soft delete)
        watchlist_item.is_active = False
        self.session.add(watchlist_item)
        self.session.commit()

        return True

    def get_alerts(self, user_id: str, limit: int = 50) -> List[WatchlistAlert]:
        """
        Get triggered alerts for a user.

        Args:
            user_id: User identifier
            limit: Maximum number of alerts to return

        Returns:
            List of WatchlistAlert objects sorted by triggered_at descending
        """
        # Get user's watchlist item IDs
        watchlist_items = self.get_watchlist(user_id, include_inactive=True)
        watchlist_item_ids = [item.id for item in watchlist_items if item.id is not None]

        if not watchlist_item_ids:
            return []

        query = select(WatchlistAlert).where(
            WatchlistAlert.watchlist_item_id.in_(watchlist_item_ids)
        )
        query = query.order_by(WatchlistAlert.triggered_at.desc())
        query = query.limit(limit)

        alerts = self.session.exec(query).all()
        return list(alerts)

    def evaluate_alerts(self) -> int:
        """
        Evaluate all active watchlist alerts against current prices.

        This method is called by the scheduler to check if any alerts should be triggered.

        Returns:
            Number of alerts triggered
        """
        # Get all active watchlist items
        active_items = self.session.exec(
            select(WatchlistItem).where(WatchlistItem.is_active.is_(True))
        ).all()

        triggered_count = 0

        for item in active_items:
            # Get current price snapshot
            price_snapshot = self.session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == item.item_id)
            ).first()

            if not price_snapshot or not price_snapshot.high_price or not price_snapshot.low_price:
                continue

            current_price = price_snapshot.low_price  # Use low_price as current buy price
            sell_price = price_snapshot.high_price

            # Evaluate alert based on type
            should_trigger = False
            current_value = 0
            message = ""

            if item.alert_type == "price_below":
                current_value = current_price
                if current_price <= item.threshold:
                    should_trigger = True
                    message = f"{item.item_name} price dropped to {current_price} GP (threshold: {item.threshold} GP)"

            elif item.alert_type == "price_above":
                current_value = current_price
                if current_price >= item.threshold:
                    should_trigger = True
                    message = f"{item.item_name} price rose to {current_price} GP (threshold: {item.threshold} GP)"

            elif item.alert_type == "margin_above":
                # Calculate margin (post-tax)
                tax = calculate_tax(sell_price)
                margin = (sell_price - tax) - current_price
                current_value = margin
                if margin >= item.threshold:
                    should_trigger = True
                    message = f"{item.item_name} margin reached {margin} GP (threshold: {item.threshold} GP)"

            if should_trigger:
                # Check if we've already triggered this alert recently (within last hour)
                # to avoid spam
                if item.last_triggered_at:
                    time_since_trigger = (
                        datetime.now(item.last_triggered_at.tzinfo) - item.last_triggered_at
                    ).total_seconds()
                    if time_since_trigger < 3600:  # 1 hour
                        continue

                # Create alert
                alert = WatchlistAlert(
                    watchlist_item_id=item.id,
                    current_value=current_value,
                    threshold_value=item.threshold,
                    message=message,
                )

                self.session.add(alert)

                # Update last_triggered_at
                item.last_triggered_at = datetime.now(item.created_at.tzinfo)
                self.session.add(item)

                triggered_count += 1

        if triggered_count > 0:
            self.session.commit()

        return triggered_count
