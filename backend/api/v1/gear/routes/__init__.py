"""Gear API route modules."""
from fastapi import APIRouter

from .gear_sets import router as gear_sets_router
from .progression import router as progression_router
from .loadouts import router as loadouts_router
from .suggestions import router as suggestions_router
from .dps import router as dps_router

# Create main router and include all sub-routers
router = APIRouter()

router.include_router(gear_sets_router)
router.include_router(progression_router)
router.include_router(loadouts_router)
router.include_router(suggestions_router)
router.include_router(dps_router)
