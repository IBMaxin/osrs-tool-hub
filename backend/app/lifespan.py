"""Application lifespan management (startup/shutdown)."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session, select, func

from backend.db.engine import engine
from backend.db.migrations import migrate_tables
from backend.models import Item, SlayerTask, Monster
from backend.services.wiki_client import WikiAPIClient
from backend.app.scheduler import setup_scheduler
from backend.app.logging_config import setup_logging
from backend.seeds.slayer import seed_slayer_data

# Configure logging - DEBUG level for all modules
setup_logging()

logger = logging.getLogger(__name__)


def create_db_and_tables() -> None:
    """Create database tables."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    # Run migration for existing tables
    migrate_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles startup and shutdown tasks:
    - Database initialization
    - Scheduler setup
    - Initial data sync
    """
    # Startup logic
    logger.info("Starting up...")
    create_db_and_tables()
    
    # Initialize scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    
    wiki_client = WikiAPIClient()
    
    # Run initial item sync
    with Session(engine) as session:
        # Check if DB is empty
        item_count = session.exec(select(Item)).first()
        logger.info(f"Current item count in DB: {item_count}")
        if not item_count:
            logger.info("Database is empty, starting initial sync...")
            await wiki_client.sync_items_to_db(session)
        else:
            logger.info(f"Database already has items, skipping initial sync")
        
        # Always sync prices on startup to ensure we have current data
        logger.info("Running initial price sync...")
        await wiki_client.sync_prices_to_db(session)
        
        # Always run seed to ensure data is up to date
        logger.info("Running slayer data seed/update...")
        try:
            seed_slayer_data()
            # Verify after seeding
            slayer_task_count = session.exec(select(func.count(SlayerTask.id))).one()
            monster_count = session.exec(select(func.count(Monster.id))).one()
            logger.info(f"✅ Slayer data updated: {slayer_task_count} tasks, {monster_count} monsters")
        except Exception as e:
            logger.error(f"Failed to seed slayer data: {e}")
            # If seeding fails, check if we have any data
            slayer_task_count = session.exec(select(func.count(SlayerTask.id))).one()
            monster_count = session.exec(select(func.count(Monster.id))).one()
            if slayer_task_count == 0 or monster_count == 0:
                logger.warning("⚠️  No slayer data in database after failed seed attempt")
            else:
                logger.info(f"Using existing slayer data: {slayer_task_count} tasks, {monster_count} monsters")
    
    yield
    
    # Shutdown logic
    scheduler.shutdown()
