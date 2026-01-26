from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from backend.models import Item, PriceSnapshot
from backend.services.flipping import FlippingService
import pytest

# Use StaticPool to share the same in-memory database
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

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
        low_volume=4000
    )
    session.add(whip_price)

    # 2. Unprofitable Item (Feather) - Tiny margin
    feather = Item(id=314, name="Feather", limit=13000, value=2)
    session.add(feather)
    feather_price = PriceSnapshot(
        item_id=314,
        high_price=3, 
        low_price=3,  # 0 diff
        high_volume=1000000,
        low_volume=1000000
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
        low_volume=50
    )
    session.add(tbow_price)
    
    session.commit()

    service = FlippingService(session)

    # Test 1: Basic Fetch (Should find Whip, maybe Feather depending on tax/roi)
    flips = service.get_flip_opportunities(min_roi=0.1)
    assert len(flips) >= 1
    assert flips[0]["item_name"] == "Abyssal whip"
    
    # Check Whip Math
    # Sell: 1,500,000. Tax (1% > 5m cap? No, 2% of 1.5m = 30k). Post-Tax: 1,470,000.
    # Buy: 1,400,000. Margin: 70,000.
    whip_flip = next(f for f in flips if f["item_name"] == "Abyssal whip")
    assert whip_flip["margin"] == 70000 
    assert whip_flip["tax"] == 30000

    # Test 2: Max Budget Filter (Should exclude Tbow)
    budget_flips = service.get_flip_opportunities(max_budget=10_000_000)
    item_names = [f["item_name"] for f in budget_flips]
    assert "Abyssal whip" in item_names
    assert "Twisted bow" not in item_names

    # Test 3: High ROI Filter
    # Whip ROI = 70k / 1.4m = 5%. If we ask for 10%, it should be empty
    high_roi_flips = service.get_flip_opportunities(min_roi=10.0)
    assert len(high_roi_flips) == 0
