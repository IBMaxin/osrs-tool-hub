"""Main FastAPI application entry point."""
# Setup logging first, before importing anything else
from backend.app.logging_config import setup_logging
setup_logging()

from backend.app.factory import create_app

# Create the application
app = create_app()
