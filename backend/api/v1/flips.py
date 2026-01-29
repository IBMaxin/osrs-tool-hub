from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from backend.database import get_session
from backend.services.flipping import FlippingService, FlipOpportunity
from backend.app.middleware import limiter
from backend.config import settings
from backend.api.v1.validators import BudgetQuery, ROIQuery, VolumeQuery
from typing import List, Optional

router = APIRouter(prefix="/flips", tags=["Flipping"])


@router.get("/opportunities", response_model=List[FlipOpportunity])
@limiter.limit(settings.default_rate_limit)
def get_flips(
    request: Request,
    max_budget: Optional[int] = BudgetQuery(None),
    min_roi: float = ROIQuery(0.0),
    min_volume: int = VolumeQuery(0),
    session: Session = Depends(get_session),
) -> List[FlipOpportunity]:
    """
    Get flip opportunities with validated parameters.

    Args:
        request: FastAPI request object (for rate limiting)
        max_budget: Maximum budget in GP (0 to 2,147,483,647)
        min_roi: Minimum ROI percentage (0 to 10000)
        min_volume: Minimum volume (0 to 2,147,483,647)
        session: Database session

    Returns:
        List of flip opportunities
    """
    service = FlippingService(session)
    budget = max_budget if max_budget is not None else 2_147_483_647
    return service.find_best_flips(budget=budget, min_roi=min_roi, min_volume=min_volume)
