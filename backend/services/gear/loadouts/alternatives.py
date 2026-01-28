"""Alternative item selection utilities."""

from typing import Dict, List, Optional, Set
from sqlmodel import Session, select
from sqlalchemy import and_

from backend.models import Item
from backend.services.gear.pricing import get_item_price
from backend.services.gear.scoring import score_item_for_style
from backend.services.gear.requirements import meets_requirements


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
