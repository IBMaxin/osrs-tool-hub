"""Loadout optimization utilities."""

from typing import Dict, List, Optional, Set
from sqlmodel import Session, select
from sqlalchemy import and_

from backend.models import Item
from backend.services.gear.pricing import get_item_price
from backend.services.gear.scoring import score_item_for_style
from backend.services.gear.requirements import (
    meets_requirements,
    meets_content_requirements,
    is_ironman_compatible,
)
from backend.services.gear.dps import calculate_dps


def get_best_loadout(
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
    if exclude_slots is None:
        exclude_slots = []

    # Define equipment slots
    slots = [
        "head",
        "cape",
        "neck",
        "weapon",
        "body",
        "shield",
        "legs",
        "hands",
        "feet",
        "ring",
        "ammo",
    ]
    slots = [s for s in slots if s not in exclude_slots]

    loadout: dict[str, Item | None] = {}
    total_cost = 0
    remaining_budget = budget

    # Get all items for each slot, sorted by score
    for slot in slots:
        query = select(Item).where(Item.slot == slot)

        # Filter by requirements
        query = query.where(
            and_(
                Item.attack_req <= stats.get("attack", 1),  # type: ignore[arg-type]
                Item.strength_req <= stats.get("strength", 1),  # type: ignore[arg-type]
                Item.defence_req <= stats.get("defence", 1),  # type: ignore[arg-type]
                Item.ranged_req <= stats.get("ranged", 1),  # type: ignore[arg-type]
                Item.magic_req <= stats.get("magic", 1),  # type: ignore[arg-type]
                Item.prayer_req <= stats.get("prayer", 1),  # type: ignore[arg-type]
            )
        )  # type: ignore[arg-type]

        items = session.exec(query).all()

        # Filter by quest/achievement requirements, constraints, and budget
        valid_items = []
        exclude_items_set = set(exclude_items or [])

        for item in items:
            if not meets_requirements(item, stats, quests_completed, achievements_completed):
                continue

            # Check ironman compatibility
            if ironman and not is_ironman_compatible(item):
                continue

            # Check content tag requirements
            if not meets_content_requirements(item, content_tag):
                continue

            # Check exclude items list
            if item.name in exclude_items_set:
                continue

            # Note: max_tick_manipulation filtering would require item metadata
            # For now, we'll skip this check as it requires additional item properties

            price = get_item_price(session, item)
            if price <= remaining_budget:
                score = score_item_for_style(item, combat_style, attack_type)
                valid_items.append((item, price, score))

        # Sort by score descending
        valid_items.sort(key=lambda x: x[2], reverse=True)

        # Select best item within budget
        if valid_items:
            best_item, price, score = valid_items[0]
            loadout[slot] = best_item
            total_cost += price
            remaining_budget -= price
        else:
            loadout[slot] = None

    # Handle 2H weapons (exclude shield if weapon is 2H)
    weapon = loadout.get("weapon")
    if weapon is not None and weapon.is_2h:
        loadout["shield"] = None

    # Calculate DPS
    dps_info = calculate_dps(loadout, combat_style, attack_type, stats)

    # Build response
    slots_payload: dict[str, object] = {}
    result: dict[str, object] = {
        "combat_style": combat_style,
        "total_cost": total_cost,
        "budget_used": budget - remaining_budget,
        "budget_remaining": remaining_budget,
        "dps": dps_info,
        "slots": slots_payload,
    }

    for slot, equipped_item in loadout.items():
        if equipped_item is not None:
            price = get_item_price(session, equipped_item)
            slots_payload[slot] = {
                "id": equipped_item.id,
                "name": equipped_item.name,
                "icon_url": equipped_item.icon_url,
                "price": price,
                "score": score_item_for_style(equipped_item, combat_style, attack_type),
            }
        else:
            slots_payload[slot] = None

    return result
