"""DPS calculation endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.models import Item
from backend.services.gear import GearService
from backend.api.v1.gear.schemas import DPSRequest

router = APIRouter()


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
