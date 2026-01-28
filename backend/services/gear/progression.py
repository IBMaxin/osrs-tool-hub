"""Wiki progression and preset loadout utilities."""

import logging
from typing import Dict, List, Optional, Set
from sqlmodel import Session, select

from backend.models import PriceSnapshot
from backend.services.gear_presets import GEAR_PRESETS
from backend.services.wiki_data import WIKI_PROGRESSION
from backend.services.gear.utils import find_item_by_name
from backend.services.gear.pricing import get_item_price
from backend.services.gear.loadouts import get_upgrade_path


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

    preset = GEAR_PRESETS[combat_style][tier]
    loadout = {
        "combat_style": combat_style,
        "tier": tier,
        "slots": {},
        "total_cost": 0,
        "missing_items": [],
    }

    # Process each slot
    for slot, item_names in preset.items():
        if not item_names:  # Empty slot (e.g., shield for 2H weapons)
            loadout["slots"][slot] = None
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

            item_price = price_snapshot.high_price if price_snapshot else item.value or 0
            loadout["total_cost"] += item_price

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

            loadout["slots"][slot] = item_data
        else:
            # Item not found in database
            loadout["slots"][slot] = None
            loadout["missing_items"].append({"slot": slot, "names": item_names})

    return loadout


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
        "torva", "masori", "zaryte", "twisted", "avernic", "dizana",
        "venator", "anguish", "torture", "suffering", "pegasian",
        "primordial", "ferocious", "inquisitor", "oathplate"
    ]
    
    # Mid game tiers
    mid_game_keywords = [
        "barrows", "void", "crystal", "blowpipe", "dragon", "rune",
        "armadyl", "bandos", "guthix", "saradomin", "zamorak"
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

        # Determine content tag based on unlocked content
        content_tag = None
        if unlocked_content:
            # Map content to content tags
            if "ToA" in unlocked_content or "toa" in [c.lower() for c in unlocked_content]:
                content_tag = "toa_entry"
            elif "GWD" in unlocked_content or "gwd" in [c.lower() for c in unlocked_content]:
                content_tag = "gwd"

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
