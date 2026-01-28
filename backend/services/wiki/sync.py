"""Database synchronization utilities for Wiki data."""

import logging
from sqlmodel import Session, select

from backend.models import Item, PriceSnapshot
from backend.services.wiki.client import WikiAPIClient

logger = logging.getLogger(__name__)


async def sync_items_to_db(client: WikiAPIClient, session: Session) -> None:
    """
    Populate or update Item table from Wiki mapping.

    Args:
        client: WikiAPIClient instance
        session: Database session
    """
    logger.info("Syncing items from Wiki...")
    mapping = await client.fetch_mapping()

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


async def sync_prices_to_db(client: WikiAPIClient, session: Session) -> None:
    """
    Populate or update PriceSnapshot table from latest prices.

    Args:
        client: WikiAPIClient instance
        session: Database session
    """
    logger.info("Syncing prices from Wiki...")
    prices_data = await client.fetch_latest_prices()

    # The API returns data in format: {"data": {item_id: {high, low, highTime, lowTime, ...}}}
    data = prices_data.get("data", {})
    count = 0

    for item_id_str, price_info in data.items():
        try:
            item_id = int(item_id_str)

            # Extract price data
            high_price = price_info.get("high")
            low_price = price_info.get("low")
            high_volume = price_info.get("highVolume")
            low_volume = price_info.get("lowVolume")
            high_time = price_info.get("highTime")
            low_time = price_info.get("lowTime")

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

            # Also update denormalized price fields on Item for performance
            item = session.get(Item, item_id)
            if item:
                item.high_price = high_price
                item.low_price = low_price
                item.high_time = high_time
                item.low_time = low_time
                item.buy_limit = item.limit  # Keep buy_limit in sync with limit
                session.add(item)

            count += 1

        except (ValueError, KeyError) as e:
            logger.warning(f"Skipping invalid price data for item {item_id_str}: {e}")
            continue

    session.commit()
    logger.info(f"Synced {count} price snapshots")
