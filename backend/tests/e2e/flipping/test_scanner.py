"""E2E tests for Flipping Scanner endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e
class TestFlippingScannerEndpoint(BaseE2ETest):
    """Test the /api/v1/flipping/scanner endpoint (GE Tracker-style)."""

    def test_scanner_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test basic scanner endpoint with required parameters."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=100000000&" "min_roi=0.5&" "min_volume=10"
        )
        data = assert_successful_response(response)

        assert isinstance(data, list)

        # Check response structure matches FlipOpportunity model
        if len(data) > 0:
            first_result = data[0]
            assert "item_id" in first_result
            assert "name" in first_result
            assert "buy_price" in first_result
            assert "sell_price" in first_result
            assert "margin" in first_result
            assert "roi" in first_result
            assert "volume" in first_result
            assert "wiki_url" in first_result

    def test_scanner_missing_required_params(self, client: TestClient, session: Session):
        """Test scanner endpoint with missing required parameters."""
        # Missing budget
        response = client.get("/api/v1/flipping/scanner?min_roi=1.0&min_volume=10")
        assert_error_response(response, 422)

        # Missing min_roi
        response = client.get("/api/v1/flipping/scanner?budget=1000000&min_volume=10")
        assert_error_response(response, 422)

        # Missing min_volume
        response = client.get("/api/v1/flipping/scanner?budget=1000000&min_roi=1.0")
        assert_error_response(response, 422)

    def test_scanner_budget_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test scanner with budget filter."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=10000000&" "min_roi=0.1&" "min_volume=10"
        )
        data = assert_successful_response(response)

        # All results should be within budget
        for result in data:
            assert result["buy_price"] <= 10000000

    def test_scanner_roi_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test scanner with ROI filter."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=1000000000&" "min_roi=5.0&" "min_volume=10"
        )
        data = assert_successful_response(response)

        # All results should meet ROI requirement
        for result in data:
            assert result["roi"] >= 5.0

    def test_scanner_volume_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test scanner with volume filter."""
        response = client.get(
            "/api/v1/flipping/scanner?" "budget=1000000000&" "min_roi=0.1&" "min_volume=1000"
        )
        data = assert_successful_response(response)

        # All results should meet volume requirement
        for result in data:
            assert result["volume"] >= 1000

    def test_scanner_exclude_members(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test scanner with exclude_members filter."""
        # First, get results with members items included
        response_with_members = client.get(
            "/api/v1/flipping/scanner?" "budget=1000000000&" "min_roi=0.1&" "min_volume=10"
        )
        data_with_members = assert_successful_response(response_with_members)

        # Then exclude members
        response_no_members = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=10&"
            "exclude_members=true"
        )
        data_no_members = assert_successful_response(response_no_members)

        # Results without members should be a subset or equal
        assert len(data_no_members) <= len(data_with_members)
