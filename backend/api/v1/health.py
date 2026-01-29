"""Health check endpoint for monitoring and load balancers."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, text
from pydantic import BaseModel
from typing import Optional

from backend.db.session import get_session
from backend.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str
    database: str
    external_api: Optional[str] = None
    version: str = "1.0.0"


@router.get("", response_model=HealthCheckResponse)
async def health_check(session: Session = Depends(get_session)) -> HealthCheckResponse:
    """
    Health check endpoint for monitoring and load balancers.

    Checks:
    - Database connectivity
    - External API (OSRS Wiki) availability

    Returns:
        Health status with component statuses

    Raises:
        HTTPException: 503 if any critical component is unhealthy
    """
    health_status = "healthy"
    database_status = "ok"
    external_api_status: Optional[str] = None

    # Check database connectivity
    try:
        result = session.exec(text("SELECT 1")).one()
        # SQLModel returns Row objects for SELECT queries, which are tuple-like
        # Extract the scalar value - Row objects support indexing
        try:
            scalar_value = result[0] if hasattr(result, '__getitem__') else result
        except (TypeError, IndexError):
            scalar_value = result
        if scalar_value != 1:
            database_status = "error"
            health_status = "unhealthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        database_status = "error"
        health_status = "unhealthy"

    # Check external API (OSRS Wiki) availability
    try:
        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            # Try a lightweight endpoint
            response = await client.get(
                f"{settings.wiki_api_base}/latest",
                headers={"User-Agent": settings.user_agent},
            )
            if response.status_code == 200:
                external_api_status = "ok"
            else:
                external_api_status = "degraded"
                # Don't mark as unhealthy, external API issues are non-critical
    except Exception as e:
        logger.warning(f"External API health check failed: {e}")
        external_api_status = "unavailable"
        # Don't mark as unhealthy, external API issues are non-critical

    # If database is down, return 503
    if database_status == "error":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )

    return HealthCheckResponse(
        status=health_status,
        database=database_status,
        external_api=external_api_status,
        version="1.0.0",
    )
