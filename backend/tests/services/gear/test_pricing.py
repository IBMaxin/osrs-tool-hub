"""Unit tests for gear pricing utilities."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.services.gear.pricing import get_item_price, get_item_cost
from backend.models import Item, PriceSnapshot


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


class TestGetItemPrice:
    """Test get_item_price function."""

    def test_get_item_price_from_snapshot(self, test_session):
        """Test that get_item_price returns PriceSnapshot.high_price when available."""
        # Create item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        test_session.add(item)

        # Create price snapshot
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
        )
        test_session.add(snapshot)
        test_session.commit()

        price = get_item_price(test_session, item)
        assert price == 1500000

    def test_get_item_price_fallback_to_value(self, test_session):
        """Test that get_item_price falls back to item.value when no snapshot."""
        # Create item with value but no snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        test_session.add(item)
        test_session.commit()

        price = get_item_price(test_session, item)
        assert price == 2000000

    def test_get_item_price_fallback_to_zero(self, test_session):
        """Test that get_item_price returns 0 when value is None."""
        # Create item with no value and no snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=0,
        )
        test_session.add(item)
        test_session.commit()

        price = get_item_price(test_session, item)
        assert price == 0

    def test_get_item_price_snapshot_with_none_high_price(self, test_session):
        """Test that get_item_price falls back when snapshot.high_price is None."""
        # Create item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        test_session.add(item)

        # Create snapshot with None high_price
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=None,
            low_price=1400000,
        )
        test_session.add(snapshot)
        test_session.commit()

        price = get_item_price(test_session, item)
        assert price == 2000000  # Falls back to value


class TestGetItemCost:
    """Test get_item_cost function."""

    def test_get_item_cost_from_snapshot_low_price(self, test_session):
        """Test that get_item_cost returns PriceSnapshot.low_price when available."""
        # Create item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        )
        test_session.add(item)

        # Create price snapshot
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
        )
        test_session.add(snapshot)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 1400000

    def test_get_item_cost_fallback_to_item_low_price(self, test_session):
        """Test that get_item_cost falls back to item.low_price when no snapshot."""
        # Create item with low_price but no snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            low_price=1450000,
        )
        test_session.add(item)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 1450000

    def test_get_item_cost_fallback_to_value(self, test_session):
        """Test that get_item_cost falls back to item.value when no low_price."""
        # Create item with value but no low_price and no snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            low_price=None,
        )
        test_session.add(item)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 2000000

    def test_get_item_cost_fallback_to_zero(self, test_session):
        """Test that get_item_cost returns 0 when all fallbacks are None/0."""
        # Create item with no value, no low_price, no snapshot
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=0,
            low_price=None,
        )
        test_session.add(item)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 0

    def test_get_item_cost_snapshot_with_none_low_price(self, test_session):
        """Test that get_item_cost falls back when snapshot.low_price is None."""
        # Create item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            low_price=1450000,
        )
        test_session.add(item)

        # Create snapshot with None low_price
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=None,
        )
        test_session.add(snapshot)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 1450000  # Falls back to item.low_price

    def test_get_item_cost_prefers_snapshot_over_item_low_price(self, test_session):
        """Test that snapshot.low_price takes precedence over item.low_price."""
        # Create item with low_price
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            low_price=1450000,
        )
        test_session.add(item)

        # Create snapshot with different low_price
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,  # Different from item.low_price
        )
        test_session.add(snapshot)
        test_session.commit()

        cost = get_item_cost(test_session, item)
        assert cost == 1400000  # Uses snapshot, not item.low_price
