"""Tests for scheduler setup and configuration."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.app.scheduler import setup_scheduler


def test_setup_scheduler_creates_scheduler():
    """Test that setup_scheduler creates and configures a scheduler."""
    mock_wiki_client = MagicMock()

    with (
        patch("backend.app.scheduler.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.scheduler.engine"),
        patch("backend.app.scheduler.WatchlistService"),
    ):
        scheduler = setup_scheduler()

        assert isinstance(scheduler, AsyncIOScheduler)
        assert scheduler.running is False  # Not started yet


def test_setup_scheduler_adds_price_job():
    """Test that setup_scheduler adds the price update job."""
    mock_wiki_client = MagicMock()

    with (
        patch("backend.app.scheduler.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.scheduler.engine"),
        patch("backend.app.scheduler.WatchlistService"),
    ):
        scheduler = setup_scheduler()

        # Verify jobs were added (price update and watchlist alerts)
        jobs = scheduler.get_jobs()
        assert len(jobs) == 2
        assert jobs[0].id is not None
        assert jobs[0].trigger.interval.seconds == 300  # 5 minutes
        assert jobs[1].id is not None
        assert jobs[1].trigger.interval.seconds == 300  # 5 minutes


@pytest.mark.asyncio
async def test_price_update_job_executes():
    """Test that the price update job executes correctly."""
    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=None)

    with (
        patch("backend.app.scheduler.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.scheduler.engine"),
        patch("backend.app.scheduler.Session", return_value=mock_session),
        patch("backend.app.scheduler.WatchlistService"),
    ):
        scheduler = setup_scheduler()

        # Get the price update job function (first job)
        jobs = scheduler.get_jobs()
        job_func = jobs[0].func

        # Execute the job
        await job_func()

        # Verify sync was called
        mock_wiki_client.sync_prices_to_db.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_price_update_job_handles_errors():
    """Test that the price update job handles errors gracefully."""
    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock(side_effect=Exception("Sync failed"))

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=None)

    with (
        patch("backend.app.scheduler.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.scheduler.engine"),
        patch("backend.app.scheduler.Session", return_value=mock_session),
        patch("backend.app.scheduler.WatchlistService"),
        patch("backend.app.scheduler.logger") as mock_logger,
    ):
        scheduler = setup_scheduler()

        # Get the price update job function (first job)
        jobs = scheduler.get_jobs()
        job_func = jobs[0].func

        # Execute the job - should not raise
        await job_func()

        # Verify error was logged
        mock_logger.error.assert_called_once()
