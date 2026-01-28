"""E2E tests for Gear Suggestions endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e
class TestGearSuggestionsEndpoint(BaseE2ETest):
    """Test gear suggestion endpoints."""

    def test_get_gear_suggestions(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test getting gear suggestions for a slot."""
        response = client.get(
            "/api/v1/gear/suggestions?" "slot=weapon&" "style=melee&" "defence_level=99"
        )

        data = assert_successful_response(response)
        assert isinstance(data, list)

    def test_get_gear_suggestions_with_budget(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test gear suggestions with budget filter."""
        response = client.get(
            "/api/v1/gear/suggestions?"
            "slot=weapon&"
            "style=melee&"
            "defence_level=99&"
            "budget=10000000"
        )

        data = assert_successful_response(response)

        # All suggestions should be within budget
        for suggestion in data:
            if "price" in suggestion:
                assert suggestion["price"] <= 10000000

    def test_suggestions_different_slots(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test suggestions for different equipment slots."""
        slots = ["weapon", "head", "body", "legs"]

        for slot in slots:
            response = client.get(
                f"/api/v1/gear/suggestions?" f"slot={slot}&" "style=melee&" "defence_level=99"
            )
            data = assert_successful_response(response)
            assert isinstance(data, list)
