"""Tests for trades API endpoints."""

from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import datetime, timedelta, timezone

from backend.models import Trade, Item


class TestTradesEndpoints:
    """Test trades API endpoints."""

    def test_log_trade_bought(self, client: TestClient, session: Session):
        """Test logging a bought trade."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        payload = {
            "user_id": "test_user_1",
            "item_id": 4151,
            "buy_price": 1500000,
            "quantity": 1,
            "status": "bought",
        }

        response = client.post("/api/v1/trades", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == "test_user_1"
        assert data["item_id"] == 4151
        assert data["status"] == "bought"
        assert data["buy_price"] == 1500000

    def test_log_trade_sold(self, client: TestClient, session: Session):
        """Test logging a sold trade."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        payload = {
            "user_id": "test_user_1",
            "item_id": 4151,
            "buy_price": 1500000,
            "sell_price": 1600000,
            "quantity": 1,
            "status": "sold",
        }

        response = client.post("/api/v1/trades", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "sold"
        assert data["profit"] > 0

    def test_log_trade_invalid_status(self, client: TestClient, session: Session):
        """Test logging trade with invalid status."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        payload = {
            "user_id": "test_user_1",
            "item_id": 4151,
            "buy_price": 1500000,
            "quantity": 1,
            "status": "invalid",
        }

        response = client.post("/api/v1/trades", json=payload)
        assert response.status_code == 422  # Validation error

    def test_log_trade_item_not_found(self, client: TestClient):
        """Test logging trade for non-existent item."""
        payload = {
            "user_id": "test_user_1",
            "item_id": 99999,
            "buy_price": 1500000,
            "quantity": 1,
            "status": "bought",
        }

        response = client.post("/api/v1/trades", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_get_trade_history_all(self, client: TestClient, session: Session):
        """Test getting all trade history."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        trade1 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        trade2 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
            profit=100000,
        )
        session.add(trade1)
        session.add(trade2)
        session.commit()

        response = client.get("/api/v1/trades", params={"user_id": "test_user_1"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_get_trade_history_filter_by_status(self, client: TestClient, session: Session):
        """Test getting trade history filtered by status."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        trade1 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        trade2 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
            profit=100000,
        )
        session.add(trade1)
        session.add(trade2)
        session.commit()

        response = client.get(
            "/api/v1/trades",
            params={"user_id": "test_user_1", "status": "sold"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "sold"

    def test_get_trade_history_filter_by_item_id(self, client: TestClient, session: Session):
        """Test getting trade history filtered by item ID."""
        item1 = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        item2 = Item(id=314, name="Feather", members=False, value=2)
        session.add(item1)
        session.add(item2)
        session.commit()

        trade1 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        trade2 = Trade(
            user_id="test_user_1",
            item_id=314,
            item_name="Feather",
            buy_price=2,
            quantity=100,
            status="bought",
        )
        session.add(trade1)
        session.add(trade2)
        session.commit()

        response = client.get(
            "/api/v1/trades",
            params={"user_id": "test_user_1", "item_id": 4151},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["item_id"] == 4151

    def test_get_trade_stats_all_time(self, client: TestClient, session: Session):
        """Test getting trade stats for all time."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        trade1 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            quantity=1,
            status="bought",
        )
        trade2 = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
            profit=100000,
        )
        session.add(trade1)
        session.add(trade2)
        session.commit()

        response = client.get("/api/v1/trades/stats", params={"user_id": "test_user_1"})

        assert response.status_code == 200
        data = response.json()
        assert "total_profit" in data
        assert "total_trades" in data
        assert data["total_trades"] == 2
        assert data["sold_trades"] == 1

    def test_get_trade_stats_with_days(self, client: TestClient, session: Session):
        """Test getting trade stats filtered by days."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        # Old trade
        old_trade = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
            profit=100000,
        )
        old_trade.created_at = datetime.now(timezone.utc) - timedelta(days=10)
        session.add(old_trade)
        session.commit()

        # Recent trade
        recent_trade = Trade(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            buy_price=1500000,
            sell_price=1600000,
            quantity=1,
            status="sold",
            profit=100000,
        )
        session.add(recent_trade)
        session.commit()

        response = client.get(
            "/api/v1/trades/stats",
            params={"user_id": "test_user_1", "days": 5},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total_trades"] == 1  # Only recent trade

    def test_get_trade_stats_no_trades(self, client: TestClient):
        """Test getting trade stats when user has no trades."""
        response = client.get("/api/v1/trades/stats", params={"user_id": "test_user_1"})

        assert response.status_code == 200
        data = response.json()
        assert data["total_profit"] == 0
        assert data["total_trades"] == 0
