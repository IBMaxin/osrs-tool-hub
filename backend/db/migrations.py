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
                "buy_limit": "INTEGER"
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
                    conn.execute(text("""
                        UPDATE item 
                        SET 
                            high_price = (SELECT high_price FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            low_price = (SELECT low_price FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            high_time = (SELECT high_time FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            low_time = (SELECT low_time FROM pricesnapshot WHERE pricesnapshot.item_id = item.id),
                            buy_limit = item.limit
                        WHERE EXISTS (SELECT 1 FROM pricesnapshot WHERE pricesnapshot.item_id = item.id)
                    """))
                    print("✓ Synced price data from PriceSnapshot to Item table")
                except Exception as e:
                    print(f"⚠ Could not sync price data: {e}")

        # 2. Monster/Slayer Table checks
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
