"""Centralized logging configuration for the application."""
import logging
import sys


def setup_logging():
    """
    Configure logging for the entire application.
    Sets DEBUG level for all modules and configures detailed formatting.
    """
    # Configure root logger with DEBUG level
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set DEBUG level for all application loggers
    logging.getLogger('backend').setLevel(logging.DEBUG)
    
    # Enable DEBUG for SQLModel/SQLAlchemy (SQL queries)
    # This shows all SQL queries, parameters, and row data
    logging.getLogger('sqlmodel').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)
    
    # Enable DEBUG for httpx (HTTP requests)
    logging.getLogger('httpx').setLevel(logging.DEBUG)
    
    # Enable DEBUG for FastAPI/Uvicorn
    logging.getLogger('uvicorn').setLevel(logging.DEBUG)
    logging.getLogger('uvicorn.access').setLevel(logging.DEBUG)
    logging.getLogger('fastapi').setLevel(logging.DEBUG)
    
    # Enable DEBUG for APScheduler
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    
    # Enable DEBUG for anyio (async library)
    logging.getLogger('anyio').setLevel(logging.DEBUG)
    
    # Get root logger and log that debug logging is enabled
    root_logger = logging.getLogger()
    root_logger.debug("Debug logging enabled for all modules")
