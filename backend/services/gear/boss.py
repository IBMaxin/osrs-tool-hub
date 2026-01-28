"""Boss-specific BiS calculation service."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from sqlmodel import Session

from backend.services.gear.loadouts import get_best_loadout
from backend.models import Monster

logger = logging.getLogger(__name__)

# Path to boss data files
_BOSS_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "bosses"


def get_boss_data(boss_name: str) -> Optional[Dict]:
    """
    Load boss data from JSON file.

    Args:
        boss_name: Boss name (e.g., "vorkath", "zulrah")

    Returns:
        Dictionary with boss data or None if not found
    """
    boss_file = _BOSS_DATA_DIR / f"{boss_name.lower()}.json"
    
    if not boss_file.exists():
        logger.warning(f"Boss data file not found: {boss_file}")
        return None

    try:
        with open(boss_file, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading boss data from {boss_file}: {e}")
        return None


def get_available_bosses() -> List[str]:
    """
    Get list of available boss names.

    Returns:
        List of boss names (without .json extension)
    """
    if not _BOSS_DATA_DIR.exists():
        return []

    bosses = []
    for boss_file in _BOSS_DATA_DIR.glob("*.json"):
        bosses.append(boss_file.stem)

    return sorted(bosses)


class BossService:
    """Service for boss-specific BiS calculations."""

    def __init__(self, session: Session):
        """
        Initialize boss service.

        Args:
            session: Database session
        """
        self.session = session

    def get_bis_for_boss(
        self,
        boss_name: str,
        budget: int,
        stats: Dict[str, int],
        ironman: bool = False,
        exclude_items: Optional[List[str]] = None,
        max_tick_manipulation: bool = False,
    ) -> Dict:
        """
        Calculate optimal loadout for a specific boss.

        Args:
            boss_name: Boss name (e.g., "vorkath", "zulrah")
            budget: Total budget in GP
            stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
            ironman: If True, filter out tradeable items
            exclude_items: List of item names to exclude
            max_tick_manipulation: If True, filter out items requiring tick manipulation

        Returns:
            Dict with optimal loadout(s) for the boss, including:
            - boss_info: Boss data
            - recommended_loadouts: List of loadouts (one per recommended style)
            - notes: Special considerations for this boss

        Raises:
            ValueError: If boss not found
        """
        boss_data = get_boss_data(boss_name)
        if not boss_data:
            raise ValueError(f"Boss '{boss_name}' not found. Available bosses: {', '.join(get_available_bosses())}")

        recommended_styles = boss_data.get("recommended_styles", ["melee", "ranged", "magic"])
        content_tag = boss_data.get("content_tags", [])
        content_tag_str = content_tag[0] if content_tag else None

        # Calculate BiS for each recommended style
        recommended_loadouts = []
        
        for style in recommended_styles:
            try:
                loadout = get_best_loadout(
                    session=self.session,
                    combat_style=style,
                    budget=budget,
                    stats=stats,
                    attack_type=None,
                    quests_completed=None,
                    achievements_completed=None,
                    exclude_slots=None,
                    ironman=ironman,
                    exclude_items=exclude_items,
                    content_tag=content_tag_str,
                    max_tick_manipulation=max_tick_manipulation,
                )
                loadout["style"] = style
                recommended_loadouts.append(loadout)
            except Exception as e:
                logger.error(f"Error calculating BiS for {boss_name} with style {style}: {e}")
                continue

        return {
            "boss_info": boss_data,
            "recommended_loadouts": recommended_loadouts,
            "notes": boss_data.get("special_mechanics", []),
        }
