"""Router configuration and mounting."""

from fastapi import FastAPI

from backend.api.v1 import flips, gear, slayer, trades, watchlist
from backend.services.flipping import FlippingService, FlipOpportunity
from fastapi import Depends, Query
from typing import List
from backend.db.session import get_session
from sqlmodel import Session


def include_routers(app: FastAPI) -> None:
    """
    Include all API routers in the application.

    Args:
        app: FastAPI application instance
    """
    # Include versioned routers
    app.include_router(flips.router, prefix="/api/v1")
    app.include_router(gear.router, prefix="/api/v1")
    app.include_router(slayer.router, prefix="/api/v1")
    app.include_router(trades.router, prefix="/api/v1")
    app.include_router(watchlist.router, prefix="/api/v1")

    # GE Tracker-style flip scanner endpoint
    @app.get("/api/v1/flipping/scanner", response_model=List[FlipOpportunity], tags=["Flipping"])
    def get_flip_scanner(
        budget: int = Query(..., description="Maximum budget in GP", gt=0),
        min_roi: float = Query(..., description="Minimum ROI percentage", ge=0.0),
        min_volume: int = Query(..., description="Minimum volume requirement", ge=0),
        exclude_members: bool = Query(False, description="Exclude members-only items"),
        session: Session = Depends(get_session),
    ) -> List[FlipOpportunity]:
        """
        GE Tracker-style flip scanner endpoint.

        Finds the best flip opportunities based on budget, ROI, and volume filters.
        All calculations are performed in the database layer for optimal performance.

        Args:
            budget: Maximum budget in GP (required)
            min_roi: Minimum ROI percentage (required)
            min_volume: Minimum volume requirement (required)
            exclude_members: If True, exclude members-only items
            session: Database session

        Returns:
            List of FlipOpportunity models sorted by potential profit
        """
        service = FlippingService(session)
        return service.find_best_flips(
            budget=budget, min_roi=min_roi, min_volume=min_volume, exclude_members=exclude_members
        )

    # Root and health endpoints
    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint."""
        return {"message": "OSRS Tool Hub API"}

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    # Admin endpoints
    @app.post("/api/v1/admin/sync-stats")
    async def sync_stats(session: Session = Depends(get_session)):
        """
        Sync item stats from OSRSBox.

        This is a heavy operation (20MB JSON), so it might take 10-20 seconds.
        """
        from backend.services.item_stats import import_item_stats

        await import_item_stats(session)
        return {"status": "Stats updated"}
