"""Loadout selection and optimization utilities."""

from typing import Dict, List, Optional, Set
from sqlmodel import Session, select
from sqlalchemy import and_

from backend.models import Item
from backend.services.gear.pricing import get_item_price
from backend.services.gear.scoring import score_item_for_style
from backend.services.gear.requirements import meets_requirements
from backend.services.gear.dps import calculate_dps


def suggest_gear(
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
    query = select(Item).where(Item.slot == slot)

    # Filter by requirements
    query = query.where(Item.defence_req <= defence_level)

    items = session.exec(query).all()

    # Sort Logic
    scored_items = []
    for item in items:
        score = 0
        if combat_style == "melee":
            score = item.melee_strength * 4 + item.attack_slash
        elif combat_style == "ranged":
            score = item.ranged_strength * 4 + item.attack_ranged
        elif combat_style == "magic":
            score = item.magic_damage * 10 + item.attack_magic
        elif combat_style == "prayer":
            score = item.prayer_bonus

        if score > 0:
            scored_items.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "score": score,
                    "stats": {"str": item.melee_strength, "pray": item.prayer_bonus},
                    "icon": item.icon_url,
                }
            )

    # Return top 10
    scored_items.sort(key=lambda x: x["score"], reverse=True)
    return scored_items[:10]


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

    loadout = {}
    total_cost = 0
    remaining_budget = budget

    # Get all items for each slot, sorted by score
    for slot in slots:
        query = select(Item).where(Item.slot == slot)

        # Filter by requirements
        query = query.where(
            and_(
                Item.attack_req <= stats.get("attack", 1),
                Item.strength_req <= stats.get("strength", 1),
                Item.defence_req <= stats.get("defence", 1),
                Item.ranged_req <= stats.get("ranged", 1),
                Item.magic_req <= stats.get("magic", 1),
                Item.prayer_req <= stats.get("prayer", 1),
            )
        )

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
    if loadout.get("weapon") and loadout["weapon"].is_2h:
        loadout["shield"] = None

    # Calculate DPS
    dps_info = calculate_dps(loadout, combat_style, attack_type, stats)

    # Build response
    result = {
        "combat_style": combat_style,
        "total_cost": total_cost,
        "budget_used": budget - remaining_budget,
        "budget_remaining": remaining_budget,
        "dps": dps_info,
        "slots": {},
    }

    for slot, item in loadout.items():
        if item:
            price = get_item_price(session, item)
            result["slots"][slot] = {
                "id": item.id,
                "name": item.name,
                "icon_url": item.icon_url,
                "price": price,
                "score": score_item_for_style(item, combat_style, attack_type),
            }
        else:
            result["slots"][slot] = None

    return result


