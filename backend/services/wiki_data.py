"""Wiki progression data - Exact replica of OSRS Wiki Gear Progression Guides (2025/2026 Meta)."""

# Exact replica of Wiki Progression Tables (2025/2026 Meta)
WIKI_PROGRESSION = {
    "melee": {
        "head": [
            {"tier": "Torva", "items": ["Torva full helm"]},
            {"tier": "Inquisitor", "items": ["Inquisitor's great helm"]},
            {"tier": "Oathplate", "items": ["Oathplate helm"]},
            {"tier": "Neitiznot", "items": ["Neitiznot faceguard", "Serpentine helm", "Helm of neitiznot"]},
            {"tier": "Barrows", "items": ["Dharok's helm", "Torag's helm", "Verac's helm", "Ahrim's hood", "Guthan's helm", "Karil's coif"]},
            {"tier": "Mid", "items": ["Berserker helm", "Warrior helm", "Rune full helm"]},
            {"tier": "Low", "items": ["Iron full helm", "Steel full helm", "Mithril full helm", "Adamant full helm"]},
        ],
        "cape": [
            {"tier": "Infernal", "items": ["Infernal cape"]},
            {"tier": "Fire", "items": ["Fire cape"]},
            {"tier": "Mythical", "items": ["Mythical cape"]},
            {"tier": "Ardougne", "items": ["Ardougne cloak 4", "Ardougne cloak 3", "Ardougne cloak 2", "Ardougne cloak 1"]},
            {"tier": "Obsidian", "items": ["Obsidian cape"]},
            {"tier": "Mixed", "items": ["Mixed hide cape"]},
            {"tier": "Low", "items": ["Black cape"]},
        ],
        "neck": [
            {"tier": "BiS", "items": ["Amulet of rancour", "Amulet of torture"]},
            {"tier": "High", "items": ["Amulet of blood fury", "Amulet of fury"]},
            {"tier": "Mid", "items": ["Amulet of glory", "Amulet of power"]},
            {"tier": "Low", "items": ["Amulet of strength"]},
        ],
        "body": [
            {"tier": "Torva", "items": ["Torva platebody"]},
            {"tier": "Inquisitor", "items": ["Inquisitor's hauberk"]},
            {"tier": "Oathplate", "items": ["Oathplate chest"]},
            {"tier": "Bandos", "items": ["Bandos chestplate"]},
            {"tier": "Fighter", "items": ["Fighter torso"]},
            {"tier": "Barrows", "items": ["Dharok's platebody", "Torag's platebody", "Verac's brassard", "Ahrim's robetop", "Guthan's platebody", "Karil's leathertop"]},
            {"tier": "Obsidian", "items": ["Obsidian platebody"]},
            {"tier": "Rune", "items": ["Rune platebody"]},
            {"tier": "Low", "items": ["Iron platebody", "Steel platebody", "Mithril platebody", "Adamant platebody"]},
        ],
        "legs": [
            {"tier": "Torva", "items": ["Torva platelegs"]},
            {"tier": "Inquisitor", "items": ["Inquisitor's plateskirt"]},
            {"tier": "Oathplate", "items": ["Oathplate legs"]},
            {"tier": "Bandos", "items": ["Bandos tassets"]},
            {"tier": "Blood moon", "items": ["Blood moon tassets"]},
            {"tier": "Obsidian", "items": ["Obsidian platelegs"]},
            {"tier": "Barrows", "items": ["Dharok's platelegs", "Torag's platelegs", "Verac's plateskirt", "Ahrim's robeskirt", "Guthan's chainskirt", "Karil's leatherskirt"]},
            {"tier": "Dragon", "items": ["Dragon platelegs", "Dragon plateskirt"]},
            {"tier": "Rune", "items": ["Rune platelegs"]},
            {"tier": "Low", "items": ["Iron platelegs", "Steel platelegs", "Mithril platelegs", "Adamant platelegs"]},
        ],
        "feet": [
            {"tier": "Primordial", "items": ["Primordial boots"]},
            {"tier": "Avernic", "items": ["Avernic treads (pr)", "Avernic treads"]},
            {"tier": "Dragon", "items": ["Dragon boots"]},
            {"tier": "Guardian", "items": ["Guardian boots"]},
            {"tier": "Rune", "items": ["Rune boots"]},
            {"tier": "Climbing", "items": ["Climbing boots"]},
            {"tier": "Fighting", "items": ["Fighting boots"]},
            {"tier": "Leather", "items": ["Leather boots"]},
        ],
        "hands": [
            {"tier": "Ferocious", "items": ["Ferocious gloves"]},
            {"tier": "Barrows", "items": ["Barrows gloves"]},
            {"tier": "Dragon", "items": ["Dragon gloves"]},
            {"tier": "Regen", "items": ["Regen bracelet"]},
            {"tier": "Combat", "items": ["Combat bracelet"]},
            {"tier": "Leather", "items": ["Leather gloves"]},
        ],
        "ring": [
            {"tier": "Ultor", "items": ["Ultor ring"]},
            {"tier": "Bellator", "items": ["Bellator ring"]},
            {"tier": "Berserker", "items": ["Berserker ring (i)", "Berserker ring"]},
            {"tier": "Brimstone", "items": ["Brimstone ring"]},
            {"tier": "Warrior", "items": ["Warrior ring (i)", "Warrior ring"]},
            {"tier": "Explorer", "items": ["Explorer's ring 4", "Explorer's ring 3", "Explorer's ring 2", "Explorer's ring 1"]},
        ],
        "weapon": [
            {"tier": "Scythe", "items": ["Scythe of vitur"]},
            {"tier": "Soulreaper", "items": ["Soulreaper axe"]},
            {"tier": "Rapier/Mace", "items": ["Ghrazi rapier", "Inquisitor's mace"]},
            {"tier": "Blade", "items": ["Blade of saeldor"]},
            {"tier": "Tentacle", "items": ["Abyssal tentacle"]},
            {"tier": "Whip", "items": ["Abyssal whip"]},
            {"tier": "D Scim", "items": ["Dragon scimitar"]},
            {"tier": "Rune", "items": ["Rune scimitar"]},
            {"tier": "Low", "items": ["Iron scimitar", "Steel scimitar", "Mithril scimitar", "Adamant scimitar"]},
        ],
        "shield": [
            {"tier": "Avernic", "items": ["Avernic defender"]},
            {"tier": "Dragon", "items": ["Dragon defender"]},
            {"tier": "DFS", "items": ["Dragonfire shield"]},
            {"tier": "Rune", "items": ["Rune kite shield"]},
            {"tier": "Low", "items": ["Iron kiteshield", "Steel kiteshield", "Mithril kiteshield", "Adamant kiteshield"]},
        ],
        "ammo": [
            {"tier": "Rada", "items": ["Rada's blessing 4", "Rada's blessing 3", "Rada's blessing 2", "Rada's blessing 1"]},
            {"tier": "Peaceful", "items": ["Peaceful blessing"]},
        ],
    },
    "ranged": {
        "head": [
            {"tier": "Masori", "items": ["Masori mask (f)", "Masori mask"]},
            {"tier": "Crystal", "items": ["Crystal helm"]},
            {"tier": "Hueycoatl", "items": ["Hueycoatl hide coif"]},
            {"tier": "Void", "items": ["Void ranger helm"]},
            {"tier": "Guthix", "items": ["Guthix coif"]},
            {"tier": "Archer", "items": ["Archer helm"]},
            {"tier": "Snakeskin", "items": ["Snakeskin bandana"]},
            {"tier": "Coif", "items": ["Coif"]},
            {"tier": "Leather", "items": ["Leather cowl"]},
        ],
        "cape": [
            {"tier": "Dizana", "items": ["Dizana's quiver"]},
            {"tier": "Ava", "items": ["Ava's assembler", "Ava's accumulator", "Ava's attractor"]},
            {"tier": "Ardougne", "items": ["Ardougne cloak 4", "Ardougne cloak 3", "Ardougne cloak 2", "Ardougne cloak 1"]},
            {"tier": "Low", "items": ["Black cape"]},
        ],
        "neck": [
            {"tier": "Anguish", "items": ["Necklace of anguish"]},
            {"tier": "Glory", "items": ["Amulet of glory"]},
            {"tier": "Power", "items": ["Amulet of power"]},
        ],
        "body": [
            {"tier": "Masori", "items": ["Masori body (f)", "Masori body"]},
            {"tier": "Crystal", "items": ["Crystal body"]},
            {"tier": "Elite Void", "items": ["Elite void top"]},
            {"tier": "Hueycoatl", "items": ["Hueycoatl hide body"]},
            {"tier": "Guthix", "items": ["Guthix d'hide body"]},
            {"tier": "Black", "items": ["Black d'hide body"]},
            {"tier": "Blue", "items": ["Blue d'hide body"]},
            {"tier": "Green", "items": ["Green d'hide body"]},
            {"tier": "Mixed", "items": ["Mixed hide top"]},
            {"tier": "Studded", "items": ["Studded body"]},
            {"tier": "Leather", "items": ["Leather body"]},
        ],
        "legs": [
            {"tier": "Masori", "items": ["Masori chaps (f)", "Masori chaps"]},
            {"tier": "Crystal", "items": ["Crystal legs"]},
            {"tier": "Elite Void", "items": ["Elite void robe"]},
            {"tier": "Hueycoatl", "items": ["Hueycoatl hide chaps"]},
            {"tier": "Guthix", "items": ["Guthix chaps"]},
            {"tier": "Black", "items": ["Black d'hide chaps"]},
            {"tier": "Blue", "items": ["Blue d'hide chaps"]},
            {"tier": "Green", "items": ["Green d'hide chaps"]},
            {"tier": "Mixed", "items": ["Mixed hide legs"]},
            {"tier": "Studded", "items": ["Studded chaps"]},
            {"tier": "Leather", "items": ["Leather chaps"]},
        ],
        "feet": [
            {"tier": "Avernic", "items": ["Avernic treads (pe)", "Avernic treads"]},
            {"tier": "Guthix", "items": ["Guthix d'hide boots"]},
            {"tier": "Mixed", "items": ["Mixed hide boots"]},
            {"tier": "Snakeskin", "items": ["Snakeskin boots"]},
            {"tier": "Leather", "items": ["Leather boots"]},
        ],
        "hands": [
            {"tier": "Zaryte", "items": ["Zaryte vambraces"]},
            {"tier": "Void", "items": ["Void knight gloves"]},
            {"tier": "Barrows", "items": ["Barrows gloves"]},
            {"tier": "Green", "items": ["Green d'hide vambraces"]},
            {"tier": "Leather", "items": ["Leather vambraces"]},
        ],
        "ring": [
            {"tier": "Venator", "items": ["Venator ring"]},
            {"tier": "Explorer", "items": ["Explorer's ring 4", "Explorer's ring 3", "Explorer's ring 2", "Explorer's ring 1"]},
        ],
        "weapon": [
            {"tier": "Twisted", "items": ["Twisted bow"]},
            {"tier": "Zaryte", "items": ["Zaryte crossbow"]},
            {"tier": "BowFa", "items": ["Bow of faerdhinen"]},
            {"tier": "Venator", "items": ["Venator bow"]},
            {"tier": "Blowpipe", "items": ["Toxic blowpipe"]},
            {"tier": "Crossbow", "items": ["Armadyl crossbow", "Dragon crossbow", "Dragon hunter crossbow"]},
            {"tier": "Mid", "items": ["Magic shortbow (i)", "Magic shortbow", "Rune crossbow", "Hunters' sunlight crossbow"]},
            {"tier": "Low", "items": ["Dorgeshuun crossbow", "Shortbow", "Oak shortbow", "Willow shortbow", "Maple shortbow"]},
        ],
        "shield": [
            {"tier": "Twisted", "items": ["Twisted buckler"]},
            {"tier": "Dragonfire", "items": ["Dragonfire ward"]},
            {"tier": "Odium", "items": ["Odium ward"]},
            {"tier": "Antler", "items": ["Antler guard"]},
            {"tier": "Book", "items": ["Book of law"]},
            {"tier": "Green", "items": ["Green d'hide shield"]},
        ],
        "ammo": [
            {"tier": "Rada", "items": ["Rada's blessing 4", "Rada's blessing 3", "Rada's blessing 2", "Rada's blessing 1"]},
            {"tier": "Dragon", "items": ["Dragon arrow", "Dragon dart", "Ruby dragon bolts (e)", "Diamond dragon bolts (e)"]},
            {"tier": "Amethyst", "items": ["Amethyst arrow", "Amethyst dart"]},
            {"tier": "Rune", "items": ["Rune arrow", "Rune dart"]},
            {"tier": "Adamant", "items": ["Adamant arrow", "Adamant dart"]},
            {"tier": "Mid", "items": ["Moonlight antler bolts", "Sunlight antler bolts", "Broad bolts", "Diamond bolts (e)", "Ruby bolts (e)"]},
            {"tier": "Low", "items": ["Bone bolts", "Iron arrow", "Steel arrow", "Mithril arrow"]},
        ],
    },
    "magic": {
        "head": [
            {"tier": "Ancestral", "items": ["Ancestral hat"]},
            {"tier": "Virtus", "items": ["Virtus mask"]},
            {"tier": "Ahrim", "items": ["Ahrim's hood"]},
            {"tier": "Void", "items": ["Void mage helm"]},
            {"tier": "Bloodbark", "items": ["Bloodbark helm"]},
            {"tier": "Mystic", "items": ["Mystic hat"]},
            {"tier": "Xerician", "items": ["Xerician hat"]},
            {"tier": "Low", "items": ["Blue wizard hat"]},
        ],
        "cape": [
            {"tier": "Imbued", "items": ["Imbued saradomin cape", "Imbued guthix cape", "Imbued zamorak cape"]},
            {"tier": "Saradomin", "items": ["Saradomin cape"]},
            {"tier": "Ardougne", "items": ["Ardougne cloak 4", "Ardougne cloak 3", "Ardougne cloak 2", "Ardougne cloak 1"]},
            {"tier": "Low", "items": ["Black cape"]},
        ],
        "neck": [
            {"tier": "Occult", "items": ["Occult necklace"]},
            {"tier": "Glory", "items": ["Amulet of glory"]},
            {"tier": "Magic", "items": ["Amulet of magic"]},
        ],
        "body": [
            {"tier": "Ancestral", "items": ["Ancestral robe top"]},
            {"tier": "Virtus", "items": ["Virtus robe top"]},
            {"tier": "Elite Void", "items": ["Elite void top"]},
            {"tier": "Ahrim", "items": ["Ahrim's robetop"]},
            {"tier": "Bloodbark", "items": ["Bloodbark body"]},
            {"tier": "Mystic", "items": ["Mystic robe top"]},
            {"tier": "Xerician", "items": ["Xerician top"]},
            {"tier": "Dagon'hai", "items": ["Dagon'hai robe top"]},
            {"tier": "Low", "items": ["Blue wizard robe"]},
        ],
        "legs": [
            {"tier": "Ancestral", "items": ["Ancestral robe bottom"]},
            {"tier": "Virtus", "items": ["Virtus robe bottom"]},
            {"tier": "Elite Void", "items": ["Elite void robe"]},
            {"tier": "Ahrim", "items": ["Ahrim's robeskirt"]},
            {"tier": "Bloodbark", "items": ["Bloodbark legs"]},
            {"tier": "Mystic", "items": ["Mystic robe bottom"]},
            {"tier": "Xerician", "items": ["Xerician robe"]},
            {"tier": "Dagon'hai", "items": ["Dagon'hai robe bottom"]},
            {"tier": "Low", "items": ["Zamorak monk bottom"]},
        ],
        "feet": [
            {"tier": "Avernic", "items": ["Avernic treads (et)", "Avernic treads"]},
            {"tier": "Eternal", "items": ["Eternal boots"]},
            {"tier": "Infinity", "items": ["Infinity boots"]},
            {"tier": "Mystic", "items": ["Mystic boots"]},
            {"tier": "Bloodbark", "items": ["Bloodbark boots"]},
            {"tier": "Leather", "items": ["Leather boots"]},
        ],
        "hands": [
            {"tier": "Confliction", "items": ["Confliction gauntlets"]},
            {"tier": "Tormented", "items": ["Tormented bracelet"]},
            {"tier": "Void", "items": ["Void knight gloves"]},
            {"tier": "Barrows", "items": ["Barrows gloves"]},
            {"tier": "Combat", "items": ["Combat bracelet"]},
            {"tier": "Leather", "items": ["Leather gloves"]},
        ],
        "ring": [
            {"tier": "Magus", "items": ["Magus ring"]},
            {"tier": "Seers", "items": ["Seers ring (i)", "Seers ring"]},
            {"tier": "Explorer", "items": ["Explorer's ring 3", "Explorer's ring 2", "Explorer's ring 1"]},
        ],
        "weapon": [
            {"tier": "Shadow", "items": ["Tumeken's shadow"]},
            {"tier": "Harmonised", "items": ["Harmonised nightmare staff"]},
            {"tier": "Purging", "items": ["Purging staff"]},
            {"tier": "Sang", "items": ["Sanguinesti staff"]},
            {"tier": "Eye", "items": ["Eye of ayak"]},
            {"tier": "Kodai", "items": ["Kodai wand"]},
            {"tier": "Dragon Hunter", "items": ["Dragon hunter wand"]},
            {"tier": "Toxic Staff", "items": ["Toxic staff of the dead"]},
            {"tier": "Swamp", "items": ["Trident of the swamp"]},
            {"tier": "Seas", "items": ["Trident of the seas"]},
            {"tier": "Ancient", "items": ["Ancient sceptre", "Ancient staff"]},
            {"tier": "Twinflame", "items": ["Twinflame staff"]},
            {"tier": "Warped", "items": ["Warped sceptre"]},
            {"tier": "Iban", "items": ["Iban's staff (u)", "Iban's staff"]},
            {"tier": "Low", "items": ["Staff of air", "Staff of water", "Staff of earth", "Staff of fire"]},
        ],
        "shield": [
            {"tier": "Elidinis", "items": ["Elidinis' ward (f)", "Elidinis' ward"]},
            {"tier": "Mage's", "items": ["Mage's book"]},
            {"tier": "Book", "items": ["Book of darkness"]},
            {"tier": "Tome", "items": ["Tome of fire", "Tome of water", "Tome of earth"]},
        ],
        "ammo": [
            {"tier": "Rada", "items": ["Rada's blessing 4", "Rada's blessing 3", "Rada's blessing 2", "Rada's blessing 1"]},
            {"tier": "Peaceful", "items": ["Peaceful blessing"]},
        ],
    },
}


def get_progression_data(combat_style: str) -> dict:
    """
    Get progression data for a combat style.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        
    Returns:
        Dictionary with progression data for all slots
    """
    return WIKI_PROGRESSION.get(combat_style, {})


def get_slot_progression(combat_style: str, slot: str) -> list:
    """
    Get progression tiers for a specific slot.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        slot: Equipment slot (head, cape, neck, etc.)
        
    Returns:
        List of tier dictionaries with items
    """
    style_data = WIKI_PROGRESSION.get(combat_style, {})
    return style_data.get(slot, [])


def get_all_slots(combat_style: str) -> list:
    """
    Get all available slots for a combat style.
    
    Args:
        combat_style: Combat style (melee, ranged, magic)
        
    Returns:
        List of slot names
    """
    style_data = WIKI_PROGRESSION.get(combat_style, {})
    return list(style_data.keys())
