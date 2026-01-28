"""Script to check if commonly used gear items are present in the database."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session, select
from backend.db.engine import engine
from backend.models import Item

# Commonly used items that should be in the database
COMMON_ITEMS = {
    # Melee Weapons
    "weapon": [
        "Abyssal whip",
        "Abyssal tentacle",
        "Dragon scimitar",
        "Dragon longsword",
        "Dragon dagger",
        "Dragon mace",
        "Dragon sword",
        "Ghrazi rapier",
        "Blade of saeldor",
        "Scythe of vitur",
        "Elder maul",
        "Dragon claws",
        "Dragon warhammer",
        "Bandos godsword",
        "Saradomin godsword",
        "Zamorak godsword",
        "Armadyl godsword",
        "Dragon defender",
        "Avernic defender",
    ],
    # Ranged Weapons
    "ranged_weapon": [
        "Toxic blowpipe",
        "Twisted bow",
        "Bow of faerdhinen (c)",
        "Bow of faerdhinen",
        "Magic shortbow (i)",
        "Magic shortbow",
        "Rune crossbow",
        "Armadyl crossbow",
        "Dragon crossbow",
        "Dragon hunter crossbow",
        "Craw's bow",
        "Webweaver bow",
    ],
    # Magic Weapons
    "magic_weapon": [
        "Trident of the seas",
        "Trident of the swamp",
        "Sanguinesti staff",
        "Tumeken's shadow",
        "Iban's staff (u)",
        "Iban's staff",
        "Ancient staff",
        "Kodai wand",
        "Master wand",
        "Elder wand",
        "Harmonised nightmare staff",
        "Volatile nightmare staff",
        "Eldritch nightmare staff",
    ],
    # Melee Armor - Head
    "head": [
        "Helm of neitiznot",
        "Berserker helm",
        "Serpentine helm",
        "Neitiznot faceguard",
        "Torva full helm",
        "Bandos tassets",  # Actually legs, but checking
        "Bandos chestplate",  # Actually body
        "Justiciar faceguard",
        "Inquisitor's great helm",
    ],
    # Melee Armor - Body
    "body": [
        "Fighter torso",
        "Bandos chestplate",
        "Torva platebody",
        "Justiciar chestguard",
        "Inquisitor's hauberk",
        "Rune platebody",
        "Dragon chainbody",
    ],
    # Melee Armor - Legs
    "legs": [
        "Bandos tassets",
        "Torva platelegs",
        "Justiciar legguards",
        "Inquisitor's plateskirt",
        "Obsidian platelegs",
        "Rune platelegs",
    ],
    # Ranged Armor
    "ranged_armor": [
        "Armadyl helmet",
        "Armadyl chestplate",
        "Armadyl chainskirt",
        "Pegasian boots",
        "Masori mask",
        "Masori body",
        "Masori chaps",
        "Crystal helm",
        "Crystal body",
        "Crystal legs",
        "Black d'hide body",
        "Black d'hide chaps",
        "Black d'hide vambraces",
        "God d'hide body",
        "God d'hide chaps",
        "God d'hide vambraces",
        "Zaryte vambraces",
    ],
    # Magic Armor
    "magic_armor": [
        "Ancestral hat",
        "Ancestral robe top",
        "Ancestral robe bottom",
        "Ahrim's hood",
        "Ahrim's robetop",
        "Ahrim's robeskirt",
        "Virtus mask",
        "Virtus robe top",
        "Virtus robe bottom",
        "Mystic hat",
        "Mystic robe top",
        "Mystic robe bottom",
        "Infinity hat",
        "Infinity top",
        "Infinity bottoms",
    ],
    # Accessories
    "cape": [
        "Fire cape",
        "Infernal cape",
        "Ava's accumulator",
        "Ava's assembler",
        "Ardougne cloak 1",
        "Ardougne cloak 2",
        "Ardougne cloak 3",
        "Ardougne cloak 4",
        "God cape",
        "Imbued god cape",
        "Mythical cape",
    ],
    "neck": [
        "Amulet of torture",
        "Amulet of fury",
        "Amulet of glory",
        "Amulet of strength",
        "Occult necklace",
        "Necklace of anguish",
        "Amulet of magic",
    ],
    "ring": [
        "Berserker ring (i)",
        "Berserker ring",
        "Warrior ring (i)",
        "Warrior ring",
        "Archers ring (i)",
        "Archers ring",
        "Seers ring (i)",
        "Seers ring",
        "Ultor ring",
        "Bellator ring",
        "Venator ring",
        "Magus ring",
        "Ring of wealth",
    ],
    "hands": [
        "Barrows gloves",
        "Ferocious gloves",
        "Combat bracelet",
        "Regen bracelet",
        "Tormented bracelet",
    ],
    "feet": [
        "Primordial boots",
        "Dragon boots",
        "Rune boots",
        "Eternal boots",
        "Infinity boots",
        "Pegasian boots",
    ],
    "shield": [
        "Dragon defender",
        "Avernic defender",
        "Dragonfire shield",
        "Dragonfire ward",
        "Elysian spirit shield",
        "Spectral spirit shield",
        "Arcane spirit shield",
        "Malediction ward",
        "Odium ward",
        "Book of darkness",
        "Unholy book",
        "Elidinis' ward (f)",
    ],
    "ammo": [
        "Amethyst arrow",
        "Rune arrow",
        "Dragon arrow",
        "Amethyst dart",
        "Rune dart",
        "Dragon dart",
        "Broad bolts",
        "Diamond bolts (e)",
        "Ruby bolts (e)",
        "Dragon bolts (e)",
    ],
}


def check_items(session: Session) -> dict:
    """Check which common items are present and have stats."""
    results = {
        "found": [],
        "missing": [],
        "missing_stats": [],
        "total_checked": 0,
    }

    for category, item_names in COMMON_ITEMS.items():
        for item_name in item_names:
            results["total_checked"] += 1
            # Search for item by name (case-insensitive)
            # Try exact match first, then try with common variants
            query = select(Item).where(Item.name.ilike(item_name))
            item = session.exec(query).first()
            
            # If not found, try common variants (inactive, uncharged, empty, etc.)
            if not item:
                # Try with common suffixes
                variants = [
                    f"{item_name} (inactive)",
                    f"{item_name} (uncharged)",
                    f"{item_name} (empty)",
                    f"{item_name} (full)",
                    f"{item_name} (u)",
                ]
                for variant in variants:
                    query = select(Item).where(Item.name.ilike(variant))
                    item = session.exec(query).first()
                    if item:
                        break
                
                # Also try partial match (for items like "Blade of saeldor" matching "Blade of saeldor (inactive)")
                if not item:
                    # Extract base name (remove common suffixes from search)
                    base_name = item_name.split(" (")[0]
                    query = select(Item).where(Item.name.ilike(f"{base_name}%"))
                    items = list(session.exec(query).all())
                    # Prefer items with stats
                    item_with_stats = next((i for i in items if i.slot), None)
                    item = item_with_stats or (items[0] if items else None)

            if not item:
                results["missing"].append(f"{category}: {item_name}")
            elif not item.slot:
                # Item exists but doesn't have slot/stats populated
                results["missing_stats"].append(f"{category}: {item_name} -> Found: {item.name} (ID: {item.id})")
            else:
                # Found with stats - note if it's a variant name
                if item.name.lower() != item_name.lower():
                    results["found"].append(f"{category}: {item_name} -> {item.name}")
                else:
                    results["found"].append(f"{category}: {item_name}")

    return results


def main():
    """Run the check."""
    print("Checking for commonly used gear items...")
    print("=" * 60)

    with Session(engine) as session:
        results = check_items(session)

        print(f"\n✅ Found: {len(results['found'])} items")
        print(f"❌ Missing: {len(results['missing'])} items")
        print(f"⚠️  Missing Stats: {len(results['missing_stats'])} items")
        print(f"📊 Total Checked: {results['total_checked']} items")

        if results["missing"]:
            print("\n" + "=" * 60)
            print("MISSING ITEMS:")
            print("=" * 60)
            for item in results["missing"][:20]:  # Show first 20
                print(f"  - {item}")
            if len(results["missing"]) > 20:
                print(f"  ... and {len(results['missing']) - 20} more")

        if results["missing_stats"]:
            print("\n" + "=" * 60)
            print("ITEMS WITHOUT STATS (need to run sync-stats):")
            print("=" * 60)
            for item in results["missing_stats"][:20]:  # Show first 20
                print(f"  - {item}")
            if len(results["missing_stats"]) > 20:
                print(f"  ... and {len(results['missing_stats']) - 20} more")

        # Check total items in DB
        total_items = session.exec(select(Item)).all()
        equipable_items = [item for item in total_items if item.slot]
        
        print("\n" + "=" * 60)
        print("DATABASE STATISTICS:")
        print("=" * 60)
        print(f"Total items in DB: {len(total_items)}")
        print(f"Items with equipment stats: {len(equipable_items)}")
        print(f"Items without stats: {len(total_items) - len(equipable_items)}")

        if results["missing_stats"]:
            print("\n⚠️  WARNING: Some items exist but don't have stats populated.")
            print("   Run: POST /api/v1/admin/sync-stats to populate item stats.")


if __name__ == "__main__":
    main()
