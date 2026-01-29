"""Centralized logging configuration for the application."""

import logging
import sys


def setup_logging():
    """
    Configure logging for the entire application.
    Sets INFO level for production use to avoid performance issues during startup.
    """
    # Configure root logger with INFO level (DEBUG causes massive output during DB loading)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Set INFO level for all application loggers
    logging.getLogger("backend").setLevel(logging.INFO)

    # Set INFO for SQLModel/SQLAlchemy to avoid logging every row during startup
    logging.getLogger("sqlmodel").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.orm").setLevel(logging.WARNING)

    # Set INFO for httpx (HTTP requests)
    logging.getLogger("httpx").setLevel(logging.INFO)

    # Set INFO for FastAPI/Uvicorn
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

    # Set INFO for APScheduler
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    # Set INFO for anyio (async library)
    logging.getLogger("anyio").setLevel(logging.INFO)

    # Get root logger and log that logging is configured
    root_logger = logging.getLogger()
    root_logger.info("Logging configured at INFO level")
