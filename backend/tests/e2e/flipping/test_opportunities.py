"""E2E tests for Flipping Opportunities endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e


class TestFlippingOpportunitiesEndpoint(BaseE2ETest):
    """Test the /api/v1/flips/opportunities endpoint."""
    
    def test_get_opportunities_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test basic opportunities endpoint returns results."""
        response = client.get("/api/v1/flips/opportunities")
        data = assert_successful_response(response)
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check structure of first result
        first_flip = data[0]
        assert "item_id" in first_flip
        assert "item_name" in first_flip
        assert "buy_price" in first_flip
        assert "sell_price" in first_flip
        assert "margin" in first_flip
        assert "roi" in first_flip
        assert "potential_profit" in first_flip
    
    def test_get_opportunities_with_budget_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test opportunities endpoint with budget filter."""
        response = client.get("/api/v1/flips/opportunities?max_budget=10000000")
        data = assert_successful_response(response)
        
        # Should not include Twisted bow (1.55B low price)
        item_names = [flip["item_name"] for flip in data]
        assert "Twisted bow" not in item_names
        assert "Abyssal whip" in item_names
    
    def test_get_opportunities_with_roi_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test opportunities endpoint with ROI filter."""
        response = client.get("/api/v1/flips/opportunities?min_roi=10.0")
        data = assert_successful_response(response)
        
        # All results should have ROI >= 10%
        for flip in data:
            assert flip["roi"] >= 10.0
    
    def test_get_opportunities_with_volume_filter(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test opportunities endpoint with volume filter."""
        response = client.get("/api/v1/flips/opportunities?min_volume=100")
        data = assert_successful_response(response)
        
        # All results should have volume >= 100
        for flip in data:
            assert flip["volume"] >= 100
    
    def test_get_opportunities_combined_filters(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot]
    ):
        """Test opportunities endpoint with multiple filters."""
        response = client.get(
            "/api/v1/flips/opportunities?"
            "max_budget=100000000&"
            "min_roi=1.0&"
            "min_volume=100"
        )
        data = assert_successful_response(response)
        
        # Verify all filters are applied
        for flip in data:
            assert flip["buy_price"] <= 100000000
            assert flip["roi"] >= 1.0
            assert flip["volume"] >= 100
