"""Upgrade path calculation utilities."""

from typing import Dict, Optional, Set
from sqlmodel import Session, select
from sqlalchemy import and_

from backend.models import Item
from backend.services.gear.pricing import get_item_price
from backend.services.gear.scoring import score_item_for_style
from backend.services.gear.requirements import meets_requirements
from backend.services.gear.dps import calculate_dps


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
    upgrades_by_slot: dict[str, dict[str, object]] = {}
    upgrade_list: list[dict[str, object]] = []
    total_upgrade_cost = 0

    # Convert current_loadout (slot -> item_id) to current_items (slot -> Item)
    current_items: dict[str, Item | None] = {}
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
                Item.slot == slot,  # type: ignore[arg-type]
                Item.attack_req <= stats.get("attack", 1),  # type: ignore[arg-type]
                Item.strength_req <= stats.get("strength", 1),  # type: ignore[arg-type]
                Item.defence_req <= stats.get("defence", 1),  # type: ignore[arg-type]
                Item.ranged_req <= stats.get("ranged", 1),  # type: ignore[arg-type]
                Item.magic_req <= stats.get("magic", 1),  # type: ignore[arg-type]
                Item.prayer_req <= stats.get("prayer", 1),  # type: ignore[arg-type]
            )
        )  # type: ignore[arg-type]

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
                    upgraded_dps_result = calculate_dps(
                        upgraded_items, combat_style, attack_type, stats
                    )
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
            total_upgrade_cost += int(best_upgrade["upgrade_cost"])
            upgrade_data: dict[str, object] = {
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
            upgrades_by_slot[slot] = upgrade_data
            upgrade_list.append(upgrade_data)

    # Sort all upgrades by priority (DPS per GP)
    def dps_per_gp_key(upgrade: dict[str, object]) -> float:
        rec = upgrade.get("recommended")
        if isinstance(rec, dict):
            val = rec.get("dps_per_gp")
            if isinstance(val, (int, float)):
                return float(val)
        return 0.0

    upgrade_list.sort(key=dps_per_gp_key, reverse=True)

    # Add priority numbers
    for idx, upgrade in enumerate(upgrade_list, start=1):
        rec = upgrade.get("recommended")
        if isinstance(rec, dict):
            rec["priority"] = idx

    recommended_upgrades: list[dict[str, object]] = []
    for upgrade in upgrade_list:
        rec = upgrade.get("recommended")
        if not isinstance(rec, dict):
            continue

        recommended_upgrades.append(
            {
                "item": str(rec.get("name", "")),
                "slot": str(upgrade.get("slot", "")),
                "cost": int(rec.get("upgrade_cost", 0)),
                "dps_increase": float(rec.get("dps_increase", 0.0)),
                "dps_per_gp": float(rec.get("dps_per_gp", 0.0)),
                "priority": int(rec.get("priority", 0)),
            }
        )

    return {
        "combat_style": combat_style,
        "current_dps": round(current_dps, 2),
        "recommended_upgrades": recommended_upgrades,
        "upgrades_by_slot": upgrades_by_slot,
        "total_upgrade_cost": total_upgrade_cost,
    }
