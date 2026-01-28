"""OSRS Wiki API HTTP client."""

import httpx
import logging
from typing import Any

from backend.config import settings

logger = logging.getLogger(__name__)


class WikiAPIClient:
    """Client for interacting with the OSRS Wiki API."""

    def __init__(self):
        """Initialize the Wiki API client."""
        self.base_url = settings.wiki_api_base
        self.headers = {"User-Agent": settings.user_agent, "Accept": "application/json"}

    async def fetch_mapping(self) -> list[dict]:
        """
        Fetch item mapping (ID, name, limit, value) from Wiki.

        Returns:
            List of item mapping dictionaries

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        url = f"{self.base_url}/mapping"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    logger.error("403 Forbidden: Invalid User-Agent header")
                raise
            except Exception as e:
                logger.error(f"Mapping fetch failed: {e}")
                raise

    async def fetch_latest_prices(self) -> dict[str, Any]:  # type: ignore[no-any-return]
        """
        Fetch latest high/low prices from Wiki.

        Returns:
            Dictionary with price data

        Raises:
            httpx.HTTPStatusError: If the API request fails
        """
        url = f"{self.base_url}/latest"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
