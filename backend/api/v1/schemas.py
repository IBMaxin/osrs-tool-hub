"""Shared Pydantic schemas for API v1 responses."""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error detail model for consistent error responses."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response schema for all API errors."""

    error: ErrorDetail
