"""Wiki progression utilities."""

from typing import Dict, List
from sqlmodel import Session

from backend.services.gear_presets import GEAR_PRESETS
from backend.services.wiki_data import WIKI_PROGRESSION
from backend.services.gear.utils import find_item_by_name
from backend.services.gear.pricing import get_item_price


def get_progression_loadout(session: Session, style: str, tier: str) -> Dict:
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
    preset = GEAR_PRESETS.get(style, {}).get(tier)
    if not preset:
        return {"error": "Invalid style or tier"}

    loadout = {}
    for slot, item_names in preset.items():
        if not item_names:  # Empty slot (e.g., shield for 2H weapons)
            continue

        found_item = None
        # Fallback logic: Try 1st item, then 2nd...
        for name in item_names:
            found_item = find_item_by_name(session, name)
            if found_item:
                break

        if found_item:
            loadout[slot] = {
                "id": found_item.id,
                "name": found_item.name,
                "icon": found_item.icon_url,
            }

    return {"tier": tier, "style": style, "loadout": loadout}


def get_wiki_progression(session: Session, style: str) -> dict:
    """
    Returns the exact Wiki table structure, enriched with Price/Icon data.

    Args:
        session: Database session
        style: Combat style (melee, ranged, magic)

    Returns:
        Dictionary with enriched progression data for all slots
    """
    import logging

    logger = logging.getLogger(__name__)

    data = WIKI_PROGRESSION.get(style, {})
    if not data:
        logger.warning(f"No progression data found for style: {style}")
        return {}

    enriched_data = {}

    for slot, tiers in data.items():
        if not isinstance(tiers, list):
            logger.warning(f"Invalid tiers data for slot {slot}: expected list, got {type(tiers)}")
            continue

        enriched_tiers = []
        for tier_group in tiers:
            if not isinstance(tier_group, dict) or "items" not in tier_group:
                logger.warning(f"Invalid tier_group structure for slot {slot}: {tier_group}")
                continue
            items_data = []
            tier_items = tier_group.get("items", [])
            if not isinstance(tier_items, list):
                logger.warning(
                    f"Invalid items list for slot {slot}, tier {tier_group.get('tier', 'unknown')}"
                )
                continue

            for item_name in tier_items:
                if not isinstance(item_name, str):
                    logger.warning(f"Invalid item_name type: {type(item_name)}, value: {item_name}")
                    continue

                try:
                    # Try to find item by name (case-insensitive, partial match)
                    item = find_item_by_name(session, item_name)

                    if item:
                        # Get price from PriceSnapshot or fallback to value
                        price = get_item_price(session, item)

                        # Generate wiki URL (handle None name)
                        item_name_clean = (
                            item.name or item_name
                        )  # Fallback to original name if None
                        wiki_name = item_name_clean.replace(" ", "_").replace("'", "%27")
                        wiki_url = f"https://oldschool.runescape.wiki/w/{wiki_name}"

                        items_data.append(
                            {
                                "id": item.id,
                                "name": item_name_clean,
                                "icon": item.icon_url,
                                "price": price,
                                "wiki_url": wiki_url,
                                "requirements": {
                                    "attack": item.attack_req or 1,
                                    "strength": item.strength_req or 1,
                                    "defence": item.defence_req or 1,
                                    "ranged": item.ranged_req or 1,
                                    "magic": item.magic_req or 1,
                                    "prayer": item.prayer_req or 1,
                                    "quest": item.quest_req,
                                    "achievement": item.achievement_req,
                                },
                                "stats": {
                                    "melee_strength": item.melee_strength or 0,
                                    "ranged_strength": item.ranged_strength or 0,
                                    "magic_damage": item.magic_damage or 0,
                                    "prayer_bonus": item.prayer_bonus or 0,
                                    "attack_stab": item.attack_stab or 0,
                                    "attack_slash": item.attack_slash or 0,
                                    "attack_crush": item.attack_crush or 0,
                                    "attack_magic": item.attack_magic or 0,
                                    "attack_ranged": item.attack_ranged or 0,
                                },
                            }
                        )
                    else:
                        # Fallback if item not in DB (generate icon URL manually)
                        safe_name = item_name.replace(" ", "_").replace("'", "%27")
                        wiki_name = item_name.replace(" ", "_").replace("'", "%27")
                        items_data.append(
                            {
                                "id": None,
                                "name": item_name,
                                "icon": f"https://oldschool.runescape.wiki/images/{safe_name}_detail.png?0",
                                "price": None,
                                "wiki_url": f"https://oldschool.runescape.wiki/w/{wiki_name}",
                                "requirements": None,
                                "stats": None,
                                "not_found": True,
                            }
                        )
                except Exception as e:
                    logger.error(
                        f"Error processing item '{item_name}' in slot {slot}: {e}", exc_info=True
                    )
                    # Add fallback entry
                    items_data.append(
                        {
                            "id": None,
                            "name": item_name,
                            "icon": f"https://oldschool.runescape.wiki/images/{item_name.replace(' ', '_')}_detail.png?0",
                            "price": None,
                            "wiki_url": f"https://oldschool.runescape.wiki/w/{item_name.replace(' ', '_')}",
                            "requirements": None,
                            "stats": None,
                            "not_found": True,
                            "error": str(e),
                        }
                    )

            # Add game stage and content tags based on tier name
            tier_name = tier_group.get("tier", "unknown").lower()
            game_stage = _determine_game_stage(tier_name)
            content_tags = _determine_content_tags(tier_name, slot, style)

            enriched_tier = {
                "tier": tier_group.get("tier", "unknown"),
                "game_stage": game_stage,
                "content": content_tags,
                "items": items_data,
            }
            enriched_tiers.append(enriched_tier)
        enriched_data[slot] = enriched_tiers

    return enriched_data


