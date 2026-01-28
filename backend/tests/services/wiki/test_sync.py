"""Tests for wiki sync service."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from backend.services.wiki.sync import sync_items_to_db, sync_prices_to_db
from backend.services.wiki.client import WikiAPIClient
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


@pytest.fixture
def mock_wiki_client():
    """Create a mock WikiAPIClient."""
    client = MagicMock(spec=WikiAPIClient)
    return client


@pytest.mark.asyncio
async def test_sync_items_to_db_creates_items(test_session, mock_wiki_client):
    """Test that sync_items_to_db creates items from mapping."""
    mock_wiki_client.fetch_mapping = AsyncMock(
        return_value=[
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000},
            {"id": 314, "name": "Feather", "members": False, "limit": 13000, "value": 2},
        ]
    )

    await sync_items_to_db(mock_wiki_client, test_session)

    # Verify items were created
    items = test_session.exec(select(Item)).all()
    assert len(items) == 2

    whip = test_session.get(Item, 4151)
    assert whip is not None
    assert whip.name == "Abyssal whip"
    assert whip.members is True
    assert whip.limit == 70
    assert whip.value == 2000000
    assert "Abyssal_whip" in whip.icon_url

    feather = test_session.get(Item, 314)
    assert feather is not None
    assert feather.name == "Feather"
    assert feather.members is False


@pytest.mark.asyncio
async def test_sync_items_to_db_updates_existing(test_session, mock_wiki_client):
    """Test that sync_items_to_db updates existing items."""
    # Create existing item
    existing_item = Item(id=4151, name="Old name", members=False, limit=50, value=1000000)
    test_session.add(existing_item)
    test_session.commit()

    mock_wiki_client.fetch_mapping = AsyncMock(
        return_value=[
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000}
        ]
    )

    await sync_items_to_db(mock_wiki_client, test_session)

    # Verify item was updated
    updated_item = test_session.get(Item, 4151)
    assert updated_item.name == "Abyssal whip"
    assert updated_item.members is True
    assert updated_item.limit == 70
    assert updated_item.value == 2000000


@pytest.mark.asyncio
async def test_sync_prices_to_db_creates_snapshots(test_session, mock_wiki_client):
    """Test that sync_prices_to_db creates price snapshots."""
    # Create item first
    item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
    test_session.add(item)
    test_session.commit()

    mock_wiki_client.fetch_latest_prices = AsyncMock(
        return_value={
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 5000,
                    "lowVolume": 4000,
                }
            }
        }
    )

    await sync_prices_to_db(mock_wiki_client, test_session)

    # Verify snapshot was created
    snapshot = test_session.exec(select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)).first()

    assert snapshot is not None
    assert snapshot.high_price == 1500000
    assert snapshot.low_price == 1400000
    assert snapshot.high_volume == 5000
    assert snapshot.low_volume == 4000

    # Verify item denormalized fields were updated
    updated_item = test_session.get(Item, 4151)
    assert updated_item.high_price == 1500000
    assert updated_item.low_price == 1400000


@pytest.mark.asyncio
async def test_sync_prices_to_db_updates_existing_snapshot(test_session, mock_wiki_client):
    """Test that sync_prices_to_db updates existing price snapshots."""
    # Create item and snapshot
    item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
    test_session.add(item)

    existing_snapshot = PriceSnapshot(
        item_id=4151, high_price=1000000, low_price=900000, high_volume=1000, low_volume=800
    )
    test_session.add(existing_snapshot)
    test_session.commit()

    mock_wiki_client.fetch_latest_prices = AsyncMock(
        return_value={
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 5000,
                    "lowVolume": 4000,
                }
            }
        }
    )

    await sync_prices_to_db(mock_wiki_client, test_session)

    # Verify snapshot was updated
    updated_snapshot = test_session.exec(
        select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
    ).first()

    assert updated_snapshot.high_price == 1500000
    assert updated_snapshot.low_price == 1400000
    assert updated_snapshot.high_volume == 5000


@pytest.mark.asyncio
async def test_sync_prices_to_db_handles_invalid_data(test_session, mock_wiki_client):
    """Test that sync_prices_to_db handles invalid price data gracefully."""
    # Create item for valid ID
    item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
    test_session.add(item)
    test_session.commit()

    mock_wiki_client.fetch_latest_prices = AsyncMock(
        return_value={
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 5000,
                    "lowVolume": 4000,
                },
                "invalid": {"high": 1000},  # Invalid item ID (string, not int)
                "999": {  # Missing required fields - will create snapshot with None values
                    "high": 1000
                    # Missing low, etc.
                },
            }
        }
    )

    # Should not raise, but handle invalid entries
    await sync_prices_to_db(mock_wiki_client, test_session)

    # Should have snapshots (invalid string ID skipped, but 999 creates one with None values)
    snapshots = test_session.exec(select(PriceSnapshot)).all()
    # Valid snapshot for 4151, and one for 999 (with None values)
    assert len(snapshots) >= 1

    # Verify valid snapshot exists
    valid_snapshot = test_session.exec(
        select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
    ).first()
    assert valid_snapshot is not None
    assert valid_snapshot.high_price == 1500000


@pytest.mark.asyncio
async def test_sync_prices_to_db_updates_item_denormalized_fields(test_session, mock_wiki_client):
    """Test that sync_prices_to_db updates denormalized fields on Item."""
    item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
    test_session.add(item)
    test_session.commit()

    mock_wiki_client.fetch_latest_prices = AsyncMock(
        return_value={
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 5000,
                    "lowVolume": 4000,
                }
            }
        }
    )

    await sync_prices_to_db(mock_wiki_client, test_session)

    # Verify item fields were updated
    updated_item = test_session.get(Item, 4151)
    assert updated_item.high_price == 1500000
    assert updated_item.low_price == 1400000
    assert updated_item.high_time == 1700000000
    assert updated_item.low_time == 1700000000
    assert updated_item.buy_limit == 70  # Should sync with limit
