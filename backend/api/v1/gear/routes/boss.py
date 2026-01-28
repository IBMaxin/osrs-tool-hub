"""Boss-specific BiS endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.db.session import get_session
from backend.services.gear.boss import BossService, get_available_bosses, get_boss_data

router = APIRouter()


class BossBiSRequest(BaseModel):
    """Request model for boss BiS calculation with constraints."""

    budget: int = Field(..., ge=0, le=2_147_483_647, description="Budget in GP")
    stats: dict[str, int] = Field(
        ..., description="Player stats: attack, strength, defence, ranged, magic, prayer"
    )
    ironman: bool = Field(default=False, description="If True, filter out tradeable items")
    exclude_items: Optional[List[str]] = Field(None, description="List of item names to exclude")
    max_tick_manipulation: bool = Field(
        default=False, description="If True, filter out items requiring tick manipulation"
    )


@router.post("/gear/bis/{boss_name}")
async def calculate_boss_bis(
    boss_name: str,
    request: BossBiSRequest,
    session: Session = Depends(get_session),
) -> dict:
    """
    Calculate BiS for a boss with constraints.

    Args:
        boss_name: Boss name (e.g., "vorkath", "zulrah")
        request: Boss BiS request with budget, stats, and constraints
        session: Database session

    Returns:
        Dictionary with optimal loadout(s) for the boss
    """
    service = BossService(session)

    try:
        result = service.get_bis_for_boss(
            boss_name=boss_name,
            budget=request.budget,
            stats=request.stats,
            ironman=request.ironman,
            exclude_items=request.exclude_items,
            max_tick_manipulation=request.max_tick_manipulation,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/gear/bosses")
async def list_bosses() -> dict:
    """
    Get list of available bosses with full data.

    Returns:
        List of boss data including names, stats, and metadata
    """
    boss_names = get_available_bosses()
    bosses_data = []
    for boss_name in boss_names:
        boss_data = get_boss_data(boss_name)
        if boss_data:
            bosses_data.append(boss_data)
    return {"bosses": bosses_data}
