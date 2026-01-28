"""Item stats importer from OSRSBox."""

import httpx
from sqlmodel import Session, select
from backend.models import Item
import logging

logger = logging.getLogger(__name__)


async def import_item_stats(session: Session):
    """Fetch item stats from OSRSBox and update DB."""
    url = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/master/docs/items-complete.json"

    logger.info("Fetching item stats from OSRSBox...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        logger.error(f"Failed to download stats: {e}")
        return

    logger.info(f"Loaded {len(data)} items from JSON. Updating DB...")

    updated_count = 0
    skipped_not_equipable = 0
    skipped_not_in_data = 0

    # Iterate through all items in our DB
    db_items = session.exec(select(Item)).all()
    logger.info(f"Found {len(db_items)} items in database to check")

    for item in db_items:
        str_id = str(item.id)
        if str_id not in data:
            skipped_not_in_data += 1
            continue

        stats = data[str_id]
        equipment = stats.get("equipment") or {}
        requirements = stats.get("requirements") or {}
        weapon = stats.get("weapon") or {}

        # Skip if not equipable
        if not stats.get("equipable_by_player"):
            skipped_not_equipable += 1
            continue

        # Update fields
        item.slot = equipment.get("slot")

        # Requirements
        item.attack_req = requirements.get("attack", 1)
        item.defence_req = requirements.get("defence", 1)
        item.strength_req = requirements.get("strength", 1)
        item.ranged_req = requirements.get("ranged", 1)
        item.magic_req = requirements.get("magic", 1)
        item.prayer_req = requirements.get("prayer", 1)
        item.slayer_req = requirements.get("slayer", 0)

        # Quest/Achievement requirements (from OSRSBox quest field if available)
        quest_req = stats.get("quest", None)
        if quest_req:
            item.quest_req = quest_req

        # Equipment metadata
        weapon_type = weapon.get("weapon_type", "") if weapon else ""
        item.is_2h = weapon_type in ["2h_sword", "2h_axe", "bow", "crossbow", "staff", "polearm"]
        item.attack_speed = weapon.get("weapon_speed", 4) if weapon else 4  # Default to 4 ticks

        # Offensive Stats
        item.attack_stab = equipment.get("attack_stab", 0)
        item.attack_slash = equipment.get("attack_slash", 0)
        item.attack_crush = equipment.get("attack_crush", 0)
        item.attack_magic = equipment.get("attack_magic", 0)
        item.attack_ranged = equipment.get("attack_ranged", 0)

        # Strength Bonuses
        item.melee_strength = equipment.get("melee_strength", 0)
        item.ranged_strength = equipment.get("ranged_strength", 0)
        item.magic_damage = equipment.get("magic_damage", 0)
        item.prayer_bonus = equipment.get("prayer", 0)

        # Defensive Stats
        item.defence_stab = equipment.get("defence_stab", 0)
        item.defence_slash = equipment.get("defence_slash", 0)
        item.defence_crush = equipment.get("defence_crush", 0)
        item.defence_magic = equipment.get("defence_magic", 0)
        item.defence_ranged = equipment.get("defence_ranged", 0)

        session.add(item)
        updated_count += 1

    session.commit()
    logger.info(
        f"Updated stats for {updated_count} items. "
        f"Skipped {skipped_not_equipable} non-equipable items. "
        f"Skipped {skipped_not_in_data} items not in OSRSBox data."
    )
