"""Database migrations and initialization."""

from sqlmodel import SQLModel
from sqlalchemy import inspect, text

from backend.db.engine import engine


def migrate_tables() -> None:
    """Run table migrations."""
    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        # 1. Item table migrations
        if "item" in table_names:
            existing_columns = [col["name"] for col in inspector.get_columns("item")]
            new_item_columns = {
                "quest_req": "TEXT",
                "achievement_req": "TEXT",
                "is_2h": "INTEGER DEFAULT 0",
                "attack_speed": "INTEGER DEFAULT 4",
                "variant_of": "INTEGER",
                # Price fields for GE Tracker-style flipping
                "high_price": "INTEGER",
                "low_price": "INTEGER",
                "high_time": "INTEGER",
                "low_time": "INTEGER",
                "buy_limit": "INTEGER",
            }
            with engine.begin() as conn:
                for col, dtype in new_item_columns.items():
                    if col not in existing_columns:
                        try:
                            conn.execute(text(f"ALTER TABLE item ADD COLUMN {col} {dtype}"))
                            print(f"✓ Added column: item.{col}")
                        except Exception as e:
                            print(f"⚠ Could not add column item.{col}: {e}")

                # After adding columns, sync price data from PriceSnapshot if available
                # This ensures existing databases get populated with price data
                try:
                    conn.execute(
                        text(
                            """
                        UPDATE item 
                        SET 
                            high_price = (SELECT high_price FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            low_price = (SELECT low_price FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            high_time = (SELECT high_time FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            low_time = (SELECT low_time FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            buy_limit = item."limit"
                        WHERE EXISTS (SELECT 1 FROM pricesnapshot WHERE pricesnapshot.item_id = item.id)
                    """
                        )
                    )
                    print("✓ Synced price data from PriceSnapshot to Item table")
                except Exception as e:
                    print(f"⚠ Could not sync price data: {e}")

        # 2. PriceSnapshot table migrations (NEW)
        if "pricesnapshot" in table_names:
            existing_columns = [col["name"] for col in inspector.get_columns("pricesnapshot")]
            new_snapshot_columns = {
                "buy_volume_24h": "INTEGER",
                "sell_volume_24h": "INTEGER",
            }
            with engine.begin() as conn:
                for col, dtype in new_snapshot_columns.items():
                    if col not in existing_columns:
                        try:
                            conn.execute(text(f"ALTER TABLE pricesnapshot ADD COLUMN {col} {dtype}"))
                            print(f"✓ Added column: pricesnapshot.{col}")
                        except Exception as e:
                            print(f"⚠ Could not add column pricesnapshot.{col}: {e}")
        else:
            print("✓ PriceSnapshot table will be created by SQLModel")

        # 3. Trade table migration
        if "trade" not in table_names:
            # Trade table will be created by SQLModel.metadata.create_all
            # This is just a placeholder for future column additions
            print("✓ Trade table will be created by SQLModel")
        else:
            _ = [col["name"] for col in inspector.get_columns("trade")]
            # Future column additions would go here
            print("✓ Trade table exists")

        # 4. Watchlist table migrations
        if "watchlistitem" not in table_names:
            print("✓ WatchlistItem table will be created by SQLModel")
        else:
            print("✓ WatchlistItem table exists")

        if "watchlistalert" not in table_names:
            print("✓ WatchlistAlert table will be created by SQLModel")
        else:
            print("✓ WatchlistAlert table exists")

        # 5. Monster/Slayer Table checks
        # Since SQLModel.metadata.create_all handles creation, we just need to verify
        # manual migrations if we were modifying existing tables.
        # For new tables (Monster, SlayerTask), create_all is sufficient.

    except Exception as e:
        print(f"⚠ Migration check failed: {e}")


async def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
    # Run migration for existing tables
    migrate_tables()
