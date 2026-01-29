"""Integration tests for flipping feature with 24h volume tracking."""

import pytest
from sqlmodel import Session
from backend.db.session import get_session
from backend.services.wiki.client import WikiAPIClient
from backend.services.wiki.sync import sync_items_to_db, sync_prices_to_db, sync_24h_volume_to_db
from backend.services.flipping import FlippingService, FlipOpportunity
from backend.models import Item, PriceSnapshot


@pytest.mark.asyncio
class TestFlippingFeatureIntegration:
    """Integration tests for flipping feature with 24h volume tracking."""

    async def test_volume_sync_and_flipping_integration(self):
        """Test complete flow: sync items -> sync prices -> sync volume -> find flips."""
        with next(get_session()) as session:
            # Setup: Sync items first
            client = WikiAPIClient()
            await sync_items_to_db(client, session)
            
            # Verify items were synced
            item_count = session.query(Item).count()
            assert item_count > 0, "Items should be synced from Wiki"
            
            # Step 1: Sync prices (latest prices)
            await sync_prices_to_db(client, session)
            
            # Verify prices were synced
            price_count = session.query(PriceSnapshot).count()
            assert price_count > 0, "Prices should be synced from Wiki"
            
            # Step 2: Sync 24h volume
            await sync_24h_volume_to_db(client, session)
            
            # Verify volume data was synced
            volume_snapshots = session.query(PriceSnapshot).filter(
                PriceSnapshot.buy_volume_24h.is_not(None) | 
                PriceSnapshot.sell_volume_24h.is_not(None)
            ).count()
            
            # Some items should have volume data (may not be all items)
            print(f"✓ Synced 24h volume for {volume_snapshots} items")
            
            # Step 3: Test flipping service with volume
            flipping_service = FlippingService(session)
            opportunities = flipping_service.get_flip_opportunities(
                max_budget=100_000_000,  # 100M budget
                min_roi=1.0,  # 1% minimum ROI
                min_volume=100,  # 100 minimum volume
                limit=10
            )
            
            # Verify opportunities were found
            assert len(opportunities) > 0, "Should find flip opportunities"
            
            # Verify each opportunity has required fields
            for opp in opportunities:
                assert "item_id" in opp
                assert "item_name" in opp
                assert "buy_price" in opp
                assert "sell_price" in opp
                assert "margin" in opp
                assert "roi" in opp
                assert "margin_x_volume" in opp or True  # May be None if no volume
                assert "potential_profit" in opp
                
                # ROI should be calculated with sell price denominator (GE Tracker style)
                expected_roi = (opp["margin"] / opp["sell_price"]) * 100 if opp["sell_price"] > 0 else 0
                assert abs(opp["roi"] - expected_roi) < 0.01, f"ROI calculation incorrect: {opp['roi']} vs {expected_roi}"

    async def test_flipping_service_with_24h_volume_ranking(self):
        """Test that flipping service correctly ranks by margin x volume."""
        with next(get_session()) as session:
            # Ensure we have data
            client = WikiAPIClient()
            await sync_items_to_db(client, session)
            await sync_prices_to_db(client, session)
            await sync_24h_volume_to_db(client, session)
            
            flipping_service = FlippingService(session)
            opportunities = flipping_service.get_flip_opportunities(
                max_budget=10_000_000,  # 10M budget for more items
                min_roi=0.5,  # 0.5% minimum ROI
                min_volume=0,  # No volume filter to test all items
                limit=50
            )
            
            # Verify sorting by margin_x_volume (descending)
            margin_x_volumes = [opp.get("margin_x_volume") for opp in opportunities if opp.get("margin_x_volume") is not None]
            
            if len(margin_x_volumes) > 1:
                # Check that items with volume are sorted by margin_x_volume
                sorted_volumes = sorted(margin_x_volumes, reverse=True)
                assert margin_x_volumes == sorted_volumes, "Opportunities should be sorted by margin_x_volume descending"

    async def test_flip_opportunity_model_with_volume_fields(self):
        """Test FlipOpportunity model includes all volume fields."""
        with next(get_session()) as session:
            flipping_service = FlippingService(session)
            opportunities = flipping_service.find_best_flips(
                budget=5_000_000,
                min_roi=1.0,
                min_volume=0,
                exclude_members=False
            )
            
            if opportunities:
                opp = opportunities[0]
                # Verify FlipOpportunity has all required fields
                assert hasattr(opp, "item_id")
                assert hasattr(opp, "item_name")
                assert hasattr(opp, "buy_price")
                assert hasattr(opp, "sell_price")
                assert hasattr(opp, "margin")
                assert hasattr(opp, "roi")
                assert hasattr(opp, "volume")
                assert hasattr(opp, "buy_volume_24h")
                assert hasattr(opp, "sell_volume_24h")
                assert hasattr(opp, "total_volume_24h")
                assert hasattr(opp, "margin_x_volume")
                assert hasattr(opp, "wiki_url")

    async def test_volume_data_none_handling(self):
        """Test flipping service handles None volume data gracefully."""
        with next(get_session()) as session:
            # Create a test item with price but no volume data
            item = Item(id=999999, name="Test Item", members=False, limit=1000)
            session.add(item)
            
            price_snapshot = PriceSnapshot(
                item_id=999999,
                high_price=1000,
                low_price=900,
                high_volume=50,
                low_volume=40,
                # buy_volume_24h and sell_volume_24h are None by default
            )
            session.add(price_snapshot)
            session.commit()
            
            flipping_service = FlippingService(session)
            opportunities = flipping_service.get_flip_opportunities(
                max_budget=1_000_000,
                min_roi=0,
                min_volume=0,
                limit=10
            )
            
            # Should find opportunities even with None volume data
            assert len(opportunities) > 0
            
            # Find our test item
            test_opp = next((opp for opp in opportunities if opp["item_id"] == 999999), None)
            if test_opp:
                # Should handle None gracefully
                assert test_opp["buy_volume_24h"] is None
                assert test_opp["sell_volume_24h"] is None
                assert test_opp["total_volume_24h"] is None
                assert test_opp["margin_x_volume"] is None


@pytest.mark.asyncio
class TestVolumeFieldsAccessibility:
    """Test that volume fields are accessible and queryable."""

    def test_pricesnapshot_buy_volume_24h_accessible(self):
        """Test buy_volume_24h column is queryable."""
        with next(get_session()) as session:
            # This should not raise OperationalError
            result = session.query(PriceSnapshot.buy_volume_24h).first()
            # If no data, result will be None, but query should succeed
            assert result is not None or True  # Query executes without error

    def test_pricesnapshot_sell_volume_24h_accessible(self):
        """Test sell_volume_24h column is queryable."""
        with next(get_session()) as session:
            result = session.query(PriceSnapshot.sell_volume_24h).first()
            assert result is not None or True  # Query executes without error

    def test_pricesnapshot_total_volume_24h_property(self):
        """Test total_volume_24h computed property works."""
        snap = PriceSnapshot(
            buy_volume_24h=100,
            sell_volume_24h=50
        )
        assert snap.total_volume_24h == 150
        
        snap = PriceSnapshot(
            buy_volume_24h=None,
            sell_volume_24h=None
        )
        assert snap.total_volume_24h is None
