"""Database configuration and initialization."""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text, inspect

from backend.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=False,
)


def migrate_item_table() -> None:
    """Add new columns to item table if they don't exist."""
    try:
        inspector = inspect(engine)
        
        # Check if item table exists
        if "item" not in inspector.get_table_names():
            return
        
        # Get existing columns
        existing_columns = [col["name"] for col in inspector.get_columns("item")]
        
        # New columns to add (SQLite syntax)
        new_columns = {
            "quest_req": "TEXT",
            "achievement_req": "TEXT",
            "is_2h": "INTEGER DEFAULT 0",  # SQLite uses INTEGER for boolean
            "attack_speed": "INTEGER DEFAULT 4",
            "variant_of": "INTEGER"
        }
        
        # Add missing columns
        with engine.begin() as conn:  # Use begin() for transaction
            for column_name, column_type in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        conn.execute(text(f"ALTER TABLE item ADD COLUMN {column_name} {column_type}"))
                        print(f"✓ Added column: {column_name}")
                    except Exception as e:
                        print(f"⚠ Could not add column {column_name}: {e}")
    except Exception as e:
        print(f"⚠ Migration check failed: {e}")


async def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
    # Run migration for existing tables
    migrate_item_table()


def get_session() -> Session:
    """Get database session."""
    with Session(engine) as session:
        yield session
