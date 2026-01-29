"""Application routers configuration."""

from fastapi import FastAPI, APIRouter
from backend.api.v1.health import router as health_router
from backend.api.v1.flips import router as flips_router, flipping_router
from backend.api.v1.trades import router as trades_router
from backend.api.v1.watchlist import router as watchlist_router
from backend.api.v1.slayer import router as slayer_router
from backend.api.v1.gear.routes import (
    items,
    loadouts,
    suggestions,
    slayer as gear_slayer,
    boss,
    progression,
    gear_sets,
    dps
)

api_router = APIRouter(prefix="/api/v1")

# Core application routes
api_router.include_router(health_router)
api_router.include_router(flips_router)
api_router.include_router(flipping_router)  # Legacy scanner endpoint for backward compatibility
api_router.include_router(trades_router)
api_router.include_router(watchlist_router)
api_router.include_router(slayer_router)

# Gear routes
api_router.include_router(items.router)
api_router.include_router(loadouts.router)
api_router.include_router(suggestions.router)
api_router.include_router(gear_slayer.router)
api_router.include_router(boss.router)
api_router.include_router(progression.router)
api_router.include_router(gear_sets.router)
api_router.include_router(dps.router)


def include_routers(app: FastAPI) -> None:
    """
    Include all routers in the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    # Root endpoint
    @app.get("/")
    def root():
        """Root endpoint with welcome message."""
        return {"message": "Welcome to OSRS Tool Hub API"}
    
    # Simple health check endpoint at root (avoids naming conflict with health module)
    @app.get("/health")
    def root_health():
        """Simple health check endpoint."""
        return {"status": "healthy"}
    
    # Include API v1 router
    app.include_router(api_router)