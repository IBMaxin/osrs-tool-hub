"""E2E tests for Watchlist endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e
class TestWatchlistCreateEndpoint(BaseE2ETest):
    """Test POST /api/v1/watchlist endpoint."""

    def test_add_to_watchlist_price_below(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test adding item to watchlist with price_below alert."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,  # Abyssal whip
            "alert_type": "price_below",
            "threshold": 1400000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        data = assert_successful_response(response, 201)

        assert data["user_id"] == "test-user-123"
        assert data["item_id"] == 4151
        assert data["item_name"] == "Abyssal whip"
        assert data["alert_type"] == "price_below"
        assert data["threshold"] == 1400000
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    def test_add_to_watchlist_price_above(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test adding item to watchlist with price_above alert."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 314,  # Feather
            "alert_type": "price_above",
            "threshold": 5,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        data = assert_successful_response(response, 201)

        assert data["alert_type"] == "price_above"
        assert data["threshold"] == 5

    def test_add_to_watchlist_margin_above(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test adding item to watchlist with margin_above alert."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,
            "alert_type": "margin_above",
            "threshold": 100000,  # 100k margin
        }

        response = client.post("/api/v1/watchlist", json=payload)
        data = assert_successful_response(response, 201)

        assert data["alert_type"] == "margin_above"
        assert data["threshold"] == 100000

    def test_add_to_watchlist_invalid_item_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test adding non-existent item to watchlist."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 999999,
            "alert_type": "price_below",
            "threshold": 1000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        assert_error_response(response, 400)

    def test_add_to_watchlist_invalid_alert_type(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test adding item with invalid alert type."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,
            "alert_type": "invalid_type",
            "threshold": 1000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        assert_error_response(response, 422)  # Validation error

    def test_add_to_watchlist_negative_threshold(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test adding item with negative threshold."""
        payload = {
            "user_id": "test-user-123",
            "item_id": 4151,
            "alert_type": "price_below",
            "threshold": -1000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        assert_error_response(response, 422)  # Validation error


@pytest.mark.e2e
class TestWatchlistGetEndpoint(BaseE2ETest):
    """Test GET /api/v1/watchlist endpoint."""

    def test_get_watchlist_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting watchlist for a user."""
        user_id = "test-user-get"
        item = sample_items[0]

        # Add item to watchlist
        payload = {
            "user_id": user_id,
            "item_id": item.id,
            "alert_type": "price_below",
            "threshold": 1000,
        }
        client.post("/api/v1/watchlist", json=payload)

        # Get watchlist
        response = client.get(f"/api/v1/watchlist?user_id={user_id}")
        data = assert_successful_response(response)

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["user_id"] == user_id
        assert data[0]["item_id"] == item.id

    def test_get_watchlist_include_inactive(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting watchlist including inactive items."""
        user_id = "test-user-inactive"
        item = sample_items[0]

        # Add item to watchlist
        payload = {
            "user_id": user_id,
            "item_id": item.id,
            "alert_type": "price_below",
            "threshold": 1000,
        }
        client.post("/api/v1/watchlist", json=payload)

        # Get watchlist with inactive
        response = client.get(f"/api/v1/watchlist?user_id={user_id}&include_inactive=true")
        data = assert_successful_response(response)

        assert isinstance(data, list)

    def test_get_watchlist_missing_user_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting watchlist without user_id parameter."""
        response = client.get("/api/v1/watchlist")
        assert_error_response(response, 422)  # Validation error


@pytest.mark.e2e
class TestWatchlistDeleteEndpoint(BaseE2ETest):
    """Test DELETE /api/v1/watchlist/{watchlist_item_id} endpoint."""

    def test_remove_from_watchlist(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test removing item from watchlist."""
        user_id = "test-user-delete"
        item = sample_items[0]

        # Add item to watchlist
        payload = {
            "user_id": user_id,
            "item_id": item.id,
            "alert_type": "price_below",
            "threshold": 1000,
        }
        create_response = client.post("/api/v1/watchlist", json=payload)
        watchlist_item_id = create_response.json()["id"]

        # Remove from watchlist
        response = client.delete(
            f"/api/v1/watchlist/{watchlist_item_id}?user_id={user_id}"
        )
        assert response.status_code == 204

        # Verify it's removed
        get_response = client.get(f"/api/v1/watchlist?user_id={user_id}")
        data = get_response.json()
        assert len(data) == 0

    def test_remove_from_watchlist_nonexistent(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test removing non-existent watchlist item."""
        response = client.delete("/api/v1/watchlist/999999?user_id=test-user")
        assert_error_response(response, 404)

    def test_remove_from_watchlist_wrong_user(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test removing watchlist item belonging to different user."""
        user_id = "test-user-owner"
        item = sample_items[0]

        # Add item to watchlist
        payload = {
            "user_id": user_id,
            "item_id": item.id,
            "alert_type": "price_below",
            "threshold": 1000,
        }
        create_response = client.post("/api/v1/watchlist", json=payload)
        watchlist_item_id = create_response.json()["id"]

        # Try to remove with different user_id
        response = client.delete(
            f"/api/v1/watchlist/{watchlist_item_id}?user_id=different-user"
        )
        # Should return 400 (item does not belong to user)
        assert_error_response(response, 400)


@pytest.mark.e2e
class TestWatchlistAlertsEndpoint(BaseE2ETest):
    """Test GET /api/v1/watchlist/alerts endpoint."""

    def test_get_alerts_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting alerts for a user."""
        user_id = "test-user-alerts"

        # Get alerts (may be empty if no alerts triggered)
        response = client.get(f"/api/v1/watchlist/alerts?user_id={user_id}")
        data = assert_successful_response(response)

        assert isinstance(data, list)

    def test_get_alerts_with_limit(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting alerts with limit parameter."""
        user_id = "test-user-alerts-limit"

        response = client.get(f"/api/v1/watchlist/alerts?user_id={user_id}&limit=10")
        data = assert_successful_response(response)

        assert isinstance(data, list)
        assert len(data) <= 10

    def test_get_alerts_missing_user_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting alerts without user_id parameter."""
        response = client.get("/api/v1/watchlist/alerts")
        assert_error_response(response, 422)  # Validation error
