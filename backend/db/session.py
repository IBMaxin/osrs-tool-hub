"""Database session management."""

from typing import Generator
from sqlmodel import Session

from backend.db.engine import engine


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    try:
        with Session(engine) as session:
            yield session
    finally:
        # Ensure session is properly closed even if exception occurs during yield
        pass
