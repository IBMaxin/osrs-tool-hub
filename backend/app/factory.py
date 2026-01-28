"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.lifespan import lifespan
from backend.app.routers import include_routers
from backend.app.middleware import setup_rate_limiting
from backend.config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="OSRS Tool Hub API",
        description="API for OSRS tools including flipping and gear calculators",
        lifespan=lifespan,
        version="1.0.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting middleware (if enabled)
    if settings.rate_limit_enabled:
        app = setup_rate_limiting(app)

    # Include routers
    include_routers(app)

    return app
