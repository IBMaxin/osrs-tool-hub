"""
Database package.

This module re-exports all database components for backward compatibility.
"""

from backend.db.engine import engine
from backend.db.session import get_session
from backend.db.migrations import migrate_tables, init_db

__all__ = [
    "engine",
    "get_session",
    "migrate_tables",
    "init_db",
]
