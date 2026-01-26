from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from backend.database import get_session
from backend.services.slayer import SlayerService
from backend.models import SlayerMaster

router = APIRouter(prefix="/slayer", tags=["Slayer"])

@router.get("/masters")
def get_slayer_masters(session: Session = Depends(get_session)):
    """Get list of Slayer Masters."""
    service = SlayerService(session)
    return service.get_masters()

@router.get("/tasks/{master}")
def get_master_tasks(
    master: SlayerMaster,
    session: Session = Depends(get_session)
):
    """Get tasks for a specific master."""
    service = SlayerService(session)
    return service.get_tasks(master)

@router.get("/advice/{task_id}")
def get_task_advice(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Get advice (Block/Skip/Do) for a task."""
    service = SlayerService(session)
    # Mock user stats for now - in future extract from auth token or query param
    user_stats = {"slayer": 85, "combat": 110} 
    
    result = service.suggest_action(task_id, user_stats)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result
