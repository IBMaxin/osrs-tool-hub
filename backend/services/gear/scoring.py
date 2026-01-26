"""Item scoring utilities for combat styles."""
from typing import Optional

from backend.models import Item


def score_item_for_style(
    item: Item, 
    combat_style: str, 
    attack_type: Optional[str] = None
) -> float:
    """
    Score an item for a specific combat style.
    
    Args:
        item: Item to score
        combat_style: Combat style (melee, ranged, magic)
        attack_type: For melee, specify attack type (stab, slash, crush)
        
    Returns:
        Score value (higher is better)
    """
    if combat_style == "melee":
        if attack_type == "stab":
            attack_bonus = item.attack_stab
        elif attack_type == "slash":
            attack_bonus = item.attack_slash
        elif attack_type == "crush":
            attack_bonus = item.attack_crush
        else:
            # Default to best melee attack bonus
            attack_bonus = max(item.attack_stab, item.attack_slash, item.attack_crush)
        return item.melee_strength * 4 + attack_bonus
    elif combat_style == "ranged":
        return item.ranged_strength * 4 + item.attack_ranged
    elif combat_style == "magic":
        return item.magic_damage * 10 + item.attack_magic
    elif combat_style == "prayer":
        return item.prayer_bonus * 10
    return 0.0
