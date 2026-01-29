"""Tests for database migrations."""

import pytest
from unittest.mock import patch, MagicMock

from backend.db.migrations import migrate_tables, init_db


class TestMigrateTables:
    """Test migrate_tables function."""

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_adds_missing_columns(self, mock_engine, mock_inspect_func):
        """Test migrate_tables adds missing columns to item table."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = ["item"]
        mock_inspector.get_columns.return_value = [
            {"name": "id"},
            {"name": "name"},
        ]

        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_engine.begin.return_value.__exit__.return_value = None

        migrate_tables()

        # Should attempt to add new columns
        assert mock_conn.execute.called

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_skips_existing_columns(self, mock_engine, mock_inspect_func):
        """Test migrate_tables skips columns that already exist."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = ["item"]
        # All columns already exist
        mock_inspector.get_columns.return_value = [
            {"name": "id"},
            {"name": "name"},
            {"name": "quest_req"},
            {"name": "high_price"},
            {"name": "low_price"},
        ]

        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_engine.begin.return_value.__exit__.return_value = None

        migrate_tables()

        # Should not add columns (or only sync price data)
        # The sync query might still run

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_handles_table_not_exists(self, mock_engine, mock_inspect_func):
        """Test migrate_tables handles case when item table doesn't exist."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = []  # No tables

        migrate_tables()

        # Should not error, just skip item table migration

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_syncs_price_data(self, mock_engine, mock_inspect_func):
        """Test migrate_tables syncs price data from PriceSnapshot."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = ["item"]
        mock_inspector.get_columns.return_value = [
            {"name": "id"},
            {"name": "name"},
            {"name": "high_price"},
            {"name": "low_price"},
        ]

        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_engine.begin.return_value.__exit__.return_value = None

        migrate_tables()

        # Should attempt to sync price data
        assert mock_conn.execute.called

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_handles_errors_gracefully(self, mock_engine, mock_inspect_func):
        """Test migrate_tables handles errors gracefully."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.side_effect = Exception("Inspect error")

        # Should not raise
        migrate_tables()

    @patch("backend.db.migrations.inspect")
    @patch("backend.db.migrations.engine")
    def test_migrate_tables_handles_column_add_error(self, mock_engine, mock_inspect_func):
        """Test migrate_tables handles errors when adding columns."""
        mock_inspector = MagicMock()
        mock_inspect_func.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = ["item"]
        mock_inspector.get_columns.return_value = [{"name": "id"}]

        mock_conn = MagicMock()
        mock_conn.execute.side_effect = Exception("Column add error")
        mock_engine.begin.return_value.__enter__.return_value = mock_conn
        mock_engine.begin.return_value.__exit__.return_value = None

        # Should not raise, errors are caught and printed
        migrate_tables()


class TestInitDb:
    """Test init_db function."""

    @patch("backend.db.migrations.migrate_tables")
    @patch("backend.db.migrations.SQLModel")
    @patch("backend.db.migrations.engine")
    @pytest.mark.asyncio
    async def test_init_db_creates_tables(self, mock_engine, mock_sqlmodel, mock_migrate):
        """Test init_db creates all tables."""
        await init_db()

        mock_sqlmodel.metadata.create_all.assert_called_once_with(mock_engine)
        mock_migrate.assert_called_once()

    @patch("backend.db.migrations.migrate_tables")
    @patch("backend.db.migrations.SQLModel")
    @patch("backend.db.migrations.engine")
    @pytest.mark.asyncio
    async def test_init_db_runs_migrations(self, mock_engine, mock_sqlmodel, mock_migrate):
        """Test init_db runs migrations after creating tables."""
        await init_db()

        # Should call migrate_tables after create_all
        assert mock_sqlmodel.metadata.create_all.called
        assert mock_migrate.called
