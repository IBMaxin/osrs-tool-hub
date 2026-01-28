from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from backend.models import Item, PriceSnapshot
from backend.services.flipping import FlippingService
import pytest

# Use StaticPool to share the same in-memory database
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            yield session
    finally:
        SQLModel.metadata.drop_all(engine)
        engine.dispose()


def test_get_flip_opportunities(session: Session):
    # Seed Data
    # 1. Profitable Item (Whip)
    whip = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
    session.add(whip)
    whip_price = PriceSnapshot(
        item_id=4151,
        high_price=1500000,
        low_price=1400000,  # 100k diff
        high_volume=5000,
        low_volume=4000,
    )
    session.add(whip_price)

    # 2. Unprofitable Item (Feather) - Tiny margin
    feather = Item(id=314, name="Feather", limit=13000, value=2)
    session.add(feather)
    feather_price = PriceSnapshot(
        item_id=314, high_price=3, low_price=3, high_volume=1000000, low_volume=1000000  # 0 diff
    )
    session.add(feather_price)

    # 3. Expensive Item (Tbow) - Outside Budget
    tbow = Item(id=20997, name="Twisted bow", limit=8, value=1000000000)
    session.add(tbow)
    tbow_price = PriceSnapshot(
        item_id=20997,
        high_price=1_600_000_000,
        low_price=1_550_000_000,
        high_volume=50,
        low_volume=50,
    )
    session.add(tbow_price)

    session.commit()

    service = FlippingService(session)

    # Test 1: Basic Fetch (Unlimited Budget)
    # Tbow has 360m profit vs Whip's 4.9m, so Tbow should be first.
    flips = service.get_flip_opportunities(min_roi=0.1)
    assert len(flips) >= 2
    assert flips[0]["item_name"] == "Twisted bow"
    assert flips[1]["item_name"] == "Abyssal whip"

    # Check Whip Math
    whip_flip = next(f for f in flips if f["item_name"] == "Abyssal whip")
    assert whip_flip["margin"] == 70000
    assert whip_flip["tax"] == 30000
    # Potential profit should be margin * min(limit, volume) = 70k * min(70, 9000) = 70k * 70 = 4.9M
    assert whip_flip["potential_profit"] == 70000 * 70

    # Test 2: Max Budget Filter (Should exclude Tbow)
    budget_flips = service.get_flip_opportunities(max_budget=10_000_000)
    item_names = [f["item_name"] for f in budget_flips]
    assert "Abyssal whip" in item_names
    assert "Twisted bow" not in item_names
    # Now Whip should be first since Tbow is gone
    assert budget_flips[0]["item_name"] == "Abyssal whip"

    # Test 3: High ROI Filter
    # Whip ROI = 70k / 1.4m = 5%. Tbow ROI = 45m / 1.55b = ~2.9%
    # If we ask for 10%, result should be empty
    high_roi_flips = service.get_flip_opportunities(min_roi=10.0)
    assert len(high_roi_flips) == 0


def test_potential_profit_uses_min_limit_volume(session: Session):
    """Test that potential profit uses MIN(limit, volume) not just limit."""
    # Item with limit > volume
    item1 = Item(id=1, name="Test Item 1", limit=1000, value=10000)
    session.add(item1)
    price1 = PriceSnapshot(
        item_id=1,
        high_price=11000,
        low_price=10000,
        high_volume=50,  # Volume is less than limit
        low_volume=50,
    )
    session.add(price1)

    # Item with volume > limit
    item2 = Item(id=2, name="Test Item 2", limit=100, value=10000)
    session.add(item2)
    price2 = PriceSnapshot(
        item_id=2,
        high_price=11000,
        low_price=10000,
        high_volume=500,  # Volume is more than limit
        low_volume=500,
    )
    session.add(price2)

    session.commit()

    service = FlippingService(session)
    flips = service.get_flip_opportunities(min_roi=0.1)

    # Find our test items
    flip1 = next(f for f in flips if f["item_name"] == "Test Item 1")
    flip2 = next(f for f in flips if f["item_name"] == "Test Item 2")

    # Calculate expected values:
    # sell_price=11000, buy_price=10000
    # tax = 11000 * 0.02 = 220
    # margin = (11000 - 220) - 10000 = 780

    # Item 1: limit=1000, volume=100, margin=780
    # Potential profit should be: 780 * min(1000, 100) = 780 * 100 = 78,000
    expected_margin = (11000 - int(11000 * 0.02)) - 10000  # 780
    assert flip1["potential_profit"] == expected_margin * 100  # margin * min(limit, volume)

    # Item 2: limit=100, volume=1000, margin=780
    # Potential profit should be: 780 * min(100, 1000) = 780 * 100 = 78,000
    assert flip2["potential_profit"] == expected_margin * 100  # margin * min(limit, volume)

    # Verify that both use min(limit, volume), not just limit
    assert flip1["limit"] == 1000  # Limit is 1000
    assert flip1["volume"] == 100  # Volume is 100
    assert flip1["potential_profit"] == expected_margin * 100  # Uses min(1000, 100) = 100

    assert flip2["limit"] == 100  # Limit is 100
    assert flip2["volume"] == 1000  # Volume is 1000
    assert flip2["potential_profit"] == expected_margin * 100  # Uses min(100, 1000) = 100


def test_invalid_sell_price_filtered(session: Session):
    """Test that items with invalid sell prices (0 or negative) are filtered out."""
    # Item with sell_price = 0
    item1 = Item(id=1, name="Invalid Sell 1", limit=100, value=1000)
    session.add(item1)
    price1 = PriceSnapshot(
        item_id=1, high_price=0, low_price=1000, high_volume=100, low_volume=100  # Invalid
    )
    session.add(price1)

    # Item with sell_price < 0
    item2 = Item(id=2, name="Invalid Sell 2", limit=100, value=1000)
    session.add(item2)
    price2 = PriceSnapshot(
        item_id=2, high_price=-100, low_price=1000, high_volume=100, low_volume=100  # Invalid
    )
    session.add(price2)

    # Valid item for comparison
    item3 = Item(id=3, name="Valid Item", limit=100, value=1000)
    session.add(item3)
    price3 = PriceSnapshot(
        item_id=3, high_price=1100, low_price=1000, high_volume=100, low_volume=100
    )
    session.add(price3)

    session.commit()

    service = FlippingService(session)
    flips = service.get_flip_opportunities(min_roi=0.1)

    # Should only have the valid item
    item_names = [f["item_name"] for f in flips]
    assert "Invalid Sell 1" not in item_names
    assert "Invalid Sell 2" not in item_names
    assert "Valid Item" in item_names
