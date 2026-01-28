"""Item requirement checking utilities."""

from typing import Dict, Optional, Set

from backend.models import Item


def meets_requirements(
    item: Item,
    stats: Dict[str, int],
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
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


def meets_content_requirements(item: Item, content_tag: Optional[str] = None) -> bool:
    """
    Check if item matches content tag requirements.

    Args:
        item: Item to check
        content_tag: Optional content tag to filter by (e.g., 'toa_entry', 'gwd')

    Returns:
        True if item matches content requirements (or no content tag specified)
    """
    if content_tag is None:
        return True

    # For now, we'll use a simple heuristic:
    # Items with certain names or properties match certain content tags
    # This can be expanded with a proper content_tag field in the Item model later
    content_mappings = {
        "toa_entry": ["Crystal", "Bow of Faerdhinen", "Blade of saeldor"],
        "gwd": ["Bandos", "Armadyl", "Zamorak", "Saradomin"],
    }

    if content_tag in content_mappings:
        matching_items = content_mappings[content_tag]
        return any(keyword.lower() in item.name.lower() for keyword in matching_items)

    # If content tag not recognized, allow all items
    return True


def is_ironman_compatible(item: Item) -> bool:
    """
    Check if item is obtainable on ironman mode.

    Note: This is a simplified check. A proper implementation would require
    a field in the Item model indicating if it's tradeable or obtainable on ironman.

    Args:
        item: Item to check

    Returns:
        True if item is ironman-compatible (obtainable without trading)
    """
    # For now, we'll assume all items are ironman-compatible
    # This can be enhanced with a proper tradeable/ironman field in the Item model
    # Common tradeable-only items that aren't ironman-compatible:
    # - Most high-end gear (can be obtained via drops)
    # - Some quest items (can be obtained via quests)
    # This is a placeholder - proper implementation would check item properties
    return True
