"""Pydantic schemas for gear API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel, field_validator, Field


class GearSetCreate(BaseModel):
    """Request model for creating a gear set."""

    name: str = Field(..., min_length=1, max_length=200, description="Gear set name")
    items: dict[int, int] = Field(..., description="Item ID to quantity mapping")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate gear set name."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: dict[int, int]) -> dict[int, int]:
        """Validate items dictionary."""
        if not v:
            raise ValueError("Items dictionary cannot be empty")
        if len(v) > 50:
            raise ValueError("Cannot have more than 50 items in a gear set")
        for item_id, quantity in v.items():
            if item_id < 0:
                raise ValueError(f"Item ID {item_id} must be non-negative")
            if quantity < 1:
                raise ValueError(f"Quantity for item {item_id} must be at least 1")
            if quantity > 10000:
                raise ValueError(f"Quantity for item {item_id} exceeds maximum (10000)")
        return v


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

    combat_style: str = Field(..., description="Combat style: melee, ranged, or magic")
    budget: int = Field(..., ge=0, le=2_147_483_647, description="Budget in GP")
    stats: dict[str, int] = Field(
        ..., description="Player stats: attack, strength, defence, ranged, magic, prayer"
    )
    attack_type: Optional[str] = Field(None, description="For melee: stab, slash, or crush")
    quests_completed: Optional[List[str]] = Field(None, description="List of completed quests")
    achievements_completed: Optional[List[str]] = Field(
        None, description="List of completed achievements"
    )
    exclude_slots: Optional[List[str]] = Field(
        None, description="Slots to exclude from calculation"
    )
    ironman: bool = Field(
        default=False, description="If True, filter out tradeable items (ironman mode)"
    )
    exclude_items: Optional[List[str]] = Field(
        None, description="List of item names to exclude from calculation"
    )
    content_tag: Optional[str] = Field(
        None, description="Filter by content tag (e.g., 'toa_entry', 'gwd')"
    )
    max_tick_manipulation: bool = Field(
        default=False,
        description="If True, filter out items requiring tick manipulation",
    )

    @field_validator("combat_style")
    @classmethod
    def validate_combat_style(cls, v: str) -> str:
        """Validate combat style."""
        valid_styles = ["melee", "ranged", "magic"]
        if v.lower() not in valid_styles:
            raise ValueError(f"Combat style must be one of: {', '.join(valid_styles)}")
        return v.lower()

    @field_validator("stats")
    @classmethod
    def validate_stats(cls, v: dict[str, int]) -> dict[str, int]:
        """Validate player stats."""
        valid_stats = ["attack", "strength", "defence", "ranged", "magic", "prayer"]
        for stat_name, stat_value in v.items():
            if stat_name.lower() not in valid_stats:
                raise ValueError(
                    f"Invalid stat: {stat_name}. Must be one of: {', '.join(valid_stats)}"
                )
            if stat_value < 1 or stat_value > 99:
                raise ValueError(f"Stat {stat_name} must be between 1 and 99")
        return {k.lower(): v for k, v in v.items()}

    @field_validator("attack_type")
    @classmethod
    def validate_attack_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate attack type."""
        if v is not None:
            valid_types = ["stab", "slash", "crush"]
            if v.lower() not in valid_types:
                raise ValueError(f"Attack type must be one of: {', '.join(valid_types)}")
            return v.lower()
        return v


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


class LoadoutInput(BaseModel):
    """Single loadout input for comparison."""

    name: str = Field(..., description="Loadout name/identifier")
    loadout: dict[str, Optional[int]] = Field(..., description="Dict of slot -> item_id")


class DPSComparisonRequest(BaseModel):
    """Request model for DPS comparison."""

    loadouts: List[LoadoutInput] = Field(
        ..., min_length=1, description="List of loadouts to compare"
    )
    combat_style: str = Field(..., description="Combat style: melee, ranged, or magic")
    attack_type: Optional[str] = Field(None, description="For melee: stab, slash, or crush")
    player_stats: Optional[dict[str, int]] = Field(
        None, description="Player combat stats: attack, strength, ranged, magic"
    )
    target_monster: Optional[dict] = Field(
        None, description="Optional monster stats for more accurate calculations"
    )

    @field_validator("combat_style")
    @classmethod
    def validate_combat_style(cls, v: str) -> str:
        """Validate combat style."""
        valid_styles = ["melee", "ranged", "magic"]
        if v.lower() not in valid_styles:
            raise ValueError(f"Combat style must be one of: {', '.join(valid_styles)}")
        return v.lower()

    @field_validator("loadouts")
    @classmethod
    def validate_loadouts(cls, v: List[LoadoutInput]) -> List[LoadoutInput]:
        """Validate loadouts list."""
        if len(v) < 1:
            raise ValueError("At least one loadout is required")
        if len(v) > 10:
            raise ValueError("Maximum 10 loadouts can be compared at once")
        return v


class DPSComparisonResult(BaseModel):
    """Single DPS comparison result."""

    loadout_id: int
    loadout_name: str
    dps: float
    max_hit: int
    attack_speed: int
    attack_speed_seconds: float
    accuracy: float
    total_attack_bonus: int
    total_strength_bonus: int
    dps_increase: Optional[float] = None
    dps_increase_percent: Optional[float] = None
    details: dict


class DPSComparisonResponse(BaseModel):
    """Response model for DPS comparison."""

    results: List[DPSComparisonResult]
