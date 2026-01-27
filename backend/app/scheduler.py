"""APScheduler configuration and job definitions."""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session

from backend.db.engine import engine
from backend.services.wiki_client import WikiAPIClient

logger = logging.getLogger(__name__)


def setup_scheduler() -> AsyncIOScheduler:
    """
    Set up and configure the APScheduler.
    
    Returns:
        Configured scheduler instance
    """
    scheduler = AsyncIOScheduler()
    wiki_client = WikiAPIClient()
    
    # Define job to run every 5 minutes (300 seconds)
    async def update_prices_job():
        try:
            with Session(engine) as session:
                await wiki_client.sync_prices_to_db(session)
        except Exception as e:
            logger.error(f"Price update failed: {e}")

    scheduler.add_job(update_prices_job, 'interval', seconds=300)
    
    return scheduler
