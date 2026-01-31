"""Wiki progression data loader and accessors."""

import json
from pathlib import Path
from typing import Any

# Path to JSON data files
_DATA_DIR = Path(__file__).parent.parent / "data" / "wiki_progression"


def _load_progression_data() -> dict:
    """
    Load progression data from JSON files.

    Returns:
        Dictionary with progression data for all combat styles
    """
    progression = {}
    for style in ["melee", "ranged", "magic"]:
        json_path = _DATA_DIR / f"{style}.json"
        if json_path.exists():
            with open(json_path, "r") as f:
                progression[style] = json.load(f)
        else:
            progression[style] = {}
    return progression


# Load progression data on module import
WIKI_PROGRESSION = _load_progression_data()


def get_progression_data(combat_style: str) -> dict[str, Any]:
    """
    Get progression data for a combat style.

    Args:
        combat_style: Combat style (melee, ranged, magic)

    Returns:
        Dictionary with progression data for the combat style
    """
    return WIKI_PROGRESSION.get(combat_style, {})  # type: ignore[no-any-return]


def get_slot_progression(combat_style: str, slot: str) -> list[Any]:
    """
    Get progression data for a specific slot.

    Args:
        combat_style: Combat style (melee, ranged, magic)
        slot: Equipment slot (head, cape, neck, etc.)

    Returns:
        List of tier groups for the slot
    """
    style_data: dict[str, Any] = WIKI_PROGRESSION.get(combat_style, {})
    slot_data = style_data.get(slot, [])
    return slot_data if isinstance(slot_data, list) else []


def get_all_slots(combat_style: str) -> list[str]:
    """
    Get all available slots for a combat style.

    Args:
        combat_style: Combat style (melee, ranged, magic)

    Returns:
        List of slot names
    """
    style_data = WIKI_PROGRESSION.get(combat_style, {})
    return list(style_data.keys())


def _load_wiki_guide_data() -> dict:
    """
    Load wiki guide data from JSON files.

    Guide data follows the canonical wiki structure with game stages, tiers,
    and full loadouts. This is separate from the slot-based progression data.

    Returns:
        Dictionary with guide data for all combat styles
    """
    guide_data = {}
    for style in ["melee", "ranged", "magic"]:
        json_path = _DATA_DIR / f"{style}_guide.json"
        if json_path.exists():
            with open(json_path, "r") as f:
                guide_data[style] = json.load(f)
        else:
            guide_data[style] = {}
    return guide_data


# Load guide data on module import
WIKI_GUIDE_DATA = _load_wiki_guide_data()


def get_wiki_guide(combat_style: str) -> dict[str, Any]:
    """
    Get wiki guide data for a combat style.

    Returns the guide data exactly as written in JSON - no reordering,
    substitution, or "fixing" of names. The guide is the source of truth.

    Args:
        combat_style: Combat style (melee, ranged, magic)

    Returns:
        Dictionary with guide data including game_stages, slot_order, bonus_table
    """
    return WIKI_GUIDE_DATA.get(combat_style, {})  # type: ignore[no-any-return]
