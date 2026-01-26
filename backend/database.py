"""
Database module (backward compatibility shim).

This module re-exports from backend.db for backward compatibility.
New code should import directly from backend.db.
"""

from backend.db import engine, get_session, migrate_tables, init_db

__all__ = ["engine", "get_session", "migrate_tables", "init_db"]
