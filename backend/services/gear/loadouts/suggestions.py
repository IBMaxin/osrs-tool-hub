"""Gear suggestion utilities."""

from typing import Dict, List
from sqlmodel import Session, select

from backend.models import Item


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

    # Return items with actual stats, sorted by relevance to combat style
    item_list = []
    for item in items:
        # Calculate relevance for sorting (but don't filter - include all items)
        relevance = 0

        if combat_style == "melee":
            relevance = item.melee_strength * 4 + max(
                item.attack_stab, item.attack_slash, item.attack_crush
            )
        elif combat_style == "ranged":
            relevance = item.ranged_strength * 4 + item.attack_ranged
        elif combat_style == "magic":
            relevance = item.magic_damage * 10 + item.attack_magic
        elif combat_style == "prayer":
            relevance = item.prayer_bonus * 2

        # Include defensive stats and prayer bonus in relevance
        relevance += (
            item.defence_stab
            + item.defence_slash
            + item.defence_crush
            + item.defence_magic
            + item.defence_ranged
        ) * 0.3
        relevance += item.prayer_bonus * 1.5

        # Include all items with full stats
        item_list.append(
            {
                "id": item.id,
                "name": item.name,
                "relevance": round(relevance, 2),  # For sorting only
                "stats": {
                    # Offensive stats
                    "attack_stab": item.attack_stab,
                    "attack_slash": item.attack_slash,
                    "attack_crush": item.attack_crush,
                    "attack_magic": item.attack_magic,
                    "attack_ranged": item.attack_ranged,
                    # Strength/damage bonuses
                    "melee_strength": item.melee_strength,
                    "ranged_strength": item.ranged_strength,
                    "magic_damage": item.magic_damage,
                    # Defensive stats
                    "defence_stab": item.defence_stab,
                    "defence_slash": item.defence_slash,
                    "defence_crush": item.defence_crush,
                    "defence_magic": item.defence_magic,
                    "defence_ranged": item.defence_ranged,
                    # Utility
                    "prayer_bonus": item.prayer_bonus,
                },
                "icon": item.icon_url,
            }
        )

    # Sort by relevance descending and return top 100
    item_list.sort(key=lambda x: x["relevance"], reverse=True)
    return item_list[:100]
