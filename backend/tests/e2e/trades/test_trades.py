"""E2E tests for Trades endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e
class TestTradesCreateEndpoint(BaseE2ETest):
    """Test POST /api/v1/trades endpoint."""

    def test_create_trade_bought(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test creating a trade with 'bought' status."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,  # Abyssal whip
            "buy_price": 1500000,
            "quantity": 1,
            "status": "bought",
        }

        response = client.post("/api/v1/trades", json=payload)
        data = assert_successful_response(response, 201)

        assert data["user_id"] == "test-user-123"
        assert data["item_id"] == 4151
        assert data["item_name"] == "Abyssal whip"
        assert data["buy_price"] == 1500000
        assert data["quantity"] == 1
        assert data["status"] == "bought"
        assert data["sell_price"] is None
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_trade_sold(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test creating a trade with 'sold' status."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 314,  # Feather
            "buy_price": 3,
            "quantity": 1000,
            "sell_price": 4,
            "status": "sold",
        }

        response = client.post("/api/v1/trades", json=payload)
        data = assert_successful_response(response, 201)

        assert data["status"] == "sold"
        assert data["sell_price"] == 4
        assert data["profit"] == 1000  # (4 - 3) * 1000

    def test_create_trade_invalid_item_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test creating a trade with non-existent item ID."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 999999,
            "buy_price": 1000,
            "quantity": 1,
        }

        response = client.post("/api/v1/trades", json=payload)
        assert_error_response(response, 400)

    def test_create_trade_invalid_status(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test creating a trade with invalid status."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,
            "buy_price": 1500000,
            "quantity": 1,
            "status": "invalid_status",
        }

        response = client.post("/api/v1/trades", json=payload)
        assert_error_response(response, 422)  # Validation error

    def test_create_trade_negative_price(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test creating a trade with negative price."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,
            "buy_price": -1000,
            "quantity": 1,
        }

        response = client.post("/api/v1/trades", json=payload)
        assert_error_response(response, 422)  # Validation error


@pytest.mark.e2e
class TestTradesGetEndpoint(BaseE2ETest):
    """Test GET /api/v1/trades endpoint."""

    def test_get_trades_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trades for a user."""
        # Create some trades first
        user_id = "test-user-456"
        for i, item in enumerate(sample_items[:2]):
            payload = {
                "user_id": user_id,
                "item_id": item.id,
                "buy_price": 1000 * (i + 1),
                "quantity": 1,
            }
            client.post("/api/v1/trades", json=payload)

        # Get trades
        response = client.get(f"/api/v1/trades?user_id={user_id}")
        data = assert_successful_response(response)

        assert isinstance(data, list)
        assert len(data) == 2
        assert all(trade["user_id"] == user_id for trade in data)

    def test_get_trades_with_status_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trades filtered by status."""
        user_id = "test-user-status"
        item = sample_items[0]

        # Create bought trade
        payload_bought = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1000,
            "quantity": 1,
            "status": "bought",
        }
        client.post("/api/v1/trades", json=payload_bought)

        # Create sold trade
        payload_sold = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1000,
            "quantity": 1,
            "sell_price": 1100,
            "status": "sold",
        }
        client.post("/api/v1/trades", json=payload_sold)

        # Get only bought trades
        response = client.get(f"/api/v1/trades?user_id={user_id}&status=bought")
        data = assert_successful_response(response)

        assert len(data) == 1
        assert data[0]["status"] == "bought"

    def test_get_trades_with_item_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trades filtered by item_id."""
        user_id = "test-user-item"
        item_id = sample_items[0].id

        # Create trade for specific item
        payload = {
            "user_id": user_id,
            "item_id": item_id,
            "buy_price": 1000,
            "quantity": 1,
        }
        client.post("/api/v1/trades", json=payload)

        # Get trades for that item
        response = client.get(f"/api/v1/trades?user_id={user_id}&item_id={item_id}")
        data = assert_successful_response(response)

        assert len(data) == 1
        assert data[0]["item_id"] == item_id

    def test_get_trades_with_limit(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trades with limit parameter."""
        user_id = "test-user-limit"
        item = sample_items[0]

        # Create multiple trades
        for i in range(5):
            payload = {
                "user_id": user_id,
                "item_id": item.id,
                "buy_price": 1000 + i,
                "quantity": 1,
            }
            client.post("/api/v1/trades", json=payload)

        # Get trades with limit
        response = client.get(f"/api/v1/trades?user_id={user_id}&limit=3")
        data = assert_successful_response(response)

        assert len(data) == 3

    def test_get_trades_missing_user_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting trades without user_id parameter."""
        response = client.get("/api/v1/trades")
        assert_error_response(response, 422)  # Validation error


@pytest.mark.e2e
class TestTradesStatsEndpoint(BaseE2ETest):
    """Test GET /api/v1/trades/stats endpoint."""

    def test_get_trade_stats_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trade statistics."""
        user_id = "test-user-stats"
        item = sample_items[0]

        # Create some trades
        payload1 = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1000,
            "quantity": 10,
            "sell_price": 1100,
            "status": "sold",
        }
        client.post("/api/v1/trades", json=payload1)

        payload2 = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1000,
            "quantity": 5,
            "status": "bought",
        }
        client.post("/api/v1/trades", json=payload2)

        # Get stats
        response = client.get(f"/api/v1/trades/stats?user_id={user_id}")
        data = assert_successful_response(response)

        assert "total_profit" in data
        assert "total_trades" in data
        assert "sold_trades" in data
        assert "profit_per_hour" in data
        assert "best_items" in data
        assert "profit_by_item" in data
        assert data["total_trades"] == 2
        assert data["sold_trades"] == 1
        # Profit = (sell_price - buy_price) * quantity - tax
        # Tax = sell_price * 0.02 * quantity = 1100 * 0.02 * 10 = 220
        # Profit = (1100 - 1000) * 10 - 220 = 780
        assert data["total_profit"] == 780

    def test_get_trade_stats_with_days_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting trade statistics with days filter."""
        user_id = "test-user-days"
        item = sample_items[0]

        # Create a trade
        payload = {
            "user_id": user_id,
            "item_id": item.id,
            "buy_price": 1000,
            "quantity": 1,
            "sell_price": 1100,
            "status": "sold",
        }
        client.post("/api/v1/trades", json=payload)

        # Get stats with days filter
        response = client.get(f"/api/v1/trades/stats?user_id={user_id}&days=30")
        data = assert_successful_response(response)

        assert "total_profit" in data
        assert "total_trades" in data

    def test_get_trade_stats_missing_user_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting trade stats without user_id parameter."""
        response = client.get("/api/v1/trades/stats")
        assert_error_response(response, 422)  # Validation error
