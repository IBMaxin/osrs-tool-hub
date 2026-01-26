"""Database configuration and initialization."""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text, inspect

from backend.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=False,
)


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
                "variant_of": "INTEGER"
            }
            with engine.begin() as conn:
                for col, dtype in new_item_columns.items():
                    if col not in existing_columns:
                        try:
                            conn.execute(text(f"ALTER TABLE item ADD COLUMN {col} {dtype}"))
                            print(f"✓ Added column: item.{col}")
                        except Exception as e:
                            print(f"⚠ Could not add column item.{col}: {e}")

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


def get_session() -> Session:
    """Get database session."""
    with Session(engine) as session:
        yield session
