"""Pydantic schemas for gear API requests and responses."""
from typing import List, Optional
from pydantic import BaseModel


class GearSetCreate(BaseModel):
    """Request model for creating a gear set."""

    name: str
    items: dict[int, int]  # item_id -> quantity
    description: Optional[str] = None


class GearSetResponse(BaseModel):
    """Response model for gear set."""

    id: int
    name: str
    description: Optional[str]
    items: dict[int, int]
    total_cost: int
    created_at: str
    updated_at: str

    class Config:
        """Pydantic config."""

        from_attributes = True


class BestLoadoutRequest(BaseModel):
    """Request model for best loadout calculation."""
    combat_style: str
    budget: int
    stats: dict[str, int]  # attack, strength, defence, ranged, magic, prayer
    attack_type: Optional[str] = None  # For melee: stab, slash, crush
    quests_completed: Optional[List[str]] = None
    achievements_completed: Optional[List[str]] = None
    exclude_slots: Optional[List[str]] = None


class UpgradePathRequest(BaseModel):
    """Request model for upgrade path calculation."""
    current_loadout: dict[str, Optional[int]]  # slot -> item_id
    combat_style: str
    budget: int
    stats: dict[str, int]
    attack_type: Optional[str] = None
    quests_completed: Optional[List[str]] = None
    achievements_completed: Optional[List[str]] = None


class DPSRequest(BaseModel):
    """Request model for DPS calculation."""
    loadout: dict[str, Optional[int]]  # slot -> item_id
    combat_style: str
    attack_type: Optional[str] = None
    player_stats: Optional[dict[str, int]] = None  # attack, strength, ranged, magic
