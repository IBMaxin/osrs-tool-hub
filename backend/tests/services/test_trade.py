"""Tests for trade service."""

import pytest
from datetime import datetime, timedelta, timezone
from sqlmodel import Session

from backend.services.trade import TradeService
from backend.models import Item


class TestTradeService:
    """Test TradeService methods."""

    def test_log_trade_bought(self, session: Session):
        """Test logging a bought trade."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )

        assert trade.user_id == "test_user_1"
        assert trade.item_id == 4151
        assert trade.item_name == "Abyssal whip"
        assert trade.buy_price == 1500000
        assert trade.quantity == 1
        assert trade.status == "bought"
        assert trade.sell_price is None
        assert trade.profit == 0

    def test_log_trade_sold(self, session: Session):
        """Test logging a sold trade."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        assert trade.status == "sold"
        assert trade.sell_price == 1600000
        assert trade.profit > 0  # Should calculate profit

    def test_log_trade_cancelled(self, session: Session):
        """Test logging a cancelled trade."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="cancelled",
        )

        assert trade.status == "cancelled"

    def test_log_trade_invalid_status(self, session: Session):
        """Test logging trade with invalid status."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        with pytest.raises(ValueError, match="Invalid status"):
            service.log_trade(
                user_id="test_user_1",
                item_id=4151,
                buy_price=1500000,
                quantity=1,
                status="invalid",
            )

    def test_log_trade_invalid_quantity(self, session: Session):
        """Test logging trade with invalid quantity."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        with pytest.raises(ValueError, match="Quantity must be greater than 0"):
            service.log_trade(
                user_id="test_user_1",
                item_id=4151,
                buy_price=1500000,
                quantity=0,
            )

    def test_log_trade_invalid_buy_price(self, session: Session):
        """Test logging trade with invalid buy price."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        with pytest.raises(ValueError, match="Buy price must be greater than 0"):
            service.log_trade(
                user_id="test_user_1",
                item_id=4151,
                buy_price=0,
                quantity=1,
            )

    def test_log_trade_item_not_found(self, session: Session):
        """Test logging trade for non-existent item."""
        service = TradeService(session)
        with pytest.raises(ValueError, match="Item with ID 99999 not found"):
            service.log_trade(
                user_id="test_user_1",
                item_id=99999,
                buy_price=1500000,
                quantity=1,
            )

    def test_get_trade_history_all(self, session: Session):
        """Test getting all trade history."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        history = service.get_trade_history("test_user_1")
        assert len(history) == 2
        assert history[0].status == "sold"  # Most recent first

    def test_get_trade_history_filter_by_status(self, session: Session):
        """Test getting trade history filtered by status."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        history = service.get_trade_history("test_user_1", status="sold")
        assert len(history) == 1
        assert history[0].status == "sold"

    def test_get_trade_history_filter_by_item_id(self, session: Session):
        """Test getting trade history filtered by item ID."""
        item1 = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        item2 = Item(id=314, name="Feather", members=False, value=2)
        session.add(item1)
        session.add(item2)
        session.commit()

        service = TradeService(session)
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        service.log_trade(
            user_id="test_user_1",
            item_id=314,
            buy_price=2,
            quantity=100,
            status="bought",
        )

        history = service.get_trade_history("test_user_1", item_id=4151)
        assert len(history) == 1
        assert history[0].item_id == 4151

    def test_get_trade_history_filter_by_date_range(self, session: Session):
        """Test getting trade history filtered by date range."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade1 = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )

        # Manually set created_at to past date
        trade1.created_at = datetime.now(timezone.utc) - timedelta(days=10)
        session.add(trade1)
        session.commit()

        trade2 = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )

        start_date = datetime.now(timezone.utc) - timedelta(days=5)
        history = service.get_trade_history("test_user_1", start_date=start_date)
        assert len(history) == 1
        assert history[0].id == trade2.id

    def test_get_trade_history_limit(self, session: Session):
        """Test getting trade history with limit."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        for i in range(10):
            service.log_trade(
                user_id="test_user_1",
                item_id=4151,
                buy_price=1500000,
                quantity=1,
                status="bought",
            )

        history = service.get_trade_history("test_user_1", limit=5)
        assert len(history) == 5

    def test_get_trade_history_invalid_status(self, session: Session):
        """Test getting trade history with invalid status filter."""
        service = TradeService(session)
        with pytest.raises(ValueError, match="Invalid status"):
            service.get_trade_history("test_user_1", status="invalid")

    def test_get_trade_stats_no_trades(self, session: Session):
        """Test getting trade stats when user has no trades."""
        service = TradeService(session)
        stats = service.get_trade_stats("test_user_1")
        assert stats["total_profit"] == 0
        assert stats["total_trades"] == 0
        assert stats["sold_trades"] == 0
        assert stats["profit_per_hour"] == 0.0
        assert stats["best_items"] == []
        assert stats["profit_by_item"] == {}

    def test_get_trade_stats_all_time(self, session: Session):
        """Test getting trade stats for all time."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        # Create bought trade
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        # Create sold trade
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1")
        assert stats["total_trades"] == 2
        assert stats["sold_trades"] == 1
        assert stats["total_profit"] > 0

    def test_get_trade_stats_with_days_filter(self, session: Session):
        """Test getting trade stats filtered by days."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade1 = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        # Set created_at to past date
        trade1.created_at = datetime.now(timezone.utc) - timedelta(days=10)
        session.add(trade1)
        session.commit()

        _ = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1", days=5)
        assert stats["total_trades"] == 1
        assert stats["sold_trades"] == 1

    def test_get_trade_stats_profit_by_item(self, session: Session):
        """Test getting trade stats with profit breakdown by item."""
        item1 = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        item2 = Item(id=314, name="Feather", members=False, value=2)
        session.add(item1)
        session.add(item2)
        session.commit()

        service = TradeService(session)
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )
        service.log_trade(
            user_id="test_user_1",
            item_id=314,
            buy_price=2,
            sell_price=3,
            quantity=100,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1")
        assert "Abyssal whip" in stats["profit_by_item"]
        assert "Feather" in stats["profit_by_item"]
        assert len(stats["best_items"]) == 2

    def test_get_trade_stats_best_items_sorted(self, session: Session):
        """Test that best items are sorted by profit descending."""
        item1 = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        item2 = Item(id=314, name="Feather", members=False, value=2)
        session.add(item1)
        session.add(item2)
        session.commit()

        service = TradeService(session)
        # Lower profit first
        service.log_trade(
            user_id="test_user_1",
            item_id=314,
            buy_price=2,
            sell_price=3,
            quantity=100,
            status="sold",
        )
        # Higher profit second
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1")
        assert len(stats["best_items"]) == 2
        assert stats["best_items"][0]["item_name"] == "Abyssal whip"  # Higher profit first
        assert stats["best_items"][1]["item_name"] == "Feather"

    def test_get_trade_stats_profit_per_hour(self, session: Session):
        """Test calculating profit per hour."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        trade1 = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        # Set created_at to 2 hours ago
        trade1.created_at = datetime.now(timezone.utc) - timedelta(hours=2)
        trade1.updated_at = datetime.now(timezone.utc)
        session.add(trade1)
        session.commit()

        _ = service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1")
        assert stats["profit_per_hour"] > 0

    def test_get_trade_stats_only_sold_trades_count(self, session: Session):
        """Test that only sold trades count toward profit."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        service = TradeService(session)
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        service.log_trade(
            user_id="test_user_1",
            item_id=4151,
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
        )

        stats = service.get_trade_stats("test_user_1")
        assert stats["total_trades"] == 2
        assert stats["sold_trades"] == 1
        assert stats["total_profit"] > 0  # Only sold trade contributes
