"""Slayer monster definitions."""
from backend.models import Monster


def get_monster_definitions() -> list[Monster]:
    """
    Get all monster definitions for seeding.
    
    Returns:
        List of Monster instances
    """
    return [
        Monster(id=415, name="Abyssal demon", combat_level=124, hitpoints=150, slayer_xp=150, slayer_category="Abyssal demons", is_demon=True),
        Monster(id=11, name="Aberrant spectre", combat_level=96, hitpoints=90, slayer_xp=90, slayer_category="Aberrant spectres"),
        Monster(id=498, name="Smoke devil", combat_level=160, hitpoints=185, slayer_xp=185, slayer_category="Smoke devils"),
        Monster(id=122, name="Gargoyle", combat_level=111, hitpoints=105, slayer_xp=105, slayer_category="Gargoyles"),
        Monster(id=16, name="Nechryael", combat_level=115, hitpoints=105, slayer_xp=105, slayer_category="Nechryaels", is_demon=True),
        Monster(id=120, name="Bloodveld", combat_level=76, hitpoints=120, slayer_xp=120, slayer_category="Bloodvelds"),
        Monster(id=54, name="Dagannoth", combat_level=90, hitpoints=70, slayer_xp=70, slayer_category="Dagannoth"),
        Monster(id=10, name="Kalphite", combat_level=28, hitpoints=40, slayer_xp=40, slayer_category="Kalphite", is_kalphite=True),
        Monster(id=4, name="Hellhound", combat_level=122, hitpoints=116, slayer_xp=116, slayer_category="Hellhounds", is_demon=True),
        Monster(id=9, name="Dust devil", combat_level=93, hitpoints=105, slayer_xp=105, slayer_category="Dust devils"),
        Monster(id=14, name="Wyrm", combat_level=62, hitpoints=100, slayer_xp=133.2, slayer_category="Wyrms", is_dragon=True),
        Monster(id=15, name="Drake", combat_level=84, hitpoints=250, slayer_xp=316.8, slayer_category="Drakes", is_dragon=True),
        Monster(id=24, name="Hydra", combat_level=194, hitpoints=300, slayer_xp=660, slayer_category="Hydras", is_dragon=True),
        Monster(id=31, name="Kraken", combat_level=291, hitpoints=255, slayer_xp=255, slayer_category="Kraken"),
    ]
