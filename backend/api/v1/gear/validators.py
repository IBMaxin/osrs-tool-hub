"""Validation helpers for gear API."""
from fastapi import HTTPException, status


VALID_COMBAT_STYLES = ["melee", "ranged", "magic"]


def validate_combat_style(combat_style: str) -> None:
    """
    Validate combat style parameter.
    
    Args:
        combat_style: Combat style to validate
        
    Raises:
        HTTPException: If combat style is invalid
    """
    if combat_style not in VALID_COMBAT_STYLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid combat style: {combat_style}. Must be one of: {', '.join(VALID_COMBAT_STYLES)}"
        )
