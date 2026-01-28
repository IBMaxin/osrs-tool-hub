"""Item and price models."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    """Item model for OSRS items."""

    id: int = Field(primary_key=True)
    name: str
    members: bool = True
    limit: Optional[int] = None  # Buy limit (GE limit)
    value: int = 0
    icon_url: Optional[str] = None

    # Denormalized price fields for performance (synced from PriceSnapshot)
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    high_time: Optional[int] = None  # Unix timestamp
    low_time: Optional[int] = None  # Unix timestamp
    buy_limit: Optional[int] = None  # Alias for limit, kept for compatibility

    # Equipment Slot (head, cape, neck, etc)
    slot: Optional[str] = None

    # Requirements
    attack_req: int = 1
    strength_req: int = 1
    defence_req: int = 1
    ranged_req: int = 1
    magic_req: int = 1
    prayer_req: int = 1
    slayer_req: int = 0

    # Quest/Achievement requirements
    quest_req: Optional[str] = None  # e.g., "Recipe for Disaster"
    achievement_req: Optional[str] = None  # e.g., "Fight Caves"

    # Equipment metadata
    is_2h: bool = False  # True if weapon is two-handed
    attack_speed: int = 4  # Default attack speed (ticks)

    # Alternative/Variant tracking
    variant_of: Optional[int] = Field(
        default=None, foreign_key="item.id"
    )  # Points to base item (e.g., Tentacle -> Whip)

    # Offensive Stats
    attack_stab: int = 0
    attack_slash: int = 0
    attack_crush: int = 0
    attack_magic: int = 0
    attack_ranged: int = 0

    # Strength Bonuses
    melee_strength: int = 0
    ranged_strength: int = 0
    magic_damage: int = 0
    prayer_bonus: int = 0

    # Defensive Stats
    defence_stab: int = 0
    defence_slash: int = 0
    defence_crush: int = 0
    defence_magic: int = 0
    defence_ranged: int = 0


class PriceSnapshot(SQLModel, table=True):
    """Price snapshot model for tracking item prices over time."""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="item.id")
    high_price: Optional[int] = None
    low_price: Optional[int] = None
    high_volume: Optional[int] = None
    low_volume: Optional[int] = None
    high_time: Optional[int] = None  # Unix timestamp
    low_time: Optional[int] = None  # Unix timestamp
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def high(self) -> Optional[int]:
        """Backward compatibility alias for high_price."""
        return self.high_price

    @property
    def low(self) -> Optional[int]:
        """Backward compatibility alias for low_price."""
        return self.low_price
