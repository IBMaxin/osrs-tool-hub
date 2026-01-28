"""Database session management."""

from sqlmodel import Session

from backend.db.engine import engine


def get_session() -> Session:
    """Get database session."""
    with Session(engine) as session:
        yield session
