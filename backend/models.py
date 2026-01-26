"""Database models."""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GearSet(SQLModel, table=True):
    """Gear set model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    items: str  # JSON string of item IDs and quantities
    total_cost: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Item(SQLModel, table=True):
    """Item model for OSRS items."""
    id: int = Field(primary_key=True)
    name: str
    members: bool = True
    limit: Optional[int] = None
    value: int = 0
    icon_url: Optional[str] = None
    slot: Optional[str] = None
    
    # Requirements
    attack_req: int = 1
    strength_req: int = 1
    defence_req: int = 1
    ranged_req: int = 1
    magic_req: int = 1
    prayer_req: int = 1
    slayer_req: int = 0
    quest_req: Optional[str] = None
    achievement_req: Optional[str] = None
    
    # Equipment metadata
    is_2h: bool = False
    attack_speed: int = 4
    variant_of: Optional[int] = Field(default=None, foreign_key="item.id")
    
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
    high_time: Optional[int] = None
    low_time: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def high(self) -> Optional[int]:
        return self.high_price
    
    @property
    def low(self) -> Optional[int]:
        return self.low_price


# --- Slayer & Monster Models ---

class Monster(SQLModel, table=True):
    """Monster model for Slayer and DPS calculations."""
    id: int = Field(primary_key=True)  # Wiki ID or custom ID
    name: str
    level: int
    slayer_level: int = 1
    is_slayer_monster: bool = False
    
    # Defensive Stats (for DPS calc)
    hitpoints: int
    defence_level: int
    magic_level: int
    
    # Defensive Bonuses
    defence_stab: int = 0
    defence_slash: int = 0
    defence_crush: int = 0
    defence_magic: int = 0
    defence_ranged: int = 0
    
    # Attributes for item effectiveness
    is_undead: bool = False      # Salve amulet
    is_demon: bool = False       # Arclight/Demonbane
    is_dragon: bool = False      # Dragon hunter weapons
    is_kalphite: bool = False    # Keris
    is_leafy: bool = False       # Leaf-bladed weapons
    is_vampyre: bool = False     # Blisterwood/Ivandis
    
    image_url: Optional[str] = None
    wiki_url: Optional[str] = None


class SlayerMaster(SQLModel, table=True):
    """Slayer Master model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    combat_level_req: int = 1
    slayer_level_req: int = 1
    image_url: Optional[str] = None
    
    tasks: List["SlayerTask"] = Relationship(back_populates="master")


class SlayerTask(SQLModel, table=True):
    """Link between Master and Monster for task assignment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    master_id: int = Field(foreign_key="slayermaster.id")
    monster_id: int = Field(foreign_key="monster.id")
    
    # Task properties
    weight: int  # Likelihood of assignment
    amount_min: int
    amount_max: int
    is_boss: bool = False
    
    # Relationships
    master: SlayerMaster = Relationship(back_populates="tasks")
    monster: Monster = Relationship()
