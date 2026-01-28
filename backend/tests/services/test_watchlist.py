"""Tests for watchlist service."""

import pytest
from datetime import datetime, timezone
from sqlmodel import Session

from backend.services.watchlist import WatchlistService
from backend.models import WatchlistItem, WatchlistAlert, Item, PriceSnapshot


class TestWatchlistService:
    """Test WatchlistService methods."""

    def test_add_to_watchlist_success(self, session: Session):
        """Test adding item to watchlist successfully."""
        # Create test item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            value=2000000,
        )
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        assert watchlist_item.user_id == "test_user_1"
        assert watchlist_item.item_id == 4151
        assert watchlist_item.item_name == "Abyssal whip"
        assert watchlist_item.alert_type == "price_below"
        assert watchlist_item.threshold == 1500000
        assert watchlist_item.is_active is True

    def test_add_to_watchlist_invalid_alert_type(self, session: Session):
        """Test adding to watchlist with invalid alert type."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        with pytest.raises(ValueError, match="Invalid alert_type"):
            service.add_to_watchlist(
                user_id="test_user_1",
                item_id=4151,
                alert_type="invalid_type",
                threshold=1500000,
            )

    def test_add_to_watchlist_invalid_threshold(self, session: Session):
        """Test adding to watchlist with invalid threshold."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        with pytest.raises(ValueError, match="Threshold must be greater than 0"):
            service.add_to_watchlist(
                user_id="test_user_1",
                item_id=4151,
                alert_type="price_below",
                threshold=0,
            )

    def test_add_to_watchlist_item_not_found(self, session: Session):
        """Test adding non-existent item to watchlist."""
        service = WatchlistService(session)
        with pytest.raises(ValueError, match="Item with ID 99999 not found"):
            service.add_to_watchlist(
                user_id="test_user_1",
                item_id=99999,
                alert_type="price_below",
                threshold=1500000,
            )

    def test_add_to_watchlist_updates_existing(self, session: Session):
        """Test that adding duplicate watchlist item updates existing."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        # Add first time
        watchlist_item1 = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )
        first_id = watchlist_item1.id

        # Add again with different threshold
        watchlist_item2 = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1600000,
        )

        # Should be same item with updated threshold
        assert watchlist_item2.id == first_id
        assert watchlist_item2.threshold == 1600000
        assert watchlist_item2.last_triggered_at is None

    def test_get_watchlist_active_only(self, session: Session):
        """Test getting watchlist with only active items."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        # Add active item
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        # Add inactive item
        inactive_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_above",
            threshold=2000000,
            is_active=False,
        )
        session.add(inactive_item)
        session.commit()

        watchlist = service.get_watchlist("test_user_1", include_inactive=False)
        assert len(watchlist) == 1
        assert watchlist[0].is_active is True

    def test_get_watchlist_include_inactive(self, session: Session):
        """Test getting watchlist including inactive items."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        inactive_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_above",
            threshold=2000000,
            is_active=False,
        )
        session.add(inactive_item)
        session.commit()

        watchlist = service.get_watchlist("test_user_1", include_inactive=True)
        assert len(watchlist) == 2

    def test_remove_from_watchlist_success(self, session: Session):
        """Test removing item from watchlist."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        result = service.remove_from_watchlist(watchlist_item.id, "test_user_1")
        assert result is True

        session.refresh(watchlist_item)
        assert watchlist_item.is_active is False

    def test_remove_from_watchlist_not_found(self, session: Session):
        """Test removing non-existent watchlist item."""
        service = WatchlistService(session)
        result = service.remove_from_watchlist(99999, "test_user_1")
        assert result is False

    def test_remove_from_watchlist_wrong_user(self, session: Session):
        """Test removing watchlist item belonging to different user."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        with pytest.raises(ValueError, match="does not belong to user"):
            service.remove_from_watchlist(watchlist_item.id, "test_user_2")

    def test_get_alerts_no_watchlist(self, session: Session):
        """Test getting alerts when user has no watchlist."""
        service = WatchlistService(session)
        alerts = service.get_alerts("test_user_1")
        assert alerts == []

    def test_get_alerts_with_alerts(self, session: Session):
        """Test getting alerts for user."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        # Create alert
        alert = WatchlistAlert(
            watchlist_item_id=watchlist_item.id,
            current_value=1400000,
            threshold_value=1500000,
            message="Test alert",
        )
        session.add(alert)
        session.commit()

        alerts = service.get_alerts("test_user_1")
        assert len(alerts) == 1
        assert alerts[0].message == "Test alert"

    def test_get_alerts_limit(self, session: Session):
        """Test getting alerts with limit."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        # Create multiple alerts
        for i in range(10):
            alert = WatchlistAlert(
                watchlist_item_id=watchlist_item.id,
                current_value=1400000 + i,
                threshold_value=1500000,
                message=f"Alert {i}",
            )
            session.add(alert)
        session.commit()

        alerts = service.get_alerts("test_user_1", limit=5)
        assert len(alerts) == 5

    def test_evaluate_alerts_price_below_triggered(self, session: Session):
        """Test evaluating alerts - price_below triggered."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        # Create price snapshot
        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,  # Below threshold
        )
        session.add(price_snapshot)
        session.commit()

        service = WatchlistService(session)
        _ = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 1

        # Check alert was created
        alerts = service.get_alerts("test_user_1")
        assert len(alerts) == 1
        assert "price dropped" in alerts[0].message.lower()

    def test_evaluate_alerts_price_above_triggered(self, session: Session):
        """Test evaluating alerts - price_above triggered."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1600000,
            low_price=1600000,  # Above threshold
        )
        session.add(price_snapshot)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_above",
            threshold=1500000,
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 1

    def test_evaluate_alerts_margin_above_triggered(self, session: Session):
        """Test evaluating alerts - margin_above triggered."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1600000,
            low_price=1400000,
        )
        session.add(price_snapshot)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="margin_above",
            threshold=100000,  # Margin should be ~168000 (1600000 - 2% tax - 1400000)
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 1

    def test_evaluate_alerts_not_triggered(self, session: Session):
        """Test evaluating alerts when conditions not met."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1600000,
            low_price=1600000,  # Above threshold for price_below
        )
        session.add(price_snapshot)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 0

    def test_evaluate_alerts_no_price_snapshot(self, session: Session):
        """Test evaluating alerts when no price snapshot exists."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 0

    def test_evaluate_alerts_cooldown_period(self, session: Session):
        """Test that alerts respect cooldown period."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
        )
        session.add(price_snapshot)
        session.commit()

        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )

        # Set last_triggered_at to recent time (within 1 hour)
        watchlist_item.last_triggered_at = datetime.now(timezone.utc)
        session.add(watchlist_item)
        session.commit()

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 0  # Should not trigger due to cooldown

    def test_evaluate_alerts_multiple_items(self, session: Session):
        """Test evaluating alerts for multiple watchlist items."""
        item1 = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        item2 = Item(id=314, name="Feather", members=False, value=2)
        session.add(item1)
        session.add(item2)
        session.commit()

        price_snapshot1 = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,  # Triggers
        )
        price_snapshot2 = PriceSnapshot(
            item_id=314,
            high_price=5,
            low_price=1,  # Triggers
        )
        session.add(price_snapshot1)
        session.add(price_snapshot2)
        session.commit()

        service = WatchlistService(session)
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=4151,
            alert_type="price_below",
            threshold=1500000,
        )
        service.add_to_watchlist(
            user_id="test_user_1",
            item_id=314,
            alert_type="price_below",
            threshold=3,
        )

        triggered_count = service.evaluate_alerts()
        assert triggered_count == 2
