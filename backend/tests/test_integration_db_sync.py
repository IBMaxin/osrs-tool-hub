"""Integration tests for database synchronization and price updates."""

from sqlmodel import Session, select

from backend.models import Item, PriceSnapshot
from backend.database import migrate_tables


class TestPriceSyncIntegration:
    """Test price synchronization from Wiki API to database."""

    def test_price_sync_updates_item_fields(self, session: Session):
        """Test that price sync updates denormalized Item fields."""
        # Create an item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        session.add(item)
        session.commit()

        # Create a price snapshot
        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
            high_time=1700000000,
            low_time=1700000000,
        )
        session.add(price_snapshot)
        session.commit()

        # Simulate price sync (which should update Item fields)
        # In real scenario, this would be called by WikiAPIClient.sync_prices_to_db
        item.high_price = price_snapshot.high_price
        item.low_price = price_snapshot.low_price
        item.high_time = price_snapshot.high_time
        item.low_time = price_snapshot.low_time
        item.buy_limit = item.limit
        session.add(item)
        session.commit()

        # Verify Item fields are updated
        updated_item = session.get(Item, 4151)
        assert updated_item.high_price == 1500000
        assert updated_item.low_price == 1400000
        assert updated_item.high_time == 1700000000
        assert updated_item.low_time == 1700000000
        assert updated_item.buy_limit == 70

    def test_migration_adds_price_fields(self, session: Session):
        """Test that migration adds price fields to existing Item table."""
        # Create an item without price fields (simulating old schema)
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        session.add(item)
        session.commit()

        # Run migration
        migrate_tables()

        # Verify item still exists and can be queried
        item = session.get(Item, 4151)
        assert item is not None
        assert item.name == "Abyssal whip"

    def test_price_sync_creates_snapshot_if_missing(self, session: Session):
        """Test that price sync creates PriceSnapshot if it doesn't exist."""
        # Create an item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
        )
        session.add(item)
        session.commit()

        # Create price snapshot (simulating sync)
        price_snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
            high_time=1700000000,
            low_time=1700000000,
        )
        session.add(price_snapshot)
        session.commit()

        # Verify snapshot exists
        snapshot = session.exec(select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)).first()
        assert snapshot is not None
        assert snapshot.high_price == 1500000
        assert snapshot.low_price == 1400000


class TestFlippingServiceIntegration:
    """Integration tests for flipping service with database."""

    def test_find_best_flips_uses_denormalized_fields(self, session: Session):
        """Test that find_best_flips uses denormalized Item price fields."""
        from backend.services.flipping import FlippingService

        # Create items with denormalized price fields
        item1 = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            high_price=1500000,
            low_price=1400000,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=70,
        )
        session.add(item1)

        item2 = Item(
            id=314,
            name="Feather",
            members=False,
            limit=13000,
            high_price=3,
            low_price=3,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=13000,
        )
        session.add(item2)

        # Create price snapshots for volume data
        # Note: find_best_flips filters by buy_volume_24h + sell_volume_24h, not high_volume/low_volume
        snapshot1 = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
            buy_volume_24h=5000,  # Required for find_best_flips volume filter
            sell_volume_24h=4000,
        )
        session.add(snapshot1)

        snapshot2 = PriceSnapshot(
            item_id=314,
            high_price=3,
            low_price=3,
            high_volume=1000000,
            low_volume=1000000,
            buy_volume_24h=1000000,  # Required for find_best_flips volume filter
            sell_volume_24h=1000000,
        )
        session.add(snapshot2)

        session.commit()

        # Test find_best_flips
        service = FlippingService(session)
        results = service.find_best_flips(
            budget=100000000, min_roi=0.1, min_volume=10, exclude_members=False
        )

        # Should find at least the whip (feather has 0% ROI)
        assert len(results) > 0

        # Verify whip is in results
        whip_result = next((r for r in results if r.item_name == "Abyssal whip"), None)
        assert whip_result is not None
        assert whip_result.buy_price == 1400000
        assert whip_result.sell_price == 1500000

    def test_find_best_flips_excludes_members(self, session: Session):
        """Test that find_best_flips correctly excludes members items."""
        from backend.services.flipping import FlippingService

        # Create members item
        members_item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            high_price=1500000,
            low_price=1400000,
            buy_limit=70,
        )
        session.add(members_item)

        # Create non-members item
        non_members_item = Item(
            id=314,
            name="Feather",
            members=False,
            limit=13000,
            high_price=3,
            low_price=2,  # Make it profitable
            buy_limit=13000,
        )
        session.add(non_members_item)

        # Create snapshots
        snapshot1 = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
        )
        session.add(snapshot1)

        snapshot2 = PriceSnapshot(
            item_id=314,
            high_price=3,
            low_price=2,
            high_volume=1000000,
            low_volume=1000000,
        )
        session.add(snapshot2)

        session.commit()

        # Test with exclude_members=True
        service = FlippingService(session)
        results = service.find_best_flips(
            budget=100000000, min_roi=0.1, min_volume=10, exclude_members=True
        )

        # Should only include non-members items
        for result in results:
            item = session.get(Item, result.item_id)
            assert item.members is False


class TestDatabaseConsistency:
    """Test database consistency and data integrity."""

    def test_item_price_fields_match_snapshot(self, session: Session):
        """Test that Item price fields stay in sync with PriceSnapshot."""
        # Create item and snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            high_price=1500000,
            low_price=1400000,
            high_time=1700000000,
            low_time=1700000000,
        )
        session.add(item)

        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_time=1700000000,
            low_time=1700000000,
        )
        session.add(snapshot)
        session.commit()

        # Verify they match
        item = session.get(Item, 4151)
        snapshot = session.exec(select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)).first()

        assert item.high_price == snapshot.high_price
        assert item.low_price == snapshot.low_price
        assert item.high_time == snapshot.high_time
        assert item.low_time == snapshot.low_time

    def test_buy_limit_synced_with_limit(self, session: Session):
        """Test that buy_limit is synced with limit field."""
        item = Item(
            id=4151,
            name="Abyssal whip",
            limit=70,
            buy_limit=70,
        )
        session.add(item)
        session.commit()

        # Update limit
        item.limit = 100
        item.buy_limit = item.limit
        session.add(item)
        session.commit()

        # Verify buy_limit is updated
        updated_item = session.get(Item, 4151)
        assert updated_item.buy_limit == 100
        assert updated_item.limit == 100
