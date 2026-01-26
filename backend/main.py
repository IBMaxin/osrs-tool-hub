"""Main FastAPI application entry point."""
from backend.app.factory import create_app

# Create the application
app = create_app()
