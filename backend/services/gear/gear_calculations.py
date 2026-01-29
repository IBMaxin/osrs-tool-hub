"""Gear calculation methods - DPS and loadout calculations."""

from typing import Optional, List, Dict, Set
from sqlmodel import Session

from backend.models import Item
from backend.services.gear.loadouts import (
    suggest_gear,
    get_best_loadout,
    get_upgrade_path,
    get_alternatives,
)
from backend.services.gear.progression import (
    get_preset_loadout,
    get_progression_loadout,
    get_wiki_progression,
)
from backend.services.gear.dps import calculate_dps
from backend.services.gear.slayer_integration import suggest_slayer_gear


def suggest_gear_for_slot(
    session: Session,
    slot: str,
    combat_style: str = "melee",
    budget_per_slot: int = 10_000_000,
    defence_level: int = 99,
) -> List[Dict]:
    """
    Suggest items for a specific slot based on style and budget.

    Args:
        session: Database session
        slot: Equipment slot (head, cape, neck, etc.)
        combat_style: Combat style (melee, ranged, magic, prayer)
        budget_per_slot: Budget per slot (for future use)
        defence_level: Defence level requirement filter

    Returns:
        List of suggested items with scores
    """
    return suggest_gear(session, slot, combat_style, budget_per_slot, defence_level)


def calculate_dps_for_loadout(
    session: Session,
    items: Dict[str, Optional[Item]],
    combat_style: str,
    attack_type: Optional[str] = None,
    player_stats: Optional[Dict[str, int]] = None,
) -> Dict:
    """
    Calculate DPS (Damage Per Second) for a gear loadout.

    Args:
        session: Database session (unused, kept for consistency)
        items: Dict of slot -> Item (e.g., {"weapon": Item(...), "head": Item(...)})
        combat_style: Combat style (melee, ranged, magic)
        attack_type: For melee, attack type (stab, slash, crush)
        player_stats: Player combat stats (attack, strength, ranged, magic)

    Returns:
        Dict with DPS information
    """
    return calculate_dps(items, combat_style, attack_type, player_stats)


def get_best_loadout_for_stats(
    session: Session,
    combat_style: str,
    budget: int,
    stats: Dict[str, int],
    attack_type: Optional[str] = None,
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
    exclude_slots: Optional[List[str]] = None,
    ironman: bool = False,
    exclude_items: Optional[List[str]] = None,
    content_tag: Optional[str] = None,
    max_tick_manipulation: bool = False,
) -> Dict:
    """
    Find the best loadout a player can afford/wear based on stats and budget.

    Args:
        session: Database session
        combat_style: Combat style (melee, ranged, magic)
        budget: Total budget in GP
        stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
        attack_type: For melee, attack type (stab, slash, crush)
        quests_completed: Set of completed quest names
        achievements_completed: Set of completed achievement names
        exclude_slots: List of slots to exclude (e.g., ["shield"] for 2H weapons)
        ironman: If True, filter out tradeable items (ironman mode)
        exclude_items: List of item names to exclude
        content_tag: Optional content tag to filter by (e.g., 'toa_entry', 'gwd')
        max_tick_manipulation: If True, filter out items requiring tick manipulation

    Returns:
        Dict with best loadout, total cost, and DPS
    """
    return get_best_loadout(
        session,
        combat_style,
        budget,
        stats,
        attack_type,
        quests_completed,
        achievements_completed,
        exclude_slots,
        ironman,
        exclude_items,
        content_tag,
        max_tick_manipulation,
    )


def get_upgrade_path_for_loadout(
    session: Session,
    current_loadout: Dict[str, Optional[int]],  # slot -> item_id
    combat_style: str,
    budget: int,
    stats: Dict[str, int],
    attack_type: Optional[str] = None,
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
) -> Dict:
    """
    Find the next upgrade path with cost analysis.

    Args:
        session: Database session
        current_loadout: Dict of slot -> item_id for current gear
        combat_style: Combat style (melee, ranged, magic)
        budget: Available budget for upgrades
        stats: Dict with stat levels
        attack_type: For melee, attack type (stab, slash, crush)
        quests_completed: Set of completed quest names
        achievements_completed: Set of completed achievement names

    Returns:
        Dict with upgrade recommendations per slot
    """
    return get_upgrade_path(
        session,
        current_loadout,
        combat_style,
        budget,
        stats,
        attack_type,
        quests_completed,
        achievements_completed,
    )


def get_alternatives_for_slot(
    session: Session,
    slot: str,
    combat_style: str,
    budget: Optional[int] = None,
    stats: Optional[Dict[str, int]] = None,
    attack_type: Optional[str] = None,
    quests_completed: Optional[Set[str]] = None,
    achievements_completed: Optional[Set[str]] = None,
    limit: int = 10,
) -> List[Dict]:
    """
    Get alternative items for a specific slot.

    Args:
        session: Database session
        slot: Equipment slot
        combat_style: Combat style (melee, ranged, magic)
        budget: Optional budget filter
        stats: Optional stat requirements filter
        attack_type: For melee, attack type (stab, slash, crush)
        quests_completed: Set of completed quest names
        achievements_completed: Set of completed achievement names
        limit: Maximum number of alternatives to return

    Returns:
        List of alternative items sorted by score
    """
    return get_alternatives(
        session,
        slot,
        combat_style,
        budget,
        stats,
        attack_type,
        quests_completed,
        achievements_completed,
        limit,
    )


def get_preset_loadout_for_tier(
    session: Session,
    combat_style: str,
    tier: str,
) -> Dict:
    """
    Get a full loadout for a specific combat style and tier.

    Args:
        session: Database session
        combat_style: Combat style (melee, ranged, magic)
        tier: Tier level (low, mid, high)

    Returns:
        Dictionary with loadout information including items, stats, and total cost
    """
    return get_preset_loadout(session, combat_style, tier)


def get_progression_loadout_for_tier(
    session: Session,
    style: str,
    tier: str,
) -> Dict:
    """
    Get a progression loadout for a specific combat style and tier.
    Simplified version that returns basic item information.

    Args:
        session: Database session
        style: Combat style (melee, ranged, magic)
        tier: Tier level (low, mid, high)

    Returns:
        Dictionary with tier, style, and loadout information
    """
    return get_progression_loadout(session, style, tier)


def get_wiki_progression_for_style(session: Session, style: str) -> dict:
    """
    Returns the exact Wiki table structure, enriched with Price/Icon data.

    Args:
        session: Database session
        style: Combat style (melee, ranged, magic)

    Returns:
        Dictionary with enriched progression data for all slots
    """
    return get_wiki_progression(session, style)


def suggest_slayer_gear_for_task(
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
    return suggest_slayer_gear(
        session,
        task_id,
        stats,
        budget,
        combat_style,
        quests_completed,
        achievements_completed,
        ironman,
    )
