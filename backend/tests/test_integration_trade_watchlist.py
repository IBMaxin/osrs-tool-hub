"""Integration tests for Trade and Watchlist service interactions."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot, Trade, WatchlistItem
from backend.services.trade import TradeService
from backend.services.watchlist import WatchlistService


@pytest.mark.integration
class TestTradeWatchlistIntegration:
    """Test integration between Trade and Watchlist services."""

    def test_trade_creation_with_watchlist_item(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that trading an item that's on watchlist works correctly."""
        user_id = "test-user-integration"
        item = sample_items[0]

        # Step 1: Add item to watchlist
        watchlist_payload = {
            "user_id": user_id,
            "item_id": item.id,
            "alert_type": "price_below",
            "threshold": 1450000,
        }
        watchlist_response = client.post("/api/v1/watchlist", json=watchlist_payload)
        assert watchlist_response.status_code == 201
        watchlist_id = watchlist_response.json()["id"]

        # Step 2: Create a trade for the same item
        trade_payload = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1400000,
            "quantity": 1,
            "status": "bought",
        }
        trade_response = client.post("/api/v1/trades", json=trade_payload)
        assert trade_response.status_code == 201

        # Step 3: Verify both exist independently
        watchlist_items = client.get(f"/api/v1/watchlist?user_id={user_id}").json()
        assert len(watchlist_items) == 1
        assert watchlist_items[0]["id"] == watchlist_id

        trades = client.get(f"/api/v1/trades?user_id={user_id}").json()
        assert len(trades) == 1
        assert trades[0]["item_id"] == item.id

    def test_trade_stats_with_watchlist_items(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that trade stats work correctly when user has watchlist items."""
        user_id = "test-user-stats-watchlist"
        item1 = sample_items[0]
        item2 = sample_items[1] if len(sample_items) > 1 else sample_items[0]

        # Add items to watchlist
        client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user_id,
                "item_id": item1.id,
                "alert_type": "price_below",
                "threshold": 1000,
            },
        )
        client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user_id,
                "item_id": item2.id,
                "alert_type": "price_above",
                "threshold": 1000,
            },
        )

        # Create trades
        client.post(
            "/api/v1/trades",
            json={
                "user_id": user_id,
                "item_id": item1.id,
                "buy_price": 1000,
                "quantity": 10,
                "sell_price": 1100,
                "status": "sold",
            },
        )

        # Get trade stats
        stats_response = client.get(f"/api/v1/trades/stats?user_id={user_id}")
        assert stats_response.status_code == 200
        stats = stats_response.json()

        assert stats["total_trades"] == 1
        assert stats["sold_trades"] == 1
        assert "total_profit" in stats

        # Verify watchlist still works
        watchlist_response = client.get(f"/api/v1/watchlist?user_id={user_id}")
        assert watchlist_response.status_code == 200
        watchlist = watchlist_response.json()
        assert len(watchlist) == 2

    def test_multiple_users_trade_same_item(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that multiple users can trade the same item independently."""
        item = sample_items[0]
        user1 = "user-1"
        user2 = "user-2"

        # User 1 creates trade
        trade1 = client.post(
            "/api/v1/trades",
            json={
                "user_id": user1,
                "item_id": item.id,
                "buy_price": 1400000,
                "quantity": 1,
            },
        )
        assert trade1.status_code == 201

        # User 2 creates trade for same item
        trade2 = client.post(
            "/api/v1/trades",
            json={
                "user_id": user2,
                "item_id": item.id,
                "buy_price": 1400000,
                "quantity": 1,
            },
        )
        assert trade2.status_code == 201

        # Verify both users see only their trades
        user1_trades = client.get(f"/api/v1/trades?user_id={user1}").json()
        user2_trades = client.get(f"/api/v1/trades?user_id={user2}").json()

        assert len(user1_trades) == 1
        assert len(user2_trades) == 1
        assert user1_trades[0]["user_id"] == user1
        assert user2_trades[0]["user_id"] == user2

    def test_trade_deletion_with_watchlist(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that deleting a watchlist item doesn't affect trades."""
        user_id = "test-user-delete"
        item = sample_items[0]

        # Create watchlist item
        watchlist_response = client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user_id,
                "item_id": item.id,
                "alert_type": "price_below",
                "threshold": 1000,
            },
        )
        watchlist_id = watchlist_response.json()["id"]

        # Create trade
        trade_response = client.post(
            "/api/v1/trades",
            json={
                "user_id": user_id,
                "item_id": item.id,
                "buy_price": 1000,
                "quantity": 1,
            },
        )
        trade_id = trade_response.json()["id"]

        # Delete watchlist item
        delete_response = client.delete(f"/api/v1/watchlist/{watchlist_id}?user_id={user_id}")
        assert delete_response.status_code == 204

        # Verify trade still exists
        trade = client.get(f"/api/v1/trades?user_id={user_id}").json()
        assert len(trade) == 1
        assert trade[0]["id"] == trade_id

        # Verify watchlist is empty
        watchlist = client.get(f"/api/v1/watchlist?user_id={user_id}").json()
        assert len(watchlist) == 0


@pytest.mark.integration
class TestTradeServiceIntegration:
    """Test TradeService integration with database and other services."""

    def test_trade_service_with_price_updates(
        self, session: Session, sample_items: list[Item], sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test that TradeService correctly uses item prices from database."""
        service = TradeService(session)
        item = sample_items[0]

        # Create trade
        trade = service.log_trade(
            user_id="test-user",
            item_id=item.id,
            buy_price=1400000,
            quantity=1,
            sell_price=1500000,
            status="sold",
        )

        assert trade.item_id == item.id
        assert trade.item_name == item.name
        assert trade.profit > 0  # Should account for tax

        # Verify trade is in database
        from sqlmodel import select

        db_trade = session.exec(select(Trade).where(Trade.id == trade.id)).first()
        assert db_trade is not None
        assert db_trade.item_name == item.name

    def test_trade_stats_aggregation(
        self, session: Session, sample_items: list[Item]
    ):
        """Test that trade stats correctly aggregate multiple trades."""
        service = TradeService(session)
        item = sample_items[0]
        user_id = "test-user-stats"

        # Create multiple trades
        for i in range(3):
            service.log_trade(
                user_id=user_id,
                item_id=item.id,
                buy_price=1000 + i * 100,
                quantity=10,
                sell_price=1100 + i * 100,
                status="sold",
            )

        # Get stats
        stats = service.get_trade_stats(user_id=user_id)

        assert stats["total_trades"] == 3
        assert stats["sold_trades"] == 3
        assert stats["total_profit"] > 0
        assert len(stats["best_items"]) > 0
