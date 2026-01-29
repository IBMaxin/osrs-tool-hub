"""Loadout optimization endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.api.v1.gear.schemas import (
    BestLoadoutRequest,
    UpgradePathRequest,
)

router = APIRouter()


@router.get("/gear/preset")
async def get_preset_loadout(
    combat_style: str, tier: str, session: Session = Depends(get_session)
) -> dict:
    """
    Get a full loadout for a specific combat style and tier.

    Args:
        combat_style: Combat style (melee, ranged, magic)
        tier: Tier level (low, mid, high)
        session: Database session

    Returns:
        Full loadout with items, stats, and total cost
    """
    service = GearService(session)
    try:
        return service.get_preset_loadout(combat_style, tier)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/gear/best-loadout")
async def get_best_loadout(
    request: BestLoadoutRequest, session: Session = Depends(get_session)
) -> dict:
    """
    Get the best loadout a player can afford/wear based on stats and budget.

    Args:
        request: Best loadout request with combat style, budget, stats, etc.
        session: Database session

    Returns:
        Best loadout with items, total cost, and DPS
    """
    service = GearService(session)
    quests = set(request.quests_completed) if request.quests_completed else None
    achievements = set(request.achievements_completed) if request.achievements_completed else None

    try:
        result = service.get_best_loadout(
            combat_style=request.combat_style,
            budget=request.budget,
            stats=request.stats,
            attack_type=request.attack_type,
            quests_completed=quests,
            achievements_completed=achievements,
            exclude_slots=request.exclude_slots,
            ironman=request.ironman,
            exclude_items=request.exclude_items,
            content_tag=request.content_tag,
            max_tick_manipulation=request.max_tick_manipulation,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/gear/upgrade-path")
async def get_upgrade_path(request: UpgradePathRequest, session: Session = Depends(get_session)) -> dict:
    """
    Find the next upgrade path with cost analysis.

    Args:
        request: Upgrade path request with current loadout, budget, stats, etc.
        session: Database session

    Returns:
        Upgrade recommendations per slot with cost and efficiency
    """
    service = GearService(session)
    quests = set(request.quests_completed) if request.quests_completed else None
    achievements = set(request.achievements_completed) if request.achievements_completed else None

    try:
        result = service.get_upgrade_path(
            current_loadout=request.current_loadout,
            combat_style=request.combat_style,
            budget=request.budget,
            stats=request.stats,
            attack_type=request.attack_type,
            quests_completed=quests,
            achievements_completed=achievements,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
