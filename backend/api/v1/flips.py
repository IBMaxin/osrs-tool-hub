from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from backend.database import get_session
from backend.services.flipping import FlippingService, FlipOpportunity
from backend.app.middleware import limiter
from backend.config import settings
from backend.api.v1.validators import BudgetQuery, ROIQuery, VolumeQuery
from typing import List, Optional

router = APIRouter(prefix="/flips", tags=["Flipping"])

# Legacy router for backward compatibility with old tests
flipping_router = APIRouter(prefix="/flipping", tags=["Flipping"])


@router.get(
    "/opportunities",
    response_model=List[FlipOpportunity],
    summary="Get flip opportunities",
    description="Find profitable Grand Exchange flip opportunities based on budget, ROI, and volume filters. Results are sorted by potential profit.",
    responses={
        200: {
            "description": "List of flip opportunities",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "item_id": 4151,
                            "item_name": "Abyssal whip",
                            "buy_price": 1200000,
                            "sell_price": 1250000,
                            "profit": 25000,
                            "roi": 2.08,
                            "volume": 1500,
                            "limit": 8,
                        }
                    ]
                }
            },
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "HTTP_429",
                            "message": "Rate limit exceeded: 100 per 1 minute",
                        }
                    }
                }
            },
        },
    },
)
@limiter.limit(settings.default_rate_limit)
def get_flips(
    request: Request,
    max_budget: Optional[int] = BudgetQuery(None),
    min_roi: float = ROIQuery(0.0),
    min_volume: int = VolumeQuery(0),
    session: Session = Depends(get_session),
):
    """
    Get flip opportunities with validated parameters.

    **Rate Limit**: 100 requests per minute per IP

    **Example Request**:
    ```
    GET /api/v1/flips/opportunities?max_budget=10000000&min_roi=1.5&min_volume=100
    ```

    Args:
        request: FastAPI request object (for rate limiting)
        max_budget: Maximum budget in GP (0 to 2,147,483,647). Filters out items where buy_price * limit exceeds this value.
        min_roi: Minimum ROI percentage (0 to 10000). Filters out opportunities below this ROI.
        min_volume: Minimum volume (0 to 2,147,483,647). Filters out items with trade volume below this threshold.
        session: Database session

    Returns:
        List of flip opportunities sorted by potential profit (descending)

    Raises:
        HTTPException: 429 if rate limit exceeded
    """
    service = FlippingService(session)
    return service.get_flip_opportunities(
        max_budget=max_budget, min_roi=min_roi, min_volume=min_volume
    )


# Legacy scanner endpoint for backward compatibility with old tests
@flipping_router.get(
    "/scanner",
    response_model=List[FlipOpportunity],
    summary="[DEPRECATED] Get flip opportunities (legacy endpoint)",
    description="**DEPRECATED**: Use /api/v1/flips/opportunities instead. This endpoint exists for backward compatibility with older tests.",
    deprecated=True,
)
@limiter.limit(settings.default_rate_limit)
def get_scanner_flips(
    request: Request,
    budget: int = BudgetQuery(...),  # Required for legacy endpoint
    min_roi: float = ROIQuery(...),  # Required for legacy endpoint
    min_volume: int = VolumeQuery(...),  # Required for legacy endpoint
    session: Session = Depends(get_session),
):
    """
    Legacy scanner endpoint - redirects to get_flips logic.
    
    Args:
        budget: Maximum budget (legacy parameter name for max_budget) - REQUIRED
        min_roi: Minimum ROI - REQUIRED
        min_volume: Minimum volume - REQUIRED
    """
    service = FlippingService(session)
    return service.get_flip_opportunities(
        max_budget=budget, min_roi=min_roi, min_volume=min_volume
    )
