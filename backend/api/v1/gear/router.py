"""Gear API router and endpoint definitions."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from backend.db.session import get_session
from backend.models import Item
from backend.services.gear import GearService
from backend.api.v1.gear.schemas import (
    GearSetCreate,
    GearSetResponse,
    BestLoadoutRequest,
    UpgradePathRequest,
    DPSRequest,
)
from backend.api.v1.gear.mappers import (
    map_gear_set_to_response,
    transform_progression_data,
    transform_slot_progression_data,
)
from backend.api.v1.gear.validators import validate_combat_style


router = APIRouter()


@router.post(
    "/gear", response_model=GearSetResponse, status_code=status.HTTP_201_CREATED
)
async def create_gear_set(
    gear_data: GearSetCreate, session: Session = Depends(get_session)
) -> GearSetResponse:
    """
    Create a new gear set.

    Args:
        gear_data: Gear set creation data
        session: Database session

    Returns:
        Created gear set
    """
    service = GearService(session)
    gear_set = await service.create_gear_set(
        gear_data.name, gear_data.items, gear_data.description
    )

    return GearSetResponse(**map_gear_set_to_response(gear_set))


@router.get("/gear", response_model=List[GearSetResponse])
async def get_gear_sets(session: Session = Depends(get_session)) -> List[GearSetResponse]:
    """
    Get all gear sets.

    Args:
        session: Database session

    Returns:
        List of all gear sets
    """
    service = GearService(session)
    gear_sets = service.get_all_gear_sets()

    return [GearSetResponse(**map_gear_set_to_response(gs)) for gs in gear_sets]


@router.get("/gear/suggestions")
async def get_gear_suggestions(
    slot: str,
    style: str = "melee",
    defence_level: int = 99,
    session: Session = Depends(get_session)
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
    service = GearService(session)
        return service.suggest_gear(slot, style, defence_level=defence_level)


@router.get("/gear/{gear_set_id}", response_model=GearSetResponse)
async def get_gear_set(
    gear_set_id: int, session: Session = Depends(get_session)
) -> GearSetResponse:
    """
    Get gear set by ID.

    Args:
        gear_set_id: Gear set ID
        session: Database session

    Returns:
        Gear set data
    """
    service = GearService(session)
    gear_set = service.get_gear_set_by_id(gear_set_id)

    if not gear_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gear set not found"
        )

    return GearSetResponse(**map_gear_set_to_response(gear_set))


@router.delete("/gear/{gear_set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gear_set(
    gear_set_id: int, session: Session = Depends(get_session)
) -> None:
    """
    Delete a gear set.

    Args:
        gear_set_id: Gear set ID
        session: Database session
    """
    service = GearService(session)
    deleted = service.delete_gear_set(gear_set_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gear set not found"
        )


@router.get("/gear/preset")
async def get_preset_loadout(
    combat_style: str,
    tier: str,
    session: Session = Depends(get_session)
):
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/gear/progression/{style}/{tier}")
async def get_progression_loadout(
    style: str,
    tier: str,
    session: Session = Depends(get_session)
):
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result


@router.post("/gear/best-loadout")
async def get_best_loadout(
    request: BestLoadoutRequest,
    session: Session = Depends(get_session)
):
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
            exclude_slots=request.exclude_slots
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/gear/upgrade-path")
async def get_upgrade_path(
    request: UpgradePathRequest,
    session: Session = Depends(get_session)
):
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
            achievements_completed=achievements
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/gear/alternatives")
async def get_alternatives(
    slot: str = Query(..., description="Equipment slot (head, cape, neck, etc.)"),
    combat_style: str = Query("melee", description="Combat style (melee, ranged, magic)"),
    budget: Optional[int] = Query(None, description="Maximum budget for items"),
    attack: Optional[int] = Query(None, description="Attack level"),
    strength: Optional[int] = Query(None, description="Strength level"),
    defence: Optional[int] = Query(None, description="Defence level"),
    ranged: Optional[int] = Query(None, description="Ranged level"),
    magic: Optional[int] = Query(None, description="Magic level"),
    prayer: Optional[int] = Query(None, description="Prayer level"),
    attack_type: Optional[str] = Query(None, description="For melee: stab, slash, crush"),
    limit: int = Query(10, description="Maximum number of alternatives to return"),
    session: Session = Depends(get_session)
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
    service = GearService(session)
    
    stats = None
    if any([attack, strength, defence, ranged, magic, prayer]):
        stats = {
            "attack": attack or 1,
            "strength": strength or 1,
            "defence": defence or 1,
            "ranged": ranged or 1,
            "magic": magic or 1,
            "prayer": prayer or 1
        }
    
    try:
        result = service.get_alternatives(
            slot=slot,
            combat_style=combat_style,
            budget=budget,
            stats=stats,
            attack_type=attack_type,
            limit=limit
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/gear/dps")
async def calculate_dps(
    request: DPSRequest,
    session: Session = Depends(get_session)
):
    """
    Calculate DPS (Damage Per Second) for a gear loadout.
    
    Args:
        request: DPS calculation request with loadout, combat style, etc.
        session: Database session
        
    Returns:
        DPS information including max hit, attack speed, accuracy, etc.
    """
    service = GearService(session)
    
    # Convert item IDs to Item objects
    items = {}
    for slot, item_id in request.loadout.items():
        if item_id is not None:
            item = session.get(Item, item_id)
            if item:
                items[slot] = item
            else:
                items[slot] = None
        else:
            items[slot] = None
    
    try:
        result = service.calculate_dps(
            items=items,
            combat_style=request.combat_style,
            attack_type=request.attack_type,
            player_stats=request.player_stats
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/gear/progression/{combat_style}")
async def get_progression(
    combat_style: str,
    session: Session = Depends(get_session)
):
    """
    Get gear progression data for a combat style with live prices and item details.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        session: Database session
        
    Returns:
        Progression data with enriched item information
    """
    try:
        validate_combat_style(combat_style)
        
        service = GearService(session)
        enriched_data = service.get_wiki_progression(combat_style)
        
        transformed_data = transform_progression_data(enriched_data)
        
        return {
            "combat_style": combat_style,
            "slots": transformed_data
        }
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in get_progression for {combat_style}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading progression data: {str(e)}"
        )


@router.get("/gear/progression/{combat_style}/{slot}")
async def get_slot_progression_data(
    combat_style: str,
    slot: str,
    session: Session = Depends(get_session)
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
            detail=f"Slot '{slot}' not found for combat style '{combat_style}'"
        )
    
    transformed_tiers = transform_slot_progression_data(enriched_data, slot)
    
    return {
        "combat_style": combat_style,
        "slot": slot,
        "tiers": transformed_tiers
    }


@router.get("/gear/wiki-progression/{style}")
async def get_wiki_gear_table(
    style: str,
    session: Session = Depends(get_session)
):
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
