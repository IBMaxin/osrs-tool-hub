"""Wiki progression data loader and accessors."""
import json
from pathlib import Path

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


def get_progression_data(combat_style: str) -> dict:
    """
    Get progression data for a combat style.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        
    Returns:
        Dictionary with progression data for the combat style
    """
    return WIKI_PROGRESSION.get(combat_style, {})


def get_slot_progression(combat_style: str, slot: str) -> list:
    """
    Get progression data for a specific slot.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        slot: Equipment slot (head, cape, neck, etc.)
        
    Returns:
        List of tier groups for the slot
    """
    style_data = WIKI_PROGRESSION.get(combat_style, {})
    return style_data.get(slot, [])


def get_all_slots(combat_style: str) -> list:
    """
    Get all available slots for a combat style.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        
    Returns:
        List of slot names
    """
    style_data = WIKI_PROGRESSION.get(combat_style, {})
    return list(style_data.keys())
