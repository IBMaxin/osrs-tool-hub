"""E2E tests for Boss endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e
class TestBossListEndpoint(BaseE2ETest):
    """Test GET /api/v1/gear/bosses endpoint."""

    def test_list_bosses(
        self,
        client: TestClient,
        session: Session,
    ):
        """Test getting list of available bosses."""
        response = client.get("/api/v1/gear/bosses")
        data = assert_successful_response(response)

        assert "bosses" in data
        assert isinstance(data["bosses"], list)
        if len(data["bosses"]) > 0:
            boss = data["bosses"][0]
            assert "name" in boss


@pytest.mark.e2e
class TestBossBiSEndpoint(BaseE2ETest):
    """Test POST /api/v1/gear/bis/{boss_name} endpoint."""

    def test_calculate_boss_bis_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test calculating BiS for a boss."""
        # Use a known boss key (not display name)
        from backend.services.gear.boss import get_available_bosses

        available_bosses = get_available_bosses()
        if not available_bosses:
            pytest.skip("No bosses available for testing")

        boss_name = available_bosses[0]  # Use the key, not the display name

        payload = {
            "budget": 100000000,
            "stats": {
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
            "ironman": False,
        }

        response = client.post(f"/api/v1/gear/bis/{boss_name}", json=payload)
        data = assert_successful_response(response)

        assert isinstance(data, dict)

    def test_calculate_boss_bis_with_constraints(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test calculating BiS with constraints."""
        # Use a known boss key (not display name)
        from backend.services.gear.boss import get_available_bosses

        available_bosses = get_available_bosses()
        if not available_bosses:
            pytest.skip("No bosses available for testing")

        boss_name = available_bosses[0]  # Use the key, not the display name

        payload = {
            "budget": 50000000,
            "stats": {
                "attack": 80,
                "strength": 80,
                "defence": 80,
                "ranged": 80,
                "magic": 80,
                "prayer": 70,
            },
            "ironman": True,
            "exclude_items": ["Twisted bow"],
            "max_tick_manipulation": False,
        }

        response = client.post(f"/api/v1/gear/bis/{boss_name}", json=payload)
        data = assert_successful_response(response)

        assert isinstance(data, dict)

    def test_calculate_boss_bis_invalid_boss(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test calculating BiS for non-existent boss."""
        payload = {
            "budget": 100000000,
            "stats": {
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        }

        response = client.post("/api/v1/gear/bis/nonexistent_boss_12345", json=payload)
        assert_error_response(response, 404)

    def test_calculate_boss_bis_invalid_budget(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test calculating BiS with invalid budget."""
        # Use a known boss key (not display name)
        from backend.services.gear.boss import get_available_bosses

        available_bosses = get_available_bosses()
        if not available_bosses:
            pytest.skip("No bosses available for testing")

        boss_name = available_bosses[0]  # Use the key, not the display name

        payload = {
            "budget": -1000,  # Invalid negative budget
            "stats": {
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        }

        response = client.post(f"/api/v1/gear/bis/{boss_name}", json=payload)
        assert_error_response(response, 422)  # Validation error

    def test_calculate_boss_bis_missing_stats(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test calculating BiS with missing stats."""
        # Use a known boss key (not display name)
        from backend.services.gear.boss import get_available_bosses

        available_bosses = get_available_bosses()
        if not available_bosses:
            pytest.skip("No bosses available for testing")

        boss_name = available_bosses[0]  # Use the key, not the display name

        payload = {
            "budget": 100000000,
            # Missing stats field
        }

        response = client.post(f"/api/v1/gear/bis/{boss_name}", json=payload)
        assert_error_response(response, 422)  # Validation error
