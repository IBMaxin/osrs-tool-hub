"""Input validation utilities for API endpoints."""

from fastapi import HTTPException, Query, status
from typing import Optional


def validate_budget(budget: Optional[int]) -> Optional[int]:
    """
    Validate budget parameter.

    Args:
        budget: Budget value in GP

    Returns:
        Validated budget value

    Raises:
        HTTPException: If budget is invalid
    """
    if budget is not None:
        if budget < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Budget must be non-negative"
            )
        if budget > 2_147_483_647:  # Max 32-bit signed integer (GP limit)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Budget exceeds maximum allowed value",
            )
    return budget


def validate_roi(roi: float) -> float:
    """
    Validate ROI parameter.

    Args:
        roi: ROI percentage

    Returns:
        Validated ROI value

    Raises:
        HTTPException: If ROI is invalid
    """
    if roi < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ROI must be non-negative"
        )
    if roi > 10000:  # Reasonable upper limit (10000%)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ROI exceeds maximum allowed value (10000%)",
        )
    return roi


def validate_volume(volume: int) -> int:
    """
    Validate volume parameter.

    Args:
        volume: Volume value

    Returns:
        Validated volume value

    Raises:
        HTTPException: If volume is invalid
    """
    if volume < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Volume must be non-negative"
        )
    if volume > 2_147_483_647:  # Max 32-bit signed integer
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Volume exceeds maximum allowed value"
        )
    return volume


def validate_level(level: int, min_level: int = 1, max_level: int = 99) -> int:
    """
    Validate skill level parameter.

    Args:
        level: Skill level
        min_level: Minimum allowed level
        max_level: Maximum allowed level

    Returns:
        Validated level value

    Raises:
        HTTPException: If level is invalid
    """
    if level < min_level or level > max_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Level must be between {min_level} and {max_level}",
        )
    return level


def validate_item_id(item_id: int) -> int:
    """
    Validate item ID parameter.

    Args:
        item_id: Item ID

    Returns:
        Validated item ID

    Raises:
        HTTPException: If item ID is invalid
    """
    if item_id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID must be non-negative"
        )
    if item_id > 2_147_483_647:  # Max 32-bit signed integer
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID exceeds maximum allowed value"
        )
    return item_id


def validate_string_length(value: str, max_length: int, field_name: str = "Field") -> str:
    """
    Validate string length.

    Args:
        value: String value to validate
        max_length: Maximum allowed length
        field_name: Name of the field for error messages

    Returns:
        Validated string value

    Raises:
        HTTPException: If string is too long
    """
    if len(value) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} exceeds maximum length of {max_length} characters",
        )
    return value


def validate_slot(slot: str) -> str:
    """
    Validate equipment slot parameter.

    Args:
        slot: Equipment slot name

    Returns:
        Validated slot name

    Raises:
        HTTPException: If slot is invalid
    """
    valid_slots = [
        "head",
        "cape",
        "neck",
        "ammo",
        "weapon",
        "shield",
        "body",
        "legs",
        "gloves",
        "boots",
        "ring",
        "two_handed",
    ]

    if slot.lower() not in valid_slots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid slot: {slot}. Must be one of: {', '.join(valid_slots)}",
        )
    return slot.lower()


# Query parameter validators using FastAPI Query
def BudgetQuery(default: Optional[int] = None, **kwargs):
    """Create a validated budget query parameter."""
    return Query(
        default,
        ge=0,
        le=2_147_483_647,
        description="Max budget in GP (0 to 2,147,483,647)",
        **kwargs,
    )


def ROIQuery(default: float = 0.0, **kwargs):
    """Create a validated ROI query parameter."""
    return Query(
        default, ge=0.0, le=10000.0, description="Minimum ROI percentage (0 to 10000)", **kwargs
    )


def VolumeQuery(default: int = 0, **kwargs):
    """Create a validated volume query parameter."""
    return Query(
        default, ge=0, le=2_147_483_647, description="Minimum volume (0 to 2,147,483,647)", **kwargs
    )


def LevelQuery(default: int = 1, min_level: int = 1, max_level: int = 99, **kwargs):
    """Create a validated level query parameter."""
    return Query(
        default,
        ge=min_level,
        le=max_level,
        description=f"Level ({min_level} to {max_level})",
        **kwargs,
    )
