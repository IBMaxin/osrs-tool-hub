"""
Wiki client module (backward compatibility shim).

This module re-exports from backend.services.wiki for backward compatibility.
New code should import directly from backend.services.wiki.
"""

import httpx
import logging
from typing import Any, Dict, List
from sqlmodel import Session, select

from backend.services.wiki import WikiAPIClient as _WikiAPIClient
from backend.models import Item, PriceSnapshot

logger = logging.getLogger(__name__)


class WikiAPIClient(_WikiAPIClient):
    """WikiAPIClient with backward-compatible sync methods."""

    async def fetch_mapping(self) -> List[Dict[str, Any]]:
        """Fetch item mapping (ID, name, limit, value) from Wiki."""
        url = f"{self.base_url}/mapping"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data if isinstance(data, list) else []
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    logger.error("403 Forbidden: Invalid User-Agent header")
                raise
            except Exception as e:
                logger.error(f"Mapping fetch failed: {e}")
                raise

    async def fetch_latest_prices(self) -> Dict[str, Any]:
        """Fetch latest high/low prices."""
        url = f"{self.base_url}/latest"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {}

    async def fetch_24h_prices(self) -> Dict[str, Any]:
        """Fetch 24h average prices and volume."""
        url = f"{self.base_url}/24h"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {}

    async def sync_items_to_db(self, session: Session) -> None:
        """Populate or update Item table from mapping."""
        logger.info("Syncing items from Wiki...")
        mapping = await self.fetch_mapping()

        count = 0
        for data in mapping:
            # Generate icon URL (replace spaces with underscores)
            safe_name = data.get("name", "").replace(" ", "_")
            icon_url = f"https://oldschool.runescape.wiki/images/{safe_name}_detail.png?0"

            item = Item(
                id=data["id"],
                name=data.get("name", "Unknown"),
                members=data.get("members", True),
                limit=data.get("limit"),
                value=data.get("value", 0),
                icon_url=icon_url,
            )
            session.merge(item)
            count += 1

        session.commit()
        logger.info(f"Synced {count} items")

    async def sync_prices_to_db(self, session: Session) -> None:
        """Populate or update PriceSnapshot table from latest prices AND 24h volume."""
        logger.info("Syncing prices from Wiki...")

        # Fetch both real-time prices and 24h volume
        latest_data = await self.fetch_latest_prices()
        volume_data = await self.fetch_24h_prices()

        # The API returns data in format: {"data": {item_id: {high, low, highTime, lowTime, ...}}}
        realtime_data = latest_data.get("data", {})
        daily_data = volume_data.get("data", {})

        count = 0

        # Iterate through items present in realtime data
        for item_id_str, price_info in realtime_data.items():
            try:
                item_id = int(item_id_str)

                # Extract Real-Time Price Data
                high_price = price_info.get("high")
                low_price = price_info.get("low")
                high_time = price_info.get("highTime")
                low_time = price_info.get("lowTime")

                # Extract 24h Volume Data (fallback to realtime if needed, but usually 24h is better)
                daily_info = daily_data.get(item_id_str, {})
                high_volume = daily_info.get("highPriceVolume", 0)
                low_volume = daily_info.get("lowPriceVolume", 0)

                # Check if price snapshot already exists for this item
                existing = session.exec(
                    select(PriceSnapshot).where(PriceSnapshot.item_id == item_id)
                ).first()

                if existing:
                    # Update existing snapshot
                    existing.high_price = high_price
                    existing.low_price = low_price
                    existing.high_volume = high_volume
                    existing.low_volume = low_volume
                    existing.high_time = high_time
                    existing.low_time = low_time
                    session.add(existing)
                else:
                    # Create new snapshot
                    price_snapshot = PriceSnapshot(
                        item_id=item_id,
                        high_price=high_price,
                        low_price=low_price,
                        high_volume=high_volume,
                        low_volume=low_volume,
                        high_time=high_time,
                        low_time=low_time,
                    )
                    session.add(price_snapshot)

                count += 1

            except (ValueError, KeyError) as e:
                logger.warning(f"Skipping invalid price data for item {item_id_str}: {e}")
                continue

        session.commit()
        logger.info(f"Synced {count} price snapshots with 24h volume")


# Backward compatibility alias
WikiClient = WikiAPIClient

__all__ = ["WikiAPIClient", "WikiClient"]
