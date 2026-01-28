"""E2E tests for Flipping calculation accuracy."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e
class TestFlippingCalculations(BaseE2ETest):
    """Test flipping calculation accuracy."""

    def test_scanner_margin_calculation(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test that margin calculation is correct (2% tax)."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=1000000000&" "min_roi=0.1&" "min_volume=10"
        )
        data = assert_successful_response(response)

        # Find Abyssal whip in results
        whip_result = next((r for r in data if r["name"] == "Abyssal whip"), None)
        if whip_result:
            # Margin should be: (high_price - tax) - low_price
            # Tax = 1500000 * 0.02 = 30000
            # (1500000 - 30000) - 1400000 = 1470000 - 1400000 = 70000
            expected_margin = (1500000 - (1500000 * 0.02)) - 1400000
            assert abs(whip_result["margin"] - expected_margin) < 1.0

    def test_scanner_roi_calculation(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test that ROI calculation is correct."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=1000000000&" "min_roi=0.1&" "min_volume=10"
        )
        data = assert_successful_response(response)

        # Find Abyssal whip in results
        whip_result = next((r for r in data if r["name"] == "Abyssal whip"), None)
        if whip_result:
            # ROI should be: margin / buy_price * 100
            expected_roi = (whip_result["margin"] / whip_result["buy_price"]) * 100
            assert abs(whip_result["roi"] - expected_roi) < 0.01

    def test_scanner_sorted_by_potential_profit(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test that results are sorted by potential profit (descending)."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=10000000000&" "min_roi=0.1&" "min_volume=10"
        )
        data = assert_successful_response(response)

        if len(data) > 1:
            # Calculate potential profit for each (margin * min(buy_limit, volume))
            profits = []
            for result in data:
                # We need to get buy_limit from the item
                item = session.get(Item, result["item_id"])
                buy_limit = item.limit if item else 0
                potential_profit = result["margin"] * min(buy_limit, result["volume"])
                profits.append(potential_profit)

            # Verify descending order
            assert profits == sorted(profits, reverse=True)
