"""Main FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select

from backend.config import settings
from backend.database import engine, init_db, get_session
from backend.api.v1 import flips, gear, slayer
from backend.models import Item
from backend.services.wiki_client import WikiAPIClient
from backend.services.item_stats import import_item_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_db_and_tables() -> None:
    """Create database tables."""
    from sqlmodel import SQLModel
    from backend.database import migrate_tables
    SQLModel.metadata.create_all(engine)
    # Run migration for existing tables
    migrate_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up...")
    create_db_and_tables()
    
    # Initialize scheduler
    scheduler = AsyncIOScheduler()
    wiki_client = WikiAPIClient()
    
    # Define job to run every 60 seconds
    async def update_prices_job():
        try:
            with Session(engine) as session:
                await wiki_client.sync_prices_to_db(session)
        except Exception as e:
            logger.error(f"Price update failed: {e}")

    scheduler.add_job(update_prices_job, 'interval', seconds=60)
    scheduler.start()
    
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
    
    yield
    
    # Shutdown logic
    scheduler.shutdown()


app = FastAPI(
    title="OSRS Tool Hub API",
    description="API for OSRS tools including flipping and gear calculators",
    lifespan=lifespan,
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(flips.router, prefix="/api/v1")
app.include_router(gear.router, prefix="/api/v1")
app.include_router(slayer.router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "OSRS Tool Hub API"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/v1/admin/sync-stats")
async def sync_stats(session: Session = Depends(get_session)):
    """
    Sync item stats from OSRSBox.
    
    This is a heavy operation (20MB JSON), so it might take 10-20 seconds.
    """
    await import_item_stats(session)
    return {"status": "Stats updated"}
