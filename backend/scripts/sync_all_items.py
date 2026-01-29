"""Script to sync all items and their stats from Wiki API and OSRSBox."""

# ruff: noqa: E402

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session, select, func
from backend.db.engine import engine
from backend.models import Item
from backend.services.wiki_client import WikiAPIClient
from backend.services.item_stats import import_item_stats


async def sync_all():
    """Sync items and stats."""
    print("=" * 60)
    print("Syncing Items and Equipment Stats")
    print("=" * 60)

    wiki_client = WikiAPIClient()

    with Session(engine) as session:
        # Check current state
        item_count = len(list(session.exec(select(Item)).all()))
        items_with_stats = len(list(session.exec(select(Item).where(Item.slot.isnot(None))).all()))

        print("\nCurrent state:")
        print(f"  Total items: {item_count}")
        print(f"  Items with stats: {items_with_stats}")
        print(f"  Items without stats: {item_count - items_with_stats}")

        # Sync items if needed
        if item_count == 0:
            print("\n📥 Syncing items from Wiki API...")
            await wiki_client.sync_items_to_db(session)
            item_count = len(list(session.exec(select(Item)).all()))
            print(f"✅ Synced {item_count} items")
        else:
            print(f"\n✓ Items already in database ({item_count} items)")

        # Import stats
        items_without_stats_count = session.exec(
            select(func.count(Item.id)).where(Item.slot.is_(None))
        ).one()

        if items_without_stats_count > 0:
            print("\n📊 Importing equipment stats from OSRSBox...")
            print(f"   (This may take 10-20 seconds for {items_without_stats_count} items)")
            await import_item_stats(session)

            # Verify
            items_with_stats_after = len(
                list(session.exec(select(Item).where(Item.slot.isnot(None))).all())
            )
            print(f"✅ Stats imported. Items with stats: {items_with_stats_after}")
        else:
            print("\n✓ All items already have equipment stats")

        # Final summary
        final_item_count = len(list(session.exec(select(Item)).all()))
        final_items_with_stats = len(
            list(session.exec(select(Item).where(Item.slot.isnot(None))).all())
        )

        print("\n" + "=" * 60)
        print("Final Summary:")
        print("=" * 60)
        print(f"Total items: {final_item_count}")
        print(f"Items with equipment stats: {final_items_with_stats}")
        print(f"Items without stats: {final_item_count - final_items_with_stats}")

        if final_items_with_stats > 0:
            print("\n✅ Database is ready for gear/DPS features!")
        else:
            print("\n⚠️  Warning: No items with stats found. Check logs for errors.")


if __name__ == "__main__":
    asyncio.run(sync_all())
