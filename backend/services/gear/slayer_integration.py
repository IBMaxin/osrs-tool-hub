"""Slayer gear suggestion integration."""

from typing import Dict, List, Optional, Set
from sqlmodel import Session

from backend.models import Monster, SlayerTask
from backend.services.slayer_data import SLAYER_TASK_DATA
from backend.services.gear.loadouts import get_best_loadout


def suggest_slayer_gear(
    session: Session,
    task_id: int,
    stats: Dict[str, int],
    budget: int = 100_000_000,
    combat_style: Optional[str] = None,
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
    ironman: bool = False,
) -> Dict:
    """
    Suggest optimal gear for a slayer task based on user levels.
    Returns multiple tier suggestions similar to wiki progression guides.

    Args:
        session: Database session
        task_id: The slayer task ID
        stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
        budget: Total budget in GP (default: 100M)
        combat_style: Optional combat style override
        quests_completed: Set of completed quest names
        achievements_completed: Set of completed achievement names
        ironman: If True, filter out tradeable items (ironman mode)

    Returns:
        Dict with optimal loadouts for multiple tiers, task info, and reasoning
    """
    # Get task and monster
    task = session.get(SlayerTask, task_id)
    if not task:
        return {"error": "Task not found"}

    monster = session.get(Monster, task.monster_id)
    if not monster:
        return {"error": "Monster not found"}

    # Get task data (weakness, attack_style)
    task_data = SLAYER_TASK_DATA.get(task.category) or SLAYER_TASK_DATA.get(monster.name) or {}
    attack_style_str = task_data.get("attack_style", "Melee")
    weakness_list = task_data.get("weakness", [])

    # Use provided combat style or parse from task data
    if combat_style:
        # Validate combat style
        if combat_style not in ["melee", "ranged", "magic"]:
            return {
                "error": f"Invalid combat style: {combat_style}. Must be melee, ranged, or magic"
            }
        # Parse attack type from weaknesses if melee
        attack_type = None
        if combat_style == "melee":
            if "stab" in [w.lower() for w in weakness_list]:
                attack_type = "stab"
            elif "slash" in [w.lower() for w in weakness_list]:
                attack_type = "slash"
            elif "crush" in [w.lower() for w in weakness_list]:
                attack_type = "crush"
    else:
        # Parse combat style and attack type from attack_style string
        combat_style, attack_type = _parse_attack_style(attack_style_str, weakness_list)

    # Determine level tier based on highest relevant stat
    primary_stat = stats.get(combat_style, stats.get("attack", 1))
    if combat_style == "melee":
        primary_stat = max(stats.get("attack", 1), stats.get("strength", 1))
    elif combat_style == "ranged":
        primary_stat = stats.get("ranged", 1)
    elif combat_style == "magic":
        primary_stat = stats.get("magic", 1)

    # Define tier budgets based on level
    tier_budgets = []
    if primary_stat >= 70:
        tier_budgets.append(("70+", 5_000_000))
    if primary_stat >= 75:
        tier_budgets.append(("75+", 20_000_000))
    if primary_stat >= 80:
        tier_budgets.append(("80+", 50_000_000))
    if primary_stat >= 85:
        tier_budgets.append(("85+", 100_000_000))
    if primary_stat >= 90:
        tier_budgets.append(("90+", 200_000_000))

    # If no tiers match, use current budget as single tier
    if not tier_budgets:
        tier_budgets = [("Current", min(budget, 5_000_000))]

    # Get loadouts for each tier
    tier_loadouts = []
    for tier_name, tier_budget in tier_budgets:
        tier_stats = stats.copy()
        # Adjust stats for tier (cap at tier level)
        tier_level = int(tier_name.replace("+", "").replace("Current", str(primary_stat)))
        for stat_key in ["attack", "strength", "defence", "ranged", "magic"]:
            if stat_key in tier_stats:
                tier_stats[stat_key] = min(tier_stats[stat_key], tier_level)

        loadout_result = get_best_loadout(
            session,
            combat_style=combat_style,
            budget=min(tier_budget, budget),
            stats=tier_stats,
            attack_type=attack_type,
            quests_completed=quests_completed,
            achievements_completed=achievements_completed,
            ironman=ironman,
        )

        tier_loadouts.append(
            {
                "tier": tier_name,
                "level": tier_level,
                "loadout": loadout_result,
            }
        )

    return {
        "task_id": task_id,
        "monster_name": monster.name,
        "category": task.category,
        "combat_style": combat_style,
        "attack_type": attack_type,
        "weakness": weakness_list,
        "attack_style_recommendation": attack_style_str,
        "tier_loadouts": tier_loadouts,
        "primary_loadout": tier_loadouts[-1]["loadout"] if tier_loadouts else None,
    }


def _parse_attack_style(
    attack_style_str: str, weakness_list: List[str]
) -> tuple[str, Optional[str]]:
    """
    Parse attack style string to determine combat style and attack type.

    Args:
        attack_style_str: Attack style string (e.g., "Melee (Slash) or Magic (Burst/Barrage)")
        weakness_list: List of weaknesses (e.g., ["Slash", "Demonbane"])

    Returns:
        Tuple of (combat_style, attack_type)
    """
    attack_style_lower = attack_style_str.lower()

    # Determine combat style priority from attack_style string
    # Priority: Magic > Ranged > Melee (for slayer efficiency)
    combat_style = "melee"  # default
    attack_type = None

    # Check for magic indicators
    if any(
        keyword in attack_style_lower
        for keyword in ["magic", "burst", "barrage", "trident", "sang"]
    ):
        combat_style = "magic"
    # Check for ranged indicators
    elif any(
        keyword in attack_style_lower
        for keyword in ["ranged", "ranged", "bow", "crossbow", "blowpipe"]
    ):
        combat_style = "ranged"
    # Otherwise default to melee

    # Determine attack type for melee from weakness or attack_style string
    if combat_style == "melee":
        # Check weakness list first
        if "stab" in [w.lower() for w in weakness_list]:
            attack_type = "stab"
        elif "slash" in [w.lower() for w in weakness_list]:
            attack_type = "slash"
        elif "crush" in [w.lower() for w in weakness_list]:
            attack_type = "crush"
        # Fallback to parsing attack_style string
        elif "stab" in attack_style_lower:
            attack_type = "stab"
        elif "slash" in attack_style_lower:
            attack_type = "slash"
        elif "crush" in attack_style_lower:
            attack_type = "crush"

    return combat_style, attack_type
