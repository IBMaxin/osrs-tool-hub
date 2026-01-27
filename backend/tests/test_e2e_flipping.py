"""End-to-end tests for flipping endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot


class TestFlippingOpportunitiesEndpoint:
    """Test the /api/v1/flips/opportunities endpoint."""
    
    def test_get_opportunities_basic(self, client: TestClient, session: Session, 
                                     sample_items: list[Item], 
                                     sample_price_snapshots: list[PriceSnapshot]):
        """Test basic opportunities endpoint returns results."""
        response = client.get("/api/v1/flips/opportunities")
        
        assert response.status_code == 200
        data = response.json()
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
    
    def test_get_opportunities_with_budget_filter(self, client: TestClient, session: Session,
                                                  sample_items: list[Item],
                                                  sample_price_snapshots: list[PriceSnapshot]):
        """Test opportunities endpoint with budget filter."""
        # Test with budget that excludes expensive items
        response = client.get("/api/v1/flips/opportunities?max_budget=10000000")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should not include Twisted bow (1.55B low price)
        item_names = [flip["item_name"] for flip in data]
        assert "Twisted bow" not in item_names
        assert "Abyssal whip" in item_names
    
    def test_get_opportunities_with_roi_filter(self, client: TestClient, session: Session,
                                               sample_items: list[Item],
                                               sample_price_snapshots: list[PriceSnapshot]):
        """Test opportunities endpoint with ROI filter."""
        # Test with high ROI requirement
        response = client.get("/api/v1/flips/opportunities?min_roi=10.0")
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should have ROI >= 10%
        for flip in data:
            assert flip["roi"] >= 10.0
    
    def test_get_opportunities_with_volume_filter(self, client: TestClient, session: Session,
                                                  sample_items: list[Item],
                                                  sample_price_snapshots: list[PriceSnapshot]):
        """Test opportunities endpoint with volume filter."""
        # Test with volume requirement
        response = client.get("/api/v1/flips/opportunities?min_volume=100")
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should have volume >= 100
        for flip in data:
            assert flip["volume"] >= 100
    
    def test_get_opportunities_combined_filters(self, client: TestClient, session: Session,
                                                 sample_items: list[Item],
                                                 sample_price_snapshots: list[PriceSnapshot]):
        """Test opportunities endpoint with multiple filters."""
        response = client.get(
            "/api/v1/flips/opportunities?"
            "max_budget=100000000&"
            "min_roi=1.0&"
            "min_volume=100"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all filters are applied
        for flip in data:
            assert flip["buy_price"] <= 100000000
            assert flip["roi"] >= 1.0
            assert flip["volume"] >= 100


class TestFlippingScannerEndpoint:
    """Test the /api/v1/flipping/scanner endpoint (GE Tracker-style)."""
    
    def test_scanner_basic(self, client: TestClient, session: Session,
                           sample_items: list[Item],
                           sample_price_snapshots: list[PriceSnapshot]):
        """Test basic scanner endpoint with required parameters."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=100000000&"
            "min_roi=0.5&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
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
        assert response.status_code == 422
        
        # Missing min_roi
        response = client.get("/api/v1/flipping/scanner?budget=1000000&min_volume=10")
        assert response.status_code == 422
        
        # Missing min_volume
        response = client.get("/api/v1/flipping/scanner?budget=1000000&min_roi=1.0")
        assert response.status_code == 422
    
    def test_scanner_budget_filter(self, client: TestClient, session: Session,
                                    sample_items: list[Item],
                                    sample_price_snapshots: list[PriceSnapshot]):
        """Test scanner with budget filter."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=10000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should be within budget
        for result in data:
            assert result["buy_price"] <= 10000000
    
    def test_scanner_roi_filter(self, client: TestClient, session: Session,
                                sample_items: list[Item],
                                sample_price_snapshots: list[PriceSnapshot]):
        """Test scanner with ROI filter."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=5.0&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should meet ROI requirement
        for result in data:
            assert result["roi"] >= 5.0
    
    def test_scanner_volume_filter(self, client: TestClient, session: Session,
                                   sample_items: list[Item],
                                   sample_price_snapshots: list[PriceSnapshot]):
        """Test scanner with volume filter."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=1000"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should meet volume requirement
        for result in data:
            assert result["volume"] >= 1000
    
    def test_scanner_exclude_members(self, client: TestClient, session: Session,
                                     sample_items: list[Item],
                                     sample_price_snapshots: list[PriceSnapshot]):
        """Test scanner with exclude_members filter."""
        # First, get results with members items included
        response_with_members = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        assert response_with_members.status_code == 200
        data_with_members = response_with_members.json()
        
        # Then exclude members
        response_no_members = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=10&"
            "exclude_members=true"
        )
        assert response_no_members.status_code == 200
        data_no_members = response_no_members.json()
        
        # Results without members should be a subset or equal
        assert len(data_no_members) <= len(data_with_members)
    
    def test_scanner_margin_calculation(self, client: TestClient, session: Session,
                                        sample_items: list[Item],
                                        sample_price_snapshots: list[PriceSnapshot]):
        """Test that margin calculation is correct (2% tax)."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Find Abyssal whip in results
        whip_result = next((r for r in data if r["name"] == "Abyssal whip"), None)
        if whip_result:
            # Margin should be: (high_price - tax) - low_price
            # Tax = 1500000 * 0.02 = 30000
            # (1500000 - 30000) - 1400000 = 1470000 - 1400000 = 70000
            expected_margin = (1500000 - (1500000 * 0.02)) - 1400000
            assert abs(whip_result["margin"] - expected_margin) < 1.0  # Allow for floating point
    
    def test_scanner_roi_calculation(self, client: TestClient, session: Session,
                                      sample_items: list[Item],
                                      sample_price_snapshots: list[PriceSnapshot]):
        """Test that ROI calculation is correct."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=1000000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Find Abyssal whip in results
        whip_result = next((r for r in data if r["name"] == "Abyssal whip"), None)
        if whip_result:
            # ROI should be: margin / buy_price * 100
            expected_roi = (whip_result["margin"] / whip_result["buy_price"]) * 100
            assert abs(whip_result["roi"] - expected_roi) < 0.01  # Allow for floating point
    
    def test_scanner_sorted_by_potential_profit(self, client: TestClient, session: Session,
                                                 sample_items: list[Item],
                                                 sample_price_snapshots: list[PriceSnapshot]):
        """Test that results are sorted by potential profit (descending)."""
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=10000000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        
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
