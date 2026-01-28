"""Tests for watchlist API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import WatchlistItem, WatchlistAlert, Item


class TestWatchlistEndpoints:
    """Test watchlist API endpoints."""

    def test_add_to_watchlist_success(self, client: TestClient, session: Session):
        """Test adding item to watchlist."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        payload = {
            "user_id": "test_user_1",
            "item_id": 4151,
            "alert_type": "price_below",
            "threshold": 1500000,
        }

        response = client.post("/api/v1/watchlist", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == "test_user_1"
        assert data["item_id"] == 4151
        assert data["alert_type"] == "price_below"
        assert data["threshold"] == 1500000

    def test_add_to_watchlist_invalid_alert_type(self, client: TestClient, session: Session):
        """Test adding to watchlist with invalid alert type."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        payload = {
            "user_id": "test_user_1",
            "item_id": 4151,
            "alert_type": "invalid_type",
            "threshold": 1500000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        assert response.status_code == 422  # Validation error

    def test_add_to_watchlist_item_not_found(self, client: TestClient):
        """Test adding non-existent item to watchlist."""
        payload = {
            "user_id": "test_user_1",
            "item_id": 99999,
            "alert_type": "price_below",
            "threshold": 1500000,
        }

        response = client.post("/api/v1/watchlist", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_get_watchlist_success(self, client: TestClient, session: Session):
        """Test getting user's watchlist."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        watchlist_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        session.add(watchlist_item)
        session.commit()

        response = client.get("/api/v1/watchlist", params={"user_id": "test_user_1"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["user_id"] == "test_user_1"

    def test_get_watchlist_include_inactive(self, client: TestClient, session: Session):
        """Test getting watchlist including inactive items."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        active_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        inactive_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_above",
            threshold=2000000,
            is_active=False,
        )
        session.add(active_item)
        session.add(inactive_item)
        session.commit()

        response = client.get(
            "/api/v1/watchlist",
            params={"user_id": "test_user_1", "include_inactive": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_remove_from_watchlist_success(self, client: TestClient, session: Session):
        """Test removing item from watchlist."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        watchlist_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        session.add(watchlist_item)
        session.commit()

        response = client.delete(
            f"/api/v1/watchlist/{watchlist_item.id}",
            params={"user_id": "test_user_1"},
        )

        assert response.status_code == 204

    def test_remove_from_watchlist_not_found(self, client: TestClient):
        """Test removing non-existent watchlist item."""
        response = client.delete(
            "/api/v1/watchlist/99999",
            params={"user_id": "test_user_1"},
        )

        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_remove_from_watchlist_wrong_user(self, client: TestClient, session: Session):
        """Test removing watchlist item belonging to different user."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        watchlist_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        session.add(watchlist_item)
        session.commit()

        response = client.delete(
            f"/api/v1/watchlist/{watchlist_item.id}",
            params={"user_id": "test_user_2"},
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_get_alerts_success(self, client: TestClient, session: Session):
        """Test getting user's alerts."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        watchlist_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        session.add(watchlist_item)
        session.commit()

        alert = WatchlistAlert(
            watchlist_item_id=watchlist_item.id,
            current_value=1400000,
            threshold_value=1500000,
            message="Price dropped",
        )
        session.add(alert)
        session.commit()

        response = client.get("/api/v1/watchlist/alerts", params={"user_id": "test_user_1"})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    def test_get_alerts_with_limit(self, client: TestClient, session: Session):
        """Test getting alerts with limit."""
        item = Item(id=4151, name="Abyssal whip", members=True, value=2000000)
        session.add(item)
        session.commit()

        watchlist_item = WatchlistItem(
            user_id="test_user_1",
            item_id=4151,
            item_name="Abyssal whip",
            alert_type="price_below",
            threshold=1500000,
            is_active=True,
        )
        session.add(watchlist_item)
        session.commit()

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

        response = client.get(
            "/api/v1/watchlist/alerts",
            params={"user_id": "test_user_1", "limit": 5},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_alerts_invalid_limit(self, client: TestClient):
        """Test getting alerts with invalid limit."""
        response = client.get(
            "/api/v1/watchlist/alerts",
            params={"user_id": "test_user_1", "limit": 0},
        )

        assert response.status_code == 422  # Validation error