def get_upgrade_path(
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
    upgrades = {}
    upgrade_list = []

    # Convert current_loadout (slot -> item_id) to current_items (slot -> Item)
    current_items = {}
    for slot, item_id in current_loadout.items():
        if item_id is not None:
            item = session.get(Item, item_id)
            if item:
                current_items[slot] = item
            else:
                current_items[slot] = None
        else:
            current_items[slot] = None

    # Calculate current DPS
    current_dps_result = calculate_dps(current_items, combat_style, attack_type, stats)
    current_dps = current_dps_result.get("dps", 0.0)

    for slot, current_item_id in current_loadout.items():
        if current_item_id is None:
            continue

        current_item = session.get(Item, current_item_id)
        if not current_item:
            continue

        current_score = score_item_for_style(current_item, combat_style, attack_type)
        current_price = get_item_price(session, current_item)

        # Find better items in same slot
        query = select(Item).where(
            and_(
                Item.slot == slot,
                Item.attack_req <= stats.get("attack", 1),
                Item.strength_req <= stats.get("strength", 1),
                Item.defence_req <= stats.get("defence", 1),
                Item.ranged_req <= stats.get("ranged", 1),
                Item.magic_req <= stats.get("magic", 1),
                Item.prayer_req <= stats.get("prayer", 1),
            )
        )

        items = session.exec(query).all()

        better_items = []
        for item in items:
            if not meets_requirements(item, stats, quests_completed, achievements_completed):
                continue

            score = score_item_for_style(item, combat_style, attack_type)
            if score > current_score:
                price = get_item_price(session, item)
                upgrade_cost = price - current_price
                if upgrade_cost <= budget:
                    # Calculate DPS with this upgrade
                    upgraded_items = current_items.copy()
                    upgraded_items[slot] = item
                    upgraded_dps_result = calculate_dps(upgraded_items, combat_style, attack_type, stats)
                    upgraded_dps = upgraded_dps_result.get("dps", 0.0)
                    dps_increase = upgraded_dps - current_dps

                    # Calculate DPS per GP
                    dps_per_gp = dps_increase / max(upgrade_cost, 1) if upgrade_cost > 0 else 0

                    better_items.append(
                        {
                            "item": item,
                            "score": score,
                            "price": price,
                            "upgrade_cost": upgrade_cost,
                            "score_improvement": score - current_score,
                            "dps_increase": dps_increase,
                            "dps_per_gp": dps_per_gp,
                        }
                    )

        # Sort by DPS per GP (priority metric)
        better_items.sort(key=lambda x: x["dps_per_gp"], reverse=True)

        if better_items:
            best_upgrade = better_items[0]
            upgrade_data = {
                "slot": slot,
                "current": {
                    "id": current_item.id,
                    "name": current_item.name,
                    "score": current_score,
                    "price": current_price,
                },
                "recommended": {
                    "id": best_upgrade["item"].id,
                    "name": best_upgrade["item"].name,
                    "icon_url": best_upgrade["item"].icon_url,
                    "score": best_upgrade["score"],
                    "price": best_upgrade["price"],
                    "upgrade_cost": best_upgrade["upgrade_cost"],
                    "score_improvement": best_upgrade["score_improvement"],
                    "dps_increase": round(best_upgrade["dps_increase"], 2),
                    "dps_per_gp": round(best_upgrade["dps_per_gp"], 8),
                    "efficiency": round(
                        best_upgrade["score_improvement"] / max(best_upgrade["upgrade_cost"], 1), 4
                    ),
                },
                "alternatives": [
                    {
                        "id": alt["item"].id,
                        "name": alt["item"].name,
                        "icon_url": alt["item"].icon_url,
                        "score": alt["score"],
                        "price": alt["price"],
                        "upgrade_cost": alt["upgrade_cost"],
                        "score_improvement": alt["score_improvement"],
                        "dps_increase": round(alt["dps_increase"], 2),
                        "dps_per_gp": round(alt["dps_per_gp"], 8),
                    }
                    for alt in better_items[1:6]  # Top 5 alternatives
                ],
            }
            upgrades[slot] = upgrade_data
            upgrade_list.append(upgrade_data)

    # Sort all upgrades by priority (DPS per GP)
    upgrade_list.sort(key=lambda x: x["recommended"]["dps_per_gp"], reverse=True)

    # Add priority numbers
    for idx, upgrade in enumerate(upgrade_list, start=1):
        upgrades[upgrade["slot"]]["recommended"]["priority"] = idx

    return {
        "combat_style": combat_style,
        "current_dps": round(current_dps, 2),
        "recommended_upgrades": [
            {
                "item": upgrade["recommended"]["name"],
                "slot": upgrade["slot"],
                "cost": upgrade["recommended"]["upgrade_cost"],
                "dps_increase": upgrade["recommended"]["dps_increase"],
                "dps_per_gp": upgrade["recommended"]["dps_per_gp"],
                "priority": upgrade["recommended"]["priority"],
            }
            for upgrade in upgrade_list
        ],
        "upgrades_by_slot": upgrades,
        "total_upgrade_cost": sum(
            upgrade["recommended"]["upgrade_cost"] for upgrade in upgrades.values()
        ),
    }


def get_alternatives(
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
    query = select(Item).where(Item.slot == slot)

    if stats:
        query = query.where(
            and_(
                Item.attack_req <= stats.get("attack", 1),
                Item.strength_req <= stats.get("strength", 1),
                Item.defence_req <= stats.get("defence", 1),
                Item.ranged_req <= stats.get("ranged", 1),
                Item.magic_req <= stats.get("magic", 1),
                Item.prayer_req <= stats.get("prayer", 1),
            )
        )

    items = session.exec(query).all()

    alternatives = []
    for item in items:
        if stats and not meets_requirements(item, stats, quests_completed, achievements_completed):
            continue

        price = get_item_price(session, item)
        if budget and price > budget:
            continue

        score = score_item_for_style(item, combat_style, attack_type)
        if score > 0:
            alternatives.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "icon_url": item.icon_url,
                    "price": price,
                    "score": score,
                    "requirements": {
                        "attack": item.attack_req,
                        "strength": item.strength_req,
                        "defence": item.defence_req,
                        "ranged": item.ranged_req,
                        "magic": item.magic_req,
                        "prayer": item.prayer_req,
                        "quest": item.quest_req,
                        "achievement": item.achievement_req,
                    },
                    "stats": {
                        "melee_strength": item.melee_strength,
                        "ranged_strength": item.ranged_strength,
                        "magic_damage": item.magic_damage,
                        "prayer_bonus": item.prayer_bonus,
                    },
                }
            )

    # Sort by score descending
    alternatives.sort(key=lambda x: x["score"], reverse=True)
    return alternatives[:limit]
