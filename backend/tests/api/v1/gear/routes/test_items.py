"""Tests for item lookup endpoints."""

from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlmodel import Session


class TestGetItem:
    """Test get_item endpoint."""

    def test_get_item_success(self, client: TestClient, session: Session, sample_items):
        """Test successful item retrieval."""
        item = sample_items[0]

        with patch("backend.api.v1.gear.routes.items.get_item_price", return_value=1500000):
            response = client.get(f"/api/v1/gear/items/{item.id}")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == item.id
            assert data["name"] == item.name
            assert data["price"] == 1500000
            assert "stats" in data
            assert "requirements" in data

    def test_get_item_not_found(self, client: TestClient, session: Session):
        """Test item retrieval with non-existent ID."""
        response = client.get("/api/v1/gear/items/99999")

        assert response.status_code == 404
        assert "not found" in response.json()["error"]["message"].lower()

    def test_get_item_includes_all_stats(self, client: TestClient, session: Session, sample_items):
        """Test get_item includes all stat fields."""
        item = sample_items[0]

        with patch("backend.api.v1.gear.routes.items.get_item_price", return_value=1500000):
            response = client.get(f"/api/v1/gear/items/{item.id}")

            assert response.status_code == 200
            data = response.json()
            stats = data["stats"]
            assert "attack_stab" in stats
            assert "attack_slash" in stats
            assert "attack_crush" in stats
            assert "attack_magic" in stats
            assert "attack_ranged" in stats
            assert "melee_strength" in stats
            assert "ranged_strength" in stats
            assert "magic_damage" in stats
            assert "prayer_bonus" in stats
            assert "defence_stab" in stats
            assert "defence_slash" in stats
            assert "defence_crush" in stats
            assert "defence_magic" in stats
            assert "defence_ranged" in stats

    def test_get_item_includes_all_requirements(
        self, client: TestClient, session: Session, sample_items
    ):
        """Test get_item includes all requirement fields."""
        item = sample_items[0]

        with patch("backend.api.v1.gear.routes.items.get_item_price", return_value=1500000):
            response = client.get(f"/api/v1/gear/items/{item.id}")

            assert response.status_code == 200
            data = response.json()
            requirements = data["requirements"]
            assert "attack" in requirements
            assert "strength" in requirements
            assert "defence" in requirements
            assert "ranged" in requirements
            assert "magic" in requirements
            assert "prayer" in requirements
            assert "quest" in requirements
            assert "achievement" in requirements

    def test_get_item_uses_price_from_snapshot(
        self, client: TestClient, session: Session, sample_items
    ):
        """Test get_item uses price from PriceSnapshot."""
        item = sample_items[0]

        with patch("backend.api.v1.gear.routes.items.get_item_price", return_value=1500000):
            response = client.get(f"/api/v1/gear/items/{item.id}")

            assert response.status_code == 200
            data = response.json()
            assert data["price"] == 1500000

    def test_get_item_handles_missing_price(
        self, client: TestClient, session: Session, sample_items
    ):
        """Test get_item handles missing price gracefully."""
        item = sample_items[0]

        with patch("backend.api.v1.gear.routes.items.get_item_price", return_value=0):
            response = client.get(f"/api/v1/gear/items/{item.id}")

            assert response.status_code == 200
            data = response.json()
            assert data["price"] == 0
