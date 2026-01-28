"""Tests for wiki client module."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.services.wiki.client import WikiAPIClient


@pytest.fixture
def wiki_client():
    """Create a WikiAPIClient instance."""
    return WikiAPIClient()


class TestWikiAPIClient:
    """Test WikiAPIClient class."""

    def test_init_sets_base_url_and_headers(self, wiki_client):
        """Test that __init__ sets base_url and headers correctly."""
        assert wiki_client.base_url is not None
        assert "User-Agent" in wiki_client.headers
        assert wiki_client.headers["Accept"] == "application/json"

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
            call_args = mock_client.get.call_args
            assert "mapping" in call_args[0][0]
            assert call_args[1]["timeout"] == 30.0
            assert call_args[1]["headers"] == wiki_client.headers

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
    async def test_fetch_mapping_generic_error(self, wiki_client):
        """Test fetch_mapping handles generic errors."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=Exception("Network error"))
            mock_client_class.return_value.__aenter__.return_value = mock_client

            with pytest.raises(Exception, match="Network error"):
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
            call_args = mock_client.get.call_args
            assert "latest" in call_args[0][0]
            assert call_args[1]["timeout"] == 10.0

    @pytest.mark.asyncio
    async def test_fetch_latest_prices_http_error(self, wiki_client):
        """Test fetch_latest_prices handles HTTP errors."""
        import httpx

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_error = httpx.HTTPStatusError(
                "500 Server Error", request=MagicMock(), response=mock_response
            )
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=mock_error)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError):
                await wiki_client.fetch_latest_prices()
