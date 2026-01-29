"""APScheduler configuration and job definitions."""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session

from backend.db.engine import engine
from backend.services.wiki_client import WikiAPIClient
from backend.services.watchlist import WatchlistService

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
    async def update_prices_job() -> None:
        try:
            with Session(engine) as session:
                await wiki_client.sync_prices_to_db(session)
        except Exception as e:
            logger.error(f"Price update failed: {e}")

    # Define job to evaluate watchlist alerts every 5 minutes (300 seconds)
    async def evaluate_watchlist_alerts_job() -> None:
        try:
            with Session(engine) as session:
                service = WatchlistService(session)
                triggered_count = service.evaluate_alerts()
                if triggered_count > 0:
                    logger.info(f"Watchlist alerts: {triggered_count} alerts triggered")
        except Exception as e:
            logger.error(f"Watchlist alert evaluation failed: {e}")

    scheduler.add_job(update_prices_job, "interval", seconds=300)
    scheduler.add_job(evaluate_watchlist_alerts_job, "interval", seconds=300)

    return scheduler
