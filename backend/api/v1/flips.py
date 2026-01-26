from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from backend.database import get_session
from backend.services.flipping import FlippingService
from typing import List, Optional

router = APIRouter(prefix="/flips", tags=["Flipping"])

@router.get("/opportunities")
def get_flips(
    max_budget: Optional[int] = Query(None, description="Max budget in GP"),
    min_roi: float = Query(1.0, description="Minimum ROI %"),
    min_volume: int = Query(0, description="Minimum volume"),
    session: Session = Depends(get_session)
):
    service = FlippingService(session)
    return service.get_flip_opportunities(
        max_budget=max_budget, 
        min_roi=min_roi, 
        min_volume=min_volume
    )
