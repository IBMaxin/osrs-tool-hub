"""Gear progression endpoints."""

from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.services.gear.progression import get_global_upgrade_path
from backend.services.wiki_data import get_wiki_guide
from backend.api.v1.gear.mappers import (
    transform_progression_data,
    transform_slot_progression_data,
)
from backend.api.v1.gear.validators import validate_combat_style

router = APIRouter()


@router.get("/gear/progression/{combat_style}")
async def get_progression(
    combat_style: str, session: Session = Depends(get_session)
) -> dict[str, object]:
    """
    Get gear progression data for a combat style with live prices and item details.

    Args:
        combat_style: Combat style (melee, ranged, magic)
        session: Database session

    Returns:
        Progression data with enriched item information
    """
    # Validate combat style (raises HTTPException with 400 if invalid)
    validate_combat_style(combat_style)

    try:
        service = GearService(session)
        enriched_data = service.get_wiki_progression(combat_style)

        transformed_data = transform_progression_data(enriched_data)

        return {"combat_style": combat_style, "slots": transformed_data}
    except HTTPException:
        # Re-raise HTTPExceptions (like validation errors) as-is
        raise
    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error in get_progression for {combat_style}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading progression data: {str(e)}",
        )


@router.get("/gear/progression/{combat_style}/{slot}")
async def get_slot_progression_data(
    combat_style: str, slot: str, session: Session = Depends(get_session)
) -> dict[str, object]:
    """
    Get progression data for a specific slot with live prices and item details.

    Args:
        combat_style: Combat style (melee, ranged, magic)
        slot: Equipment slot (head, cape, neck, etc.)
        session: Database session

    Returns:
        Slot progression data with enriched item information
    """
    validate_combat_style(combat_style)

    service = GearService(session)
    enriched_data = service.get_wiki_progression(combat_style)

    if slot not in enriched_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slot '{slot}' not found for combat style '{combat_style}'",
        )

    transformed_tiers = transform_slot_progression_data(enriched_data, slot)

    return {"combat_style": combat_style, "slot": slot, "tiers": transformed_tiers}


@router.get("/gear/wiki-guide/{style}")
async def get_wiki_guide_data(style: str) -> dict:
    """
    Get wiki guide data for a combat style - exact mirror of the wiki page.

    Returns the guide data exactly as written in JSON with no transformation,
    reordering, substitution, or "fixing" of names. The guide is the source
    of truth for slot-for-slot, tier-for-tier, item-for-item matching.

    Args:
        style: Combat style (melee, ranged, magic)

    Returns:
        Guide data with game_stages (tiers + full loadouts), slot_order, bonus_table
    """
    validate_combat_style(style)

    guide_data = get_wiki_guide(style)

    if not guide_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No guide data found for style '{style}'"
        )

    return guide_data


@router.get("/gear/wiki-progression/{style}")
async def get_wiki_gear_table(style: str, session: Session = Depends(get_session)) -> dict:
    """
    Get Wiki-style gear progression table for a combat style.

    Args:
        style: Combat style (melee, ranged, magic)
        session: Database session

    Returns:
        Wiki progression table structure with enriched item data
    """
    validate_combat_style(style)

    service = GearService(session)
    return service.get_wiki_progression(style)


@router.get("/gear/progression/{style}/{tier}")
async def get_progression_loadout(
    style: str, tier: str, session: Session = Depends(get_session)
) -> dict:
    """
    Get a progression loadout for a specific combat style and tier.

    Args:
        style: Combat style (melee, ranged, magic)
        tier: Tier level (low, mid, high)
        session: Database session

    Returns:
        Simplified loadout with basic item information
    """
    service = GearService(session)
    result = service.get_progression_loadout(style, tier)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])

    return result


class GlobalProgressionRequest(BaseModel):
    """Request model for global cross-style progression."""

    current_gear: Dict[str, Dict[str, Optional[int]]] = Field(
        ..., description="Dict of style -> loadout (slot -> item_id)"
    )
    bank_value: int = Field(..., ge=0, le=2_147_483_647, description="Total bank value in GP")
    stats: Dict[str, int] = Field(
        ..., description="Player stats: attack, strength, defence, ranged, magic, prayer"
    )
    unlocked_content: Optional[List[str]] = Field(
        None, description="List of unlocked content (e.g., ['ToA', 'GWD'])"
    )
    attack_type: Optional[str] = Field(None, description="For melee: stab, slash, or crush")
    quests_completed: Optional[List[str]] = Field(None, description="List of completed quests")
    achievements_completed: Optional[List[str]] = Field(
        None, description="List of completed achievements"
    )


@router.post("/gear/global-upgrade-path")
async def get_global_progression(
    request: GlobalProgressionRequest, session: Session = Depends(get_session)
) -> dict:
    """
    Calculate cross-style account progression with prioritized upgrade path.

    Args:
        request: Global progression request with current gear, bank value, stats, etc.
        session: Database session

    Returns:
        Prioritized upgrade path across all styles (melee, ranged, magic)
    """
    quests = set(request.quests_completed) if request.quests_completed else None
    achievements = set(request.achievements_completed) if request.achievements_completed else None

    try:
        result = get_global_upgrade_path(
            session=session,
            current_gear=request.current_gear,
            bank_value=request.bank_value,
            stats=request.stats,
            unlocked_content=request.unlocked_content,
            attack_type=request.attack_type,
            quests_completed=quests,
            achievements_completed=achievements,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
