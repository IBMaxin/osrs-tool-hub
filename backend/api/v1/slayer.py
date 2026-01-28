from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.slayer import SlayerService
from backend.models import SlayerMaster
from backend.app.middleware import limiter
from backend.config import settings

router = APIRouter(prefix="/slayer", tags=["Slayer"])


@router.get("/masters")
@limiter.limit(settings.default_rate_limit)
def get_slayer_masters(request: Request, session: Session = Depends(get_session)):
    """Get list of Slayer Masters."""
    service = SlayerService(session)
    return service.get_masters()


@router.get("/tasks/{master}")
@limiter.limit(settings.default_rate_limit)
def get_master_tasks(
    request: Request, master: SlayerMaster, session: Session = Depends(get_session)
):
    """Get tasks for a specific master."""
    service = SlayerService(session)
    return service.get_tasks(master)


@router.get(
    "/location/{task_id}",
    response_model=None,
    responses={
        200: {
            "description": "Location information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "task_id": 123,
                        "monster_name": "Abyssal demon",
                        "category": "Abyssal demons",
                        "master": "Duradel",
                        "locations": [
                            {
                                "name": "Slayer Tower",
                                "requirements": [],
                                "multi_combat": True,
                                "cannon": False,
                                "safespot": False,
                                "notes": "Most popular location",
                                "pros": ["Close to bank"],
                                "cons": ["Can be crowded"],
                                "best_for": "Melee training",
                            }
                        ],
                        "alternatives": [],
                        "strategy": "Use Arclight for bonus damage",
                        "weakness": ["Slash", "Demonbane"],
                        "items_needed": [],
                        "has_detailed_data": True,
                    }
                }
            },
        },
        404: {
            "description": "Task not found",
            "content": {"application/json": {"example": {"detail": "Task not found"}}},
        },
    },
)
@limiter.limit(settings.default_rate_limit)
def get_task_location(request: Request, task_id: int, session: Session = Depends(get_session)):
    """Get detailed location information for a slayer task.

    Returns comprehensive location data including:
    - Available locations with detailed metadata
    - Requirements for each location (quests, favors, etc.)
    - Combat type (multi-combat vs single-combat)
    - Cannon and safespot availability
    - Pros and cons for each location
    - Alternative monsters that count for the task
    - Strategy recommendations and optimal setup
    - Monster weaknesses and required items

    Args:
        task_id: The slayer task ID to get locations for

    Returns:
        Dictionary with location information, strategy, and requirements

    Raises:
        HTTPException: 404 if task not found
    """
    service = SlayerService(session)
    result = service.get_task_locations(task_id)

    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])

    return result


@router.get("/advice/{task_id}")
@limiter.limit(settings.default_rate_limit)
def get_task_advice(
    request: Request,
    task_id: int,
    slayer_level: int = Query(1, ge=1, le=99, description="Player's Slayer level"),
    combat_level: int = Query(3, ge=3, le=126, description="Player's Combat level"),
    session: Session = Depends(get_session),
):
    """Get advice (Block/Skip/Do) for a task based on player stats.

    Args:
        task_id: The slayer task ID
        slayer_level: Player's slayer level (1-99)
        combat_level: Player's combat level (3-126)

    Returns:
        Task advice with recommendation (DO/SKIP/BLOCK) and reasoning
    """
    service = SlayerService(session)
    user_stats = {"slayer": slayer_level, "combat": combat_level}

    result = service.suggest_action(task_id, user_stats)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
