"""Gear API route modules."""

from fastapi import APIRouter

from .gear_sets import router as gear_sets_router
from .progression import router as progression_router
from .loadouts import router as loadouts_router
from .suggestions import router as suggestions_router
from .dps import router as dps_router
from .boss import router as boss_router
from .items import router as items_router
from .slayer import router as slayer_router

# Create main router and include all sub-routers
# Order matters: specific routes must come before parameterized routes
router = APIRouter()

# Include specific routes first (before parameterized routes)
router.include_router(items_router)
router.include_router(suggestions_router)
router.include_router(loadouts_router)
router.include_router(progression_router)
router.include_router(dps_router)
router.include_router(boss_router)
router.include_router(slayer_router)
# Include parameterized routes last
router.include_router(gear_sets_router)
