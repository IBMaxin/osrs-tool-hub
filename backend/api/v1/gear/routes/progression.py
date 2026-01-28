"""Gear progression endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.api.v1.gear.mappers import (
    transform_progression_data,
    transform_slot_progression_data,
)
from backend.api.v1.gear.validators import validate_combat_style

router = APIRouter()


@router.get("/gear/progression/{combat_style}")
async def get_progression(combat_style: str, session: Session = Depends(get_session)):
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
):
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


@router.get("/gear/wiki-progression/{style}")
async def get_wiki_gear_table(style: str, session: Session = Depends(get_session)):
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
async def get_progression_loadout(style: str, tier: str, session: Session = Depends(get_session)):
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
