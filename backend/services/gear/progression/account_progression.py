"""Account-wide progression utilities."""

import logging
from typing import Dict, List, Optional, Set
from sqlmodel import Session

from backend.services.gear.loadouts import get_upgrade_path


def get_global_upgrade_path(
    session: Session,
    current_gear: Dict[str, Dict[str, Optional[int]]],  # style -> slot -> item_id
    bank_value: int,
    stats: Dict[str, int],
    unlocked_content: Optional[List[str]] = None,
    attack_type: Optional[str] = None,
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
) -> Dict:
    """
    Calculate cross-style account progression with prioritized upgrade path.

    Args:
        session: Database session
        current_gear: Dict of style -> loadout (slot -> item_id)
            Example: {"melee": {"weapon": 123, "head": 456}, "ranged": {...}, "magic": {...}}
        bank_value: Total bank value available for upgrades
        stats: Dict with stat levels
        unlocked_content: List of unlocked content tags (e.g., ["ToA", "GWD"])
        attack_type: For melee, attack type (stab, slash, crush)
        quests_completed: Set of completed quest names
        achievements_completed: Set of completed achievement names

    Returns:
        Dict with prioritized upgrade path across all styles:
        - recommended_upgrades: List of upgrades sorted by DPS/GP priority
        - upgrades_by_style: Dict of style -> upgrade path
        - total_cost: Total cost of all recommended upgrades
    """
    all_upgrades = []
    upgrades_by_style = {}

    # Calculate upgrade paths for each style
    styles = ["melee", "ranged", "magic"]

    for style in styles:
        loadout = current_gear.get(style, {})
        if not loadout:
            continue

        # Content tag mapping reserved for future use (ToA, GWD, etc.)
        if unlocked_content:
            if "ToA" in unlocked_content or "toa" in [c.lower() for c in unlocked_content]:
                pass  # toa_entry
            elif "GWD" in unlocked_content or "gwd" in [c.lower() for c in unlocked_content]:
                pass  # gwd

        try:
            upgrade_result = get_upgrade_path(
                session=session,
                current_loadout=loadout,
                combat_style=style,
                budget=bank_value,  # Use full bank value for each style calculation
                stats=stats,
                attack_type=attack_type if style == "melee" else None,
                quests_completed=quests_completed,
                achievements_completed=achievements_completed,
            )

            upgrades_by_style[style] = upgrade_result

            # Extract recommended upgrades and add style info
            if "recommended_upgrades" in upgrade_result:
                for upgrade in upgrade_result["recommended_upgrades"]:
                    upgrade["style"] = style
                    all_upgrades.append(upgrade)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error calculating upgrade path for {style}: {e}")
            continue

    # Sort all upgrades by DPS per GP (global priority)
    all_upgrades.sort(key=lambda x: x.get("dps_per_gp", 0), reverse=True)

    # Add global priority numbers
    for idx, upgrade in enumerate(all_upgrades, start=1):
        upgrade["global_priority"] = idx

    # Calculate total cost (sum of top upgrades within bank value)
    total_cost = 0
    prioritized_upgrades = []
    remaining_budget = bank_value

    for upgrade in all_upgrades:
        cost = upgrade.get("cost", 0)
        if cost <= remaining_budget:
            prioritized_upgrades.append(upgrade)
            total_cost += cost
            remaining_budget -= cost

    return {
        "recommended_upgrades": prioritized_upgrades,
        "upgrades_by_style": upgrades_by_style,
        "total_cost": total_cost,
        "bank_value": bank_value,
        "remaining_budget": remaining_budget,
    }
