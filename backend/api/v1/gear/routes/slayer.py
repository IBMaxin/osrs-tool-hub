"""Slayer gear suggestion endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.api.v1.gear.schemas import SlayerGearRequest

router = APIRouter()


@router.post("/gear/slayer-gear")
async def suggest_slayer_gear(request: SlayerGearRequest, session: Session = Depends(get_session)):
    """
    Suggest optimal gear for a slayer task based on user levels.

    Args:
        request: Slayer gear request with task_id, stats, budget, etc.
        session: Database session

    Returns:
        Optimal loadout for the slayer task with task context
    """
    service = GearService(session)
    quests = set(request.quests_completed) if request.quests_completed else None
    achievements = set(request.achievements_completed) if request.achievements_completed else None

    try:
        result = service.suggest_slayer_gear(
            task_id=request.task_id,
            stats=request.stats,
            budget=request.budget,
            combat_style=request.combat_style,
            quests_completed=quests,
            achievements_completed=achievements,
            ironman=request.ironman,
        )

        if "error" in result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
