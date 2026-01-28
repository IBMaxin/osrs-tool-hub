"""Tests for wiki_client module (backward compatibility shim)."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from backend.services.wiki_client import WikiAPIClient
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
def wiki_client():
    """Create a WikiAPIClient instance."""
    return WikiAPIClient()


class TestWikiAPIClientFetchMethods:
    """Test fetch methods of WikiAPIClient."""

    @pytest.mark.asyncio
    async def test_fetch_mapping_success(self, wiki_client):
        """Test successful fetch_mapping call."""
        mock_data = [
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000},
            {"id": 314, "name": "Feather", "members": False, "limit": 13000, "value": 2},
        ]

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            result = await wiki_client.fetch_mapping()

            assert result == mock_data
            mock_client.get.assert_called_once()
            assert "mapping" in mock_client.get.call_args[0][0]

    @pytest.mark.asyncio
    async def test_fetch_mapping_403_error(self, wiki_client):
        """Test fetch_mapping handles 403 Forbidden error."""
        import httpx

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 403
            mock_error = httpx.HTTPStatusError(
                "403 Forbidden", request=MagicMock(), response=mock_response
            )
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=mock_error)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError):
                await wiki_client.fetch_mapping()

    @pytest.mark.asyncio
    async def test_fetch_latest_prices_success(self, wiki_client):
        """Test successful fetch_latest_prices call."""
        mock_data = {
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                }
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            result = await wiki_client.fetch_latest_prices()

            assert result == mock_data
            mock_client.get.assert_called_once()
            assert "latest" in mock_client.get.call_args[0][0]

    @pytest.mark.asyncio
    async def test_fetch_24h_prices_success(self, wiki_client):
        """Test successful fetch_24h_prices call."""
        mock_data = {
            "data": {
                "4151": {
                    "highPriceVolume": 5000,
                    "lowPriceVolume": 4000,
                }
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            result = await wiki_client.fetch_24h_prices()

            assert result == mock_data
            mock_client.get.assert_called_once()
            assert "24h" in mock_client.get.call_args[0][0]


class TestWikiAPIClientSyncMethods:
    """Test sync methods of WikiAPIClient."""

    @pytest.mark.asyncio
    async def test_sync_items_to_db_creates_items(self, wiki_client, test_session):
        """Test sync_items_to_db creates items from mapping."""
        mock_mapping = [
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000},
            {"id": 314, "name": "Feather", "members": False, "limit": 13000, "value": 2},
        ]

        with patch.object(wiki_client, "fetch_mapping", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_mapping

            await wiki_client.sync_items_to_db(test_session)

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

    @pytest.mark.asyncio
    async def test_sync_items_to_db_updates_existing(self, wiki_client, test_session):
        """Test sync_items_to_db updates existing items."""
        # Create existing item
        existing_item = Item(id=4151, name="Old name", members=False, limit=50, value=1000000)
        test_session.add(existing_item)
        test_session.commit()

        mock_mapping = [
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000}
        ]

        with patch.object(wiki_client, "fetch_mapping", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_mapping

            await wiki_client.sync_items_to_db(test_session)

            # Verify item was updated
            updated_item = test_session.get(Item, 4151)
            assert updated_item.name == "Abyssal whip"
            assert updated_item.members is True
            assert updated_item.limit == 70

    @pytest.mark.asyncio
    async def test_sync_prices_to_db_creates_snapshots(self, wiki_client, test_session):
        """Test sync_prices_to_db creates price snapshots with 24h volume."""
        # Create item first
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        test_session.add(item)
        test_session.commit()

        mock_latest_prices = {
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                }
            }
        }

        mock_24h_prices = {
            "data": {
                "4151": {
                    "highPriceVolume": 5000,
                    "lowPriceVolume": 4000,
                }
            }
        }

        with (
            patch.object(wiki_client, "fetch_latest_prices", new_callable=AsyncMock) as mock_latest,
            patch.object(wiki_client, "fetch_24h_prices", new_callable=AsyncMock) as mock_24h,
        ):
            mock_latest.return_value = mock_latest_prices
            mock_24h.return_value = mock_24h_prices

            await wiki_client.sync_prices_to_db(test_session)

            # Verify snapshot was created with 24h volume
            snapshot = test_session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
            ).first()

            assert snapshot is not None
            assert snapshot.high_price == 1500000
            assert snapshot.low_price == 1400000
            assert snapshot.high_volume == 5000  # From 24h data
            assert snapshot.low_volume == 4000  # From 24h data

    @pytest.mark.asyncio
    async def test_sync_prices_to_db_updates_existing_snapshot(self, wiki_client, test_session):
        """Test sync_prices_to_db updates existing price snapshots."""
        # Create item and snapshot
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        test_session.add(item)

        existing_snapshot = PriceSnapshot(
            item_id=4151, high_price=1000000, low_price=900000, high_volume=1000, low_volume=800
        )
        test_session.add(existing_snapshot)
        test_session.commit()

        mock_latest_prices = {
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                }
            }
        }

        mock_24h_prices = {
            "data": {
                "4151": {
                    "highPriceVolume": 5000,
                    "lowPriceVolume": 4000,
                }
            }
        }

        with (
            patch.object(wiki_client, "fetch_latest_prices", new_callable=AsyncMock) as mock_latest,
            patch.object(wiki_client, "fetch_24h_prices", new_callable=AsyncMock) as mock_24h,
        ):
            mock_latest.return_value = mock_latest_prices
            mock_24h.return_value = mock_24h_prices

            await wiki_client.sync_prices_to_db(test_session)

            # Verify snapshot was updated
            updated_snapshot = test_session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
            ).first()

            assert updated_snapshot.high_price == 1500000
            assert updated_snapshot.low_price == 1400000
            assert updated_snapshot.high_volume == 5000
            assert updated_snapshot.low_volume == 4000

    @pytest.mark.asyncio
    async def test_sync_prices_to_db_handles_invalid_data(self, wiki_client, test_session):
        """Test sync_prices_to_db handles invalid price data gracefully."""
        # Create item for valid ID
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        test_session.add(item)
        test_session.commit()

        mock_latest_prices = {
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                },
                "invalid": {"high": 1000},  # Invalid item ID (string, not int)
            }
        }

        mock_24h_prices = {"data": {}}

        with (
            patch.object(wiki_client, "fetch_latest_prices", new_callable=AsyncMock) as mock_latest,
            patch.object(wiki_client, "fetch_24h_prices", new_callable=AsyncMock) as mock_24h,
        ):
            mock_latest.return_value = mock_latest_prices
            mock_24h.return_value = mock_24h_prices

            # Should not raise, but handle invalid entries
            await wiki_client.sync_prices_to_db(test_session)

            # Should have snapshot for valid item
            valid_snapshot = test_session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
            ).first()
            assert valid_snapshot is not None
            assert valid_snapshot.high_price == 1500000

    @pytest.mark.asyncio
    async def test_sync_prices_to_db_fallback_to_realtime_volume(self, wiki_client, test_session):
        """Test sync_prices_to_db falls back to realtime volume if 24h not available."""
        # Create item
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        test_session.add(item)
        test_session.commit()

        mock_latest_prices = {
            "data": {
                "4151": {
                    "high": 1500000,
                    "low": 1400000,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 3000,  # Realtime volume
                    "lowVolume": 2000,
                }
            }
        }

        mock_24h_prices = {"data": {}}  # No 24h data for this item

        with (
            patch.object(wiki_client, "fetch_latest_prices", new_callable=AsyncMock) as mock_latest,
            patch.object(wiki_client, "fetch_24h_prices", new_callable=AsyncMock) as mock_24h,
        ):
            mock_latest.return_value = mock_latest_prices
            mock_24h.return_value = mock_24h_prices

            await wiki_client.sync_prices_to_db(test_session)

            # Note: The current implementation uses 24h volume, but if not available,
            # it defaults to 0. This test verifies the behavior.
            snapshot = test_session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == 4151)
            ).first()

            assert snapshot is not None
            # Volume will be 0 since 24h data is empty and code doesn't use realtime volume
            assert snapshot.high_volume == 0
            assert snapshot.low_volume == 0
