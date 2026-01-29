"""DPS calculation endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.models import Item
from backend.services.gear import GearService
from backend.services.gear.dps import compare_dps
from backend.api.v1.gear.schemas import (
    DPSRequest,
    DPSComparisonRequest,
    DPSComparisonResponse,
    DPSComparisonResult,
)

router = APIRouter(tags=["Gear", "DPS"])


@router.post("/gear/dps")
async def calculate_dps(request: DPSRequest, session: Session = Depends(get_session)):
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
            player_stats=request.player_stats,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/dps/compare",
    response_model=DPSComparisonResponse,
    summary="Compare DPS for multiple loadouts",
    description="Compare Damage Per Second (DPS) for multiple gear loadouts side-by-side. Returns detailed DPS metrics including max hit, accuracy, attack speed, and marginal gains compared to the baseline loadout.",
)
async def compare_dps_endpoint(
    request: DPSComparisonRequest, session: Session = Depends(get_session)
):
    """
    Compare DPS for multiple loadouts side-by-side.

    Args:
        request: DPS comparison request with multiple loadouts
        session: Database session

    Returns:
        List of DPS results with comparison metrics
    """
    # Convert loadouts from item IDs to Item objects
    loadout_objects = []
    for loadout_input in request.loadouts:
        items = {}
        for slot, item_id in loadout_input.loadout.items():
            if item_id is not None:
                item = session.get(Item, item_id)
                if item:
                    items[slot] = item
                else:
                    items[slot] = None
            else:
                items[slot] = None

        loadout_objects.append(
            {
                "name": loadout_input.name,
                "loadout": items,
            }
        )

    try:
        # Validate that at least one loadout has a weapon
        has_weapon = False
        for loadout_obj in loadout_objects:
            if loadout_obj.get("loadout", {}).get("weapon"):
                has_weapon = True
                break

        if not has_weapon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one loadout must have a weapon equipped for DPS calculation",
            )

        results = compare_dps(
            loadouts=loadout_objects,
            combat_style=request.combat_style,
            attack_type=request.attack_type,
            player_stats=request.player_stats,
            target_monster=request.target_monster,
        )

        # Convert to response models
        response_results = [DPSComparisonResult(**result) for result in results]

        return DPSComparisonResponse(results=response_results)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
