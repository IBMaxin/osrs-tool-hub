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
    import logging
    from sqlmodel import select, func
    from backend.models import SlayerTask, Monster
    
    logger = logging.getLogger(__name__)
    logger.info(f"Getting tasks for master: {master} (type: {type(master)}, value: {master.value})")
    
    # Debug: Check what's in the database
    task_count = session.exec(select(func.count(SlayerTask.id)).where(SlayerTask.master == master)).one()
    logger.info(f"Total tasks in DB for {master}: {task_count}")
    
    service = SlayerService(session)
    tasks = service.get_tasks(master)
    logger.info(f"Returning {len(tasks)} tasks for {master}")
    
    if len(tasks) == 0 and task_count > 0:
        logger.warning(f"WARNING: Database has {task_count} tasks but service returned 0!")
        # Try direct query as fallback
        query = select(SlayerTask, Monster).join(Monster).where(SlayerTask.master == master)
        results = session.exec(query).all()
        logger.info(f"Direct query returned {len(results)} results")
        if results:
            tasks = [{
                "task_id": task.id,
                "monster_name": monster.name,
                "monster_id": monster.id,
                "category": task.category,
                "amount": f"{task.quantity_min}-{task.quantity_max}",
                "weight": task.weight,
                "combat_level": monster.combat_level,
                "slayer_xp": monster.slayer_xp,
                "is_skippable": task.is_skippable,
                "is_blockable": task.is_blockable
            } for task, monster in results]
            tasks.sort(key=lambda x: x["weight"], reverse=True)
            logger.info(f"Fallback query returned {len(tasks)} tasks")
    
    return tasks

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
