"""Item requirement checking utilities."""
from typing import Dict, Optional, Set

from backend.models import Item


def meets_requirements(
    item: Item,
    stats: Dict[str, int],
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None
) -> bool:
    """
    Check if item meets all requirements (stats, quests, achievements).
    
    Args:
        item: Item to check
        stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
        quests_completed: Set of completed quest names (optional)
        achievements_completed: Set of completed achievement names (optional)
        
    Returns:
        True if item meets all requirements
    """
    # Check stat requirements
    if stats.get("attack", 1) < item.attack_req:
        return False
    if stats.get("strength", 1) < item.strength_req:
        return False
    if stats.get("defence", 1) < item.defence_req:
        return False
    if stats.get("ranged", 1) < item.ranged_req:
        return False
    if stats.get("magic", 1) < item.magic_req:
        return False
    if stats.get("prayer", 1) < item.prayer_req:
        return False
    
    # Check quest requirement
    if item.quest_req:
        if quests_completed is None or item.quest_req not in quests_completed:
            return False
    
    # Check achievement requirement
    if item.achievement_req:
        if achievements_completed is None or item.achievement_req not in achievements_completed:
            return False
    
    return True
