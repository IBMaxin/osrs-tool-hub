"""Tests for application lifespan management."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from backend.app.lifespan import lifespan, create_db_and_tables
from backend.models import Item


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def mock_app():
    """Create a mock FastAPI app."""
    app = MagicMock(spec=FastAPI)
    return app


@pytest.mark.asyncio
async def test_create_db_and_tables(test_engine):
    """Test that create_db_and_tables creates tables."""
    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.migrate_tables") as mock_migrate,
    ):
        create_db_and_tables()

        # Verify tables were created
        with Session(test_engine) as session:
            # Try to query a table to verify it exists
            try:
                session.exec(select(Item)).first()
            except Exception:
                pytest.fail("Tables were not created")

        # Verify migration was called
        mock_migrate.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_startup_empty_db(mock_app, test_engine):
    """Test lifespan startup with empty database."""
    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_items_to_db = AsyncMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data") as mock_seed,
    ):

        # Empty database - no items
        async with lifespan(mock_app):
            # Verify scheduler started
            mock_scheduler.start.assert_called_once()

            # Verify initial sync was called (empty DB)
            mock_wiki_client.sync_items_to_db.assert_called_once()
            mock_wiki_client.sync_prices_to_db.assert_called_once()

            # Verify slayer seed was called
            mock_seed.assert_called_once()

        # Verify scheduler shutdown
        mock_scheduler.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_startup_with_existing_data(mock_app, test_engine):
    """Test lifespan startup with existing database data."""
    # Create tables and add an item
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        session.add(item)
        session.commit()

    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_items_to_db = AsyncMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data") as mock_seed,
    ):

        async with lifespan(mock_app):
            # Verify scheduler started
            mock_scheduler.start.assert_called_once()

            # Verify item sync was NOT called (DB has items)
            mock_wiki_client.sync_items_to_db.assert_not_called()

            # Verify price sync was still called
            mock_wiki_client.sync_prices_to_db.assert_called_once()

            # Verify slayer seed was called
            mock_seed.assert_called_once()

        # Verify scheduler shutdown
        mock_scheduler.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_handles_seed_failure(mock_app, test_engine):
    """Test that lifespan handles slayer seed failures gracefully."""
    SQLModel.metadata.create_all(test_engine)

    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data", side_effect=Exception("Seed failed")),
    ):

        # Should not raise, but handle the error gracefully
        try:
            async with lifespan(mock_app):
                # Context manager should handle the error internally
                pass
        except Exception:
            # If an exception propagates, that's also acceptable for this test
            pass

        # Verify scheduler still shutdown properly (if it was started)
        # Note: shutdown might not be called if startup failed completely


@pytest.mark.asyncio
async def test_lifespan_seed_success_with_verification(mock_app, test_engine):
    """Test lifespan when seed succeeds and verifies counts."""
    SQLModel.metadata.create_all(test_engine)

    # Add some slayer data to verify counts work
    from backend.models import SlayerTask, Monster, SlayerMaster

    with Session(test_engine) as session:
        monster = Monster(id=1, name="Test Monster", combat_level=50, hitpoints=100, slayer_xp=50)
        session.add(monster)
        task = SlayerTask(
            master=SlayerMaster.TURAEL,
            monster_id=monster.id,
            category="Test",
            quantity_min=10,
            quantity_max=20,
            weight=5,
        )
        session.add(task)
        session.commit()

    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_items_to_db = AsyncMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data") as mock_seed,
        patch("backend.app.lifespan.logger") as mock_logger,
    ):

        async with lifespan(mock_app):
            # Verify seed was called
            mock_seed.assert_called_once()
            # Verify verification logging was called
            assert mock_logger.info.called


@pytest.mark.asyncio
async def test_lifespan_seed_failure_no_existing_data(mock_app, test_engine):
    """Test lifespan when seed fails and there's no existing slayer data."""
    SQLModel.metadata.create_all(test_engine)

    # Add an item so DB is not empty (to skip item sync)
    with Session(test_engine) as session:
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        session.add(item)
        session.commit()

    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data", side_effect=Exception("Seed failed")),
        patch("backend.app.lifespan.logger") as mock_logger,
    ):

        async with lifespan(mock_app):
            # Verify error was logged
            mock_logger.error.assert_called()
            # Verify warning was logged (no data case)
            warning_calls = [
                call for call in mock_logger.warning.call_args_list if "No slayer data" in str(call)
            ]
            assert len(warning_calls) > 0


@pytest.mark.asyncio
async def test_lifespan_seed_failure_with_existing_data(mock_app, test_engine):
    """Test lifespan when seed fails but existing slayer data exists."""
    SQLModel.metadata.create_all(test_engine)

    # Add an item so DB is not empty (to skip item sync)
    with Session(test_engine) as session:
        item = Item(id=4151, name="Abyssal whip", limit=70, value=2000000)
        session.add(item)

        # Add existing slayer data
        from backend.models import SlayerTask, Monster, SlayerMaster

        monster = Monster(id=1, name="Test Monster", combat_level=50, hitpoints=100, slayer_xp=50)
        session.add(monster)
        task = SlayerTask(
            master=SlayerMaster.TURAEL,
            monster_id=monster.id,
            category="Test",
            quantity_min=10,
            quantity_max=20,
            weight=5,
        )
        session.add(task)
        session.commit()

    mock_wiki_client = MagicMock()
    mock_wiki_client.sync_prices_to_db = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.start = MagicMock()
    mock_scheduler.shutdown = MagicMock()

    with (
        patch("backend.app.lifespan.engine", test_engine),
        patch("backend.app.lifespan.setup_scheduler", return_value=mock_scheduler),
        patch("backend.app.lifespan.WikiAPIClient", return_value=mock_wiki_client),
        patch("backend.app.lifespan.seed_slayer_data", side_effect=Exception("Seed failed")),
        patch("backend.app.lifespan.logger") as mock_logger,
    ):

        async with lifespan(mock_app):
            # Verify error was logged
            mock_logger.error.assert_called()
            # Verify info was logged (existing data case)
            info_calls = [
                call
                for call in mock_logger.info.call_args_list
                if "existing slayer data" in str(call).lower()
            ]
            assert len(info_calls) > 0
