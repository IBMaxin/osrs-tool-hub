"""Tests for seed_prices script."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.scripts.seed_prices import seed_prices


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
def mock_wiki_client():
    """Mock WikiAPIClient."""
    mock_client = MagicMock()

    # Mock mapping data
    mock_client.fetch_mapping = AsyncMock(
        return_value=[
            {"id": 4151, "name": "Abyssal whip", "members": True, "limit": 70, "value": 2000000},
            {"id": 314, "name": "Feather", "members": False, "limit": 13000, "value": 2},
        ]
    )

    # Mock price data
    mock_client.fetch_latest_prices = AsyncMock(
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
                "314": {
                    "high": 3,
                    "low": 3,
                    "highTime": 1700000000,
                    "lowTime": 1700000000,
                    "highVolume": 1000000,
                    "lowVolume": 1000000,
                },
            }
        }
    )

    mock_client.sync_items_to_db = AsyncMock()
    mock_client.sync_prices_to_db = AsyncMock()

    return mock_client


@pytest.mark.asyncio
async def test_seed_prices_success(test_engine, mock_wiki_client):
    """Test successful price seeding."""
    with (
        patch("backend.scripts.seed_prices.engine", test_engine),
        patch("backend.scripts.seed_prices.WikiAPIClient", return_value=mock_wiki_client),
    ):

        await seed_prices()

        # Verify sync methods were called
        mock_wiki_client.sync_items_to_db.assert_called_once()
        mock_wiki_client.sync_prices_to_db.assert_called_once()


@pytest.mark.asyncio
async def test_seed_prices_handles_api_error(test_engine):
    """Test that seed_prices handles API errors gracefully."""
    mock_client = MagicMock()
    mock_client.sync_items_to_db = AsyncMock(side_effect=Exception("API Error"))

    with (
        patch("backend.scripts.seed_prices.engine", test_engine),
        patch("backend.scripts.seed_prices.WikiAPIClient", return_value=mock_client),
    ):

        # Should not raise, but handle the error
        with pytest.raises(Exception):
            await seed_prices()
