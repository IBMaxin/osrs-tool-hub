"""E2E tests for Items endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e
class TestItemsGetEndpoint(BaseE2ETest):
    """Test GET /api/v1/gear/items/{item_id} endpoint."""

    def test_get_item_by_id(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting item details by ID."""
        item = sample_items[0]

        response = client.get(f"/api/v1/gear/items/{item.id}")
        data = assert_successful_response(response)

        assert data["id"] == item.id
        assert data["name"] == item.name
        assert "price" in data
        assert "icon_url" in data
        assert "members" in data
        assert "stats" in data
        assert isinstance(data["stats"], dict)
        assert "requirements" in data
        assert isinstance(data["requirements"], dict)

    def test_get_item_verify_stats_structure(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test that item stats structure is correct."""
        item = sample_items[0]

        response = client.get(f"/api/v1/gear/items/{item.id}")
        data = assert_successful_response(response)

        stats = data["stats"]
        # Check combat stats are present
        assert "attack_stab" in stats
        assert "attack_slash" in stats
        assert "attack_crush" in stats
        assert "attack_magic" in stats
        assert "attack_ranged" in stats
        assert "melee_strength" in stats
        assert "ranged_strength" in stats
        assert "magic_damage" in stats
        assert "defence_stab" in stats
        assert "defence_slash" in stats
        assert "defence_crush" in stats
        assert "defence_magic" in stats
        assert "defence_ranged" in stats

    def test_get_item_verify_requirements_structure(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test that item requirements structure is correct."""
        item = sample_items[0]

        response = client.get(f"/api/v1/gear/items/{item.id}")
        data = assert_successful_response(response)

        requirements = data["requirements"]
        assert "attack" in requirements
        assert "strength" in requirements
        assert "defence" in requirements
        assert "ranged" in requirements
        assert "magic" in requirements
        assert "prayer" in requirements
        assert "quest" in requirements
        assert "achievement" in requirements

    def test_get_item_nonexistent(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting non-existent item."""
        response = client.get("/api/v1/gear/items/999999")
        assert_error_response(response, 404)

    def test_get_item_invalid_id(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting item with invalid ID format."""
        response = client.get("/api/v1/gear/items/invalid")
        assert_error_response(response, 422)  # Validation error
