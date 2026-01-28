"""Watchlist endpoints for managing item watchlists and alerts."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from sqlmodel import Session

from backend.database import get_session
from backend.services.watchlist import WatchlistService
from backend.app.middleware import limiter
from backend.config import settings
from pydantic import BaseModel, Field, field_validator


router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


class WatchlistCreateRequest(BaseModel):
    """Request model for creating a watchlist item."""

    user_id: str = Field(..., description="User identifier (UUID from localStorage)")
    item_id: int = Field(..., gt=0, description="OSRS item ID")
    alert_type: str = Field(
        ..., description="Alert type: 'price_below', 'price_above', or 'margin_above'"
    )
    threshold: int = Field(
        ..., gt=0, description="Threshold value for alert (price or margin in GP)"
    )

    @field_validator("alert_type")
    @classmethod
    def validate_alert_type(cls, v: str) -> str:
        """Validate alert type."""
        valid_types = ("price_below", "price_above", "margin_above")
        if v not in valid_types:
            raise ValueError(f"Alert type must be one of: {', '.join(valid_types)}")
        return v


class WatchlistItemResponse(BaseModel):
    """Response model for a watchlist item."""

    id: int
    user_id: str
    item_id: int
    item_name: str
    alert_type: str
    threshold: int
    is_active: bool
    created_at: str
    last_triggered_at: Optional[str] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class WatchlistAlertResponse(BaseModel):
    """Response model for a watchlist alert."""

    id: int
    watchlist_item_id: int
    triggered_at: str
    current_value: int
    threshold_value: int
    message: str

    class Config:
        """Pydantic config."""

        from_attributes = True


@router.post("", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.default_rate_limit)
def add_to_watchlist(
    request: Request,
    watchlist_data: WatchlistCreateRequest,
    session: Session = Depends(get_session),
) -> WatchlistItemResponse:
    """
    Add an item to the watchlist with alert rules.

    Args:
        request: FastAPI request object (for rate limiting)
        watchlist_data: Watchlist creation data
        session: Database session

    Returns:
        Created watchlist item object

    Raises:
        HTTPException: If validation fails or item not found
    """
    try:
        service = WatchlistService(session)
        watchlist_item = service.add_to_watchlist(
            user_id=watchlist_data.user_id,
            item_id=watchlist_data.item_id,
            alert_type=watchlist_data.alert_type,
            threshold=watchlist_data.threshold,
        )
        return WatchlistItemResponse.model_validate(
            {
                **watchlist_item.model_dump(),
                "created_at": (
                    watchlist_item.created_at.isoformat() if watchlist_item.created_at else None
                ),
                "last_triggered_at": (
                    watchlist_item.last_triggered_at.isoformat()
                    if watchlist_item.last_triggered_at
                    else None
                ),
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("", response_model=List[WatchlistItemResponse])
@limiter.limit(settings.default_rate_limit)
def get_watchlist(
    request: Request,
    user_id: str = Query(..., description="User identifier"),
    include_inactive: bool = Query(False, description="Include inactive watchlist items"),
    session: Session = Depends(get_session),
) -> List[WatchlistItemResponse]:
    """
    Get user's watchlist.

    Args:
        request: FastAPI request object (for rate limiting)
        user_id: User identifier (required)
        include_inactive: If True, include inactive watchlist items
        session: Database session

    Returns:
        List of watchlist items
    """
    service = WatchlistService(session)
    watchlist_items = service.get_watchlist(user_id=user_id, include_inactive=include_inactive)
    return [
        WatchlistItemResponse.model_validate(
            {
                **item.model_dump(),
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "last_triggered_at": (
                    item.last_triggered_at.isoformat() if item.last_triggered_at else None
                ),
            }
        )
        for item in watchlist_items
    ]


@router.delete("/{watchlist_item_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.default_rate_limit)
def remove_from_watchlist(
    request: Request,
    watchlist_item_id: int,
    user_id: str = Query(..., description="User identifier"),
    session: Session = Depends(get_session),
) -> None:
    """
    Remove an item from the watchlist (deactivate it).

    Args:
        request: FastAPI request object (for rate limiting)
        watchlist_item_id: Watchlist item ID
        user_id: User identifier (for security check)
        session: Database session

    Raises:
        HTTPException: If watchlist item not found or doesn't belong to user
    """
    try:
        service = WatchlistService(session)
        removed = service.remove_from_watchlist(
            watchlist_item_id=watchlist_item_id, user_id=user_id
        )
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Watchlist item not found",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/alerts", response_model=List[WatchlistAlertResponse])
@limiter.limit(settings.default_rate_limit)
def get_alerts(
    request: Request,
    user_id: str = Query(..., description="User identifier"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of alerts"),
    session: Session = Depends(get_session),
) -> List[WatchlistAlertResponse]:
    """
    Get triggered alerts for a user.

    Args:
        request: FastAPI request object (for rate limiting)
        user_id: User identifier (required)
        limit: Maximum number of alerts to return (1-1000)
        session: Database session

    Returns:
        List of triggered alerts sorted by triggered_at descending
    """
    service = WatchlistService(session)
    alerts = service.get_alerts(user_id=user_id, limit=limit)
    return [
        WatchlistAlertResponse.model_validate(
            {
                **alert.model_dump(),
                "triggered_at": alert.triggered_at.isoformat() if alert.triggered_at else None,
            }
        )
        for alert in alerts
    ]