def _determine_game_stage(tier_name: str) -> str:
    """
    Determine game stage based on tier name.

    Args:
        tier_name: Tier name (lowercase)

    Returns:
        Game stage: 'early_game', 'mid_game', or 'late_game'
    """
    # Late game tiers
    late_game_keywords = [
        "torva",
        "masori",
        "zaryte",
        "twisted",
        "avernic",
        "dizana",
        "venator",
        "anguish",
        "torture",
        "suffering",
        "pegasian",
        "primordial",
        "ferocious",
        "inquisitor",
        "oathplate",
    ]

    # Mid game tiers
    mid_game_keywords = [
        "barrows",
        "void",
        "crystal",
        "blowpipe",
        "dragon",
        "rune",
        "armadyl",
        "bandos",
        "guthix",
        "saradomin",
        "zamorak",
    ]

    tier_lower = tier_name.lower()

    if any(keyword in tier_lower for keyword in late_game_keywords):
        return "late_game"
    elif any(keyword in tier_lower for keyword in mid_game_keywords):
        return "mid_game"
    else:
        return "early_game"


def _determine_content_tags(tier_name: str, slot: str, style: str) -> List[str]:
    """
    Determine content tags based on tier name, slot, and style.

    Args:
        tier_name: Tier name (lowercase)
        slot: Equipment slot
        style: Combat style

    Returns:
        List of content tags
    """
    tags = []
    tier_lower = tier_name.lower()

    # General content tags
    if "void" in tier_lower:
        tags.append("Pest Control")
    if "crystal" in tier_lower or "bowfa" in tier_lower or "faerdhinen" in tier_lower:
        tags.append("ToA")
        tags.append("Slayer")
    if "masori" in tier_lower:
        tags.append("ToA")
    if "barrows" in tier_lower:
        tags.append("Barrows")
    if "dragon" in tier_lower and "hunter" in tier_lower:
        tags.append("Dragon")
    if "twisted" in tier_lower:
        tags.append("Raids")
    if "zaryte" in tier_lower:
        tags.append("Nex")
    if "torva" in tier_lower or "avernic" in tier_lower:
        tags.append("GWD")
    if "inquisitor" in tier_lower:
        tags.append("Nightmare")
    if "oathplate" in tier_lower:
        tags.append("Varlamore")

    # Default tags
    if not tags:
        tags.append("General")
        if slot == "weapon":
            tags.append("Questing")

    return tags
