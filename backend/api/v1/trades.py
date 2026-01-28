"""Trade endpoints for logging and tracking user transactions."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from sqlmodel import Session

from backend.database import get_session
from backend.services.trade import TradeService
from backend.app.middleware import limiter
from backend.config import settings
from pydantic import BaseModel, Field, field_validator


router = APIRouter(prefix="/trades", tags=["Trades"])


class TradeCreateRequest(BaseModel):
    """Request model for creating a trade."""

    user_id: str = Field(..., description="User identifier (UUID from localStorage)")
    item_id: int = Field(..., gt=0, description="OSRS item ID")
    buy_price: int = Field(..., gt=0, description="Price per item when bought")
    quantity: int = Field(..., gt=0, description="Quantity of items")
    sell_price: Optional[int] = Field(None, gt=0, description="Optional price per item when sold")
    status: str = Field(
        default="bought", description="Trade status: 'bought', 'sold', or 'cancelled'"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate trade status."""
        valid_statuses = ("bought", "sold", "cancelled")
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v


class TradeResponse(BaseModel):
    """Response model for a trade."""

    id: int
    user_id: str
    item_id: int
    item_name: str
    buy_price: int
    sell_price: Optional[int]
    quantity: int
    profit: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TradeStatsResponse(BaseModel):
    """Response model for trade statistics."""

    total_profit: int
    total_trades: int
    sold_trades: int
    profit_per_hour: float
    best_items: List[dict]
    profit_by_item: dict


@router.post("", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.default_rate_limit)
def create_trade(
    request: Request,
    trade_data: TradeCreateRequest,
    session: Session = Depends(get_session),
) -> TradeResponse:
    """
    Log a buy/sell transaction.

    Args:
        request: FastAPI request object (for rate limiting)
        trade_data: Trade creation data
        session: Database session

    Returns:
        Created trade object

    Raises:
        HTTPException: If validation fails or item not found
    """
    try:
        service = TradeService(session)
        trade = service.log_trade(
            user_id=trade_data.user_id,
            item_id=trade_data.item_id,
            buy_price=trade_data.buy_price,
            quantity=trade_data.quantity,
            sell_price=trade_data.sell_price,
            status=trade_data.status,
        )
        return TradeResponse.model_validate(trade)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("", response_model=List[TradeResponse])
@limiter.limit(settings.default_rate_limit)
def get_trades(
    request: Request,
    user_id: str = Query(..., description="User identifier"),
    status: Optional[str] = Query(
        None, description="Filter by status: 'bought', 'sold', 'cancelled'"
    ),
    item_id: Optional[int] = Query(None, gt=0, description="Filter by item ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (ISO format)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    session: Session = Depends(get_session),
) -> List[TradeResponse]:
    """
    Get user's trade history with optional filters.

    Args:
        request: FastAPI request object (for rate limiting)
        user_id: User identifier (required)
        status: Optional filter by status
        item_id: Optional filter by item ID
        start_date: Optional filter by start date
        end_date: Optional filter by end date
        limit: Maximum number of results (1-1000)
        session: Database session

    Returns:
        List of trade objects sorted by created_at descending

    Raises:
        HTTPException: If validation fails
    """
    try:
        service = TradeService(session)
        trades = service.get_trade_history(
            user_id=user_id,
            status=status,
            item_id=item_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )
        return [TradeResponse.model_validate(trade) for trade in trades]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/stats", response_model=TradeStatsResponse)
@limiter.limit(settings.default_rate_limit)
def get_trade_stats(
    request: Request,
    user_id: str = Query(..., description="User identifier"),
    days: Optional[int] = Query(
        None, ge=1, description="Number of days to look back (None = all time)"
    ),
    session: Session = Depends(get_session),
) -> TradeStatsResponse:
    """
    Get aggregate statistics for user's trades.

    Args:
        request: FastAPI request object (for rate limiting)
        user_id: User identifier (required)
        days: Optional number of days to look back
        session: Database session

    Returns:
        Dictionary with aggregate stats: total_profit, total_trades, sold_trades,
        profit_per_hour, best_items, profit_by_item
    """
    service = TradeService(session)
    stats = service.get_trade_stats(user_id=user_id, days=days)
    return TradeStatsResponse(**stats)
