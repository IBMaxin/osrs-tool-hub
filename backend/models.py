"""Database models."""
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship


class SlayerMaster(str, Enum):
    TURAEL = "Turael"
    SPRIA = "Spria"
    MAZCHNA = "Mazchna"
    VANNAKA = "Vannaka"
    CHAELDAR = "Chaeldar"
    KONAR = "Konar"
    NIEVE = "Nieve"
    DURADEL = "Duradel"


class AttackStyle(str, Enum):
    STAB = "stab"
    SLASH = "slash"
    CRUSH = "crush"
    MAGIC = "magic"
    RANGED = "ranged"


class Monster(SQLModel, table=True):
    """Monster model for combat and slayer."""
    
    id: int = Field(primary_key=True)  # OSRSBox ID
    name: str
    combat_level: int
    hitpoints: int
    slayer_xp: float
    
    # Defensive Stats
    defence_level: int = 1
    magic_level: int = 1
    ranged_level: int = 1
    
    # Defensive Bonuses
    defence_stab: int = 0
    defence_slash: int = 0
    defence_crush: int = 0
    defence_magic: int = 0
    defence_ranged: int = 0
    
    # Slayer Metadata
    slayer_category: Optional[str] = None  # e.g., "Abyssal demons"
    is_slayer_monster: bool = False
    wiki_url: Optional[str] = None
    
    # Attributes
    is_dragon: bool = False
    is_demon: bool = False
    is_undead: bool = False
    is_kalphite: bool = False


class SlayerTask(SQLModel, table=True):
    """Slayer task configuration."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    master: SlayerMaster
    monster_id: int = Field(foreign_key="monster.id")
    category: str
    quantity_min: int
    quantity_max: int
    weight: int
    
    # Task properties
    is_skippable: bool = True
    is_blockable: bool = True
    
    # Relationships
    # monster: Optional[Monster] = Relationship()


class Flip(SQLModel, table=True):
    """Flip tracking model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int
    item_name: str
    buy_price: int
    sell_price: int
    profit: int
    profit_percent: float
    volume: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GearSet(SQLModel, table=True):
    """Gear set model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    items: str  # JSON string of item IDs and quantities
    total_cost: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Item(SQLModel, table=True):
    """Item model for OSRS items."""

    id: int = Field(primary_key=True)
    name: str
    members: bool = True
    limit: Optional[int] = None
    value: int = 0
    icon_url: Optional[str] = None
    
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
    variant_of: Optional[int] = Field(default=None, foreign_key="item.id")  # Points to base item (e.g., Tentacle -> Whip)
    
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
