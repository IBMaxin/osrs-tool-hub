"""Preset loadout utilities."""

from typing import Any, Dict
from sqlmodel import Session, select

from backend.models import PriceSnapshot
from backend.services.gear_presets import GEAR_PRESETS
from backend.services.gear.utils import find_item_by_name


def get_preset_loadout(session: Session, combat_style: str, tier: str) -> Dict:
    """
    Get a full loadout for a specific combat style and tier.

    Args:
        session: Database session
        combat_style: Combat style (melee, ranged, magic)
        tier: Tier level (low, mid, high)

    Returns:
        Dictionary with loadout information including items, stats, and total cost
    """
    # Validate inputs
    if combat_style not in GEAR_PRESETS:
        raise ValueError(
            f"Invalid combat style: {combat_style}. Must be one of {list(GEAR_PRESETS.keys())}"
        )

    if tier not in GEAR_PRESETS[combat_style]:
        raise ValueError(
            f"Invalid tier: {tier}. Must be one of {list(GEAR_PRESETS[combat_style].keys())}"
        )

    preset: dict[str, list[str]] = GEAR_PRESETS[combat_style][tier]
    slots_payload: dict[str, Any] = {}
    missing_items: list[dict[str, Any]] = []
    total_cost = 0

    # Process each slot
    for slot, item_names in preset.items():
        if not item_names:  # Empty slot (e.g., shield for 2H weapons)
            slots_payload[slot] = None
            continue

        # Try to find the first available item from the list
        item = None
        for item_name in item_names:
            found_item = find_item_by_name(session, item_name)
            if found_item:
                item = found_item
                break

        if item:
            # Get price information
            price_snapshot = session.exec(
                select(PriceSnapshot).where(PriceSnapshot.item_id == item.id)
            ).first()

            item_price = int(price_snapshot.high_price or 0) if price_snapshot else int(item.value or 0)
            total_cost += item_price

            # Build item details
            item_data = {
                "id": item.id,
                "name": item.name,
                "icon_url": item.icon_url,
                "price": item_price,
                "slot": item.slot,
                "requirements": {
                    "attack": item.attack_req,
                    "strength": item.strength_req,
                    "defence": item.defence_req,
                    "ranged": item.ranged_req,
                    "magic": item.magic_req,
                    "prayer": item.prayer_req,
                    "slayer": item.slayer_req,
                },
                "offensive_stats": {
                    "attack_stab": item.attack_stab,
                    "attack_slash": item.attack_slash,
                    "attack_crush": item.attack_crush,
                    "attack_magic": item.attack_magic,
                    "attack_ranged": item.attack_ranged,
                },
                "strength_bonuses": {
                    "melee_strength": item.melee_strength,
                    "ranged_strength": item.ranged_strength,
                    "magic_damage": item.magic_damage,
                    "prayer_bonus": item.prayer_bonus,
                },
                "defensive_stats": {
                    "defence_stab": item.defence_stab,
                    "defence_slash": item.defence_slash,
                    "defence_crush": item.defence_crush,
                    "defence_magic": item.defence_magic,
                    "defence_ranged": item.defence_ranged,
                },
            }

            slots_payload[slot] = item_data
        else:
            # Item not found in database
            slots_payload[slot] = None
            missing_items.append({"slot": slot, "names": item_names})

    return {
        "combat_style": combat_style,
        "tier": tier,
        "slots": slots_payload,
        "total_cost": total_cost,
        "missing_items": missing_items,
    }
