"""Gear suggestions and alternatives endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.api.v1.gear.validators import validate_combat_style
from backend.api.v1.validators import validate_slot

router = APIRouter()


@router.get("/gear/suggestions")
async def get_gear_suggestions(
    slot: str,
    style: str = Query("melee", description="Combat style"),
    defence_level: int = Query(99, ge=1, le=99, description="Defence level"),
    session: Session = Depends(get_session),
):
    """
    Get gear suggestions for a specific slot and combat style.

    Args:
        slot: Equipment slot (head, cape, neck, etc.)
        style: Combat style (melee, ranged, magic, prayer)
        defence_level: Defence level requirement filter
        session: Database session

    Returns:
        List of suggested items with scores
    """
    # Validate inputs
    slot = validate_slot(slot)
    validate_combat_style(style)

    service = GearService(session)
    return service.suggest_gear(slot, style, defence_level=defence_level)


@router.get("/gear/alternatives")
async def get_alternatives(
    slot: str = Query(..., description="Equipment slot (head, cape, neck, etc.)"),
    combat_style: str = Query("melee", description="Combat style (melee, ranged, magic)"),
    budget: Optional[int] = Query(None, ge=0, description="Maximum budget for items"),
    attack: Optional[int] = Query(None, ge=1, le=99, description="Attack level"),
    strength: Optional[int] = Query(None, ge=1, le=99, description="Strength level"),
    defence: Optional[int] = Query(None, ge=1, le=99, description="Defence level"),
    ranged: Optional[int] = Query(None, ge=1, le=99, description="Ranged level"),
    magic: Optional[int] = Query(None, ge=1, le=99, description="Magic level"),
    prayer: Optional[int] = Query(None, ge=1, le=99, description="Prayer level"),
    attack_type: Optional[str] = Query(None, description="For melee: stab, slash, crush"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of alternatives to return"),
    session: Session = Depends(get_session),
):
    """
    Get alternative items for a specific slot.

    Args:
        slot: Equipment slot
        combat_style: Combat style
        budget: Optional budget filter
        attack: Optional attack level requirement
        strength: Optional strength level requirement
        defence: Optional defence level requirement
        ranged: Optional ranged level requirement
        magic: Optional magic level requirement
        prayer: Optional prayer level requirement
        attack_type: For melee, attack type (stab, slash, crush)
        limit: Maximum number of alternatives to return
        session: Database session

    Returns:
        List of alternative items sorted by score
    """
    # Validate inputs
    slot = validate_slot(slot)
    validate_combat_style(combat_style)

    service = GearService(session)

    stats = None
    if any([attack, strength, defence, ranged, magic, prayer]):
        stats = {
            "attack": attack or 1,
            "strength": strength or 1,
            "defence": defence or 1,
            "ranged": ranged or 1,
            "magic": magic or 1,
            "prayer": prayer or 1,
        }

    try:
        result = service.get_alternatives(
            slot=slot,
            combat_style=combat_style,
            budget=budget,
            stats=stats,
            attack_type=attack_type,
            limit=limit,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
