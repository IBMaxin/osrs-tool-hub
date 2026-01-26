"""Slayer models."""
from typing import Optional

from sqlmodel import Field, SQLModel

from backend.models.enums import SlayerMaster


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
