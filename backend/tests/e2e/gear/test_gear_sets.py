"""E2E tests for Gear Set CRUD endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e
class TestGearSetEndpoints(BaseE2ETest):
    """Test gear set CRUD endpoints."""

    def test_create_gear_set(self, client: TestClient, session: Session, sample_items: list[Item]):
        """Test creating a new gear set."""
        payload = {
            "name": "Test Melee Set",
            "description": "A test melee gear set",
            "items": {
                4151: 1,  # Abyssal whip
                11802: 1,  # Saradomin godsword
            },
        }

        response = client.post("/api/v1/gear", json=payload)
        data = assert_successful_response(response, 201)

        assert data["name"] == "Test Melee Set"
        assert data["description"] == "A test melee gear set"
        # API returns string keys, convert for comparison
        response_items = {int(k): v for k, v in data["items"].items()}
        assert response_items == payload["items"]
        assert "id" in data
        assert "total_cost" in data
        assert data["total_cost"] > 0

    def test_get_all_gear_sets(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test getting all gear sets."""
        # Create gear sets
        payload1 = {"name": "Test Set 1", "items": {4151: 1}}
        client.post("/api/v1/gear", json=payload1)

        payload2 = {"name": "Test Set 2", "items": {11802: 1}}
        client.post("/api/v1/gear", json=payload2)

        # Get all
        response = client.get("/api/v1/gear")
        data = assert_successful_response(response)

        assert isinstance(data, list)
        assert len(data) >= 2

        # Verify structure
        for gear_set in data:
            assert "id" in gear_set
            assert "name" in gear_set
            assert "items" in gear_set
            assert "total_cost" in gear_set

    def test_get_gear_set_by_id(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test getting a specific gear set by ID."""
        # Create a gear set
        payload = {"name": "Test Set", "items": {4151: 1}}
        create_response = client.post("/api/v1/gear", json=payload)
        gear_set_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/api/v1/gear/{gear_set_id}")
        data = assert_successful_response(response)

        assert data["id"] == gear_set_id
        assert data["name"] == "Test Set"

    def test_get_nonexistent_gear_set(self, client: TestClient, session: Session):
        """Test getting a gear set that doesn't exist."""
        response = client.get("/api/v1/gear/99999")
        assert response.status_code == 404

    def test_delete_gear_set(self, client: TestClient, session: Session, sample_items: list[Item]):
        """Test deleting a gear set."""
        # Create a gear set
        payload = {"name": "Test Set to Delete", "items": {4151: 1}}
        create_response = client.post("/api/v1/gear", json=payload)
        gear_set_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/v1/gear/{gear_set_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_response = client.get(f"/api/v1/gear/{gear_set_id}")
        assert get_response.status_code == 404

    def test_gear_set_total_cost_calculation(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test that gear set total cost is calculated correctly."""
        payload = {
            "name": "Cost Test Set",
            "items": {
                4151: 1,  # Abyssal whip: 1,400,000
                11802: 1,  # SGS: 50,000,000
            },
        }

        response = client.post("/api/v1/gear", json=payload)
        data = assert_successful_response(response, 201)

        # Total should be sum of item prices
        expected_cost = 1_400_000 + 50_000_000
        assert data["total_cost"] == expected_cost
