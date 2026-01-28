"""Gear presets based on OSRS meta progression tiers."""

# Progression tiers based on standard OSRS meta (Wiki/Community guides)
GEAR_PRESETS = {
    "melee": {
        "low": {
            # ~Lv 60 stats, < 500k budget
            "head": ["Helm of neitiznot", "Berserker helm"],
            "cape": ["Obsidian cape", "Ardougne cloak 1"],
            "neck": ["Amulet of glory"],
            "weapon": ["Dragon scimitar"],
            "body": ["Fighter torso", "Rune platebody"],
            "shield": ["Dragon defender", "Rune kite shield"],
            "legs": ["Obsidian platelegs", "Rune platelegs"],
            "hands": ["Combat bracelet"],
            "feet": ["Rune boots", "Climbing boots"],
            "ring": ["Ring of wealth", "Explorer's ring 2"],
        },
        "mid": {
            # ~Lv 75 stats, ~20m budget
            "head": ["Serpentine helm", "Neitiznot faceguard"],
            "cape": ["Fire cape"],
            "neck": ["Amulet of torture", "Amulet of fury"],
            "weapon": ["Abyssal whip", "Abyssal tentacle"],
            "body": ["Fighter torso", "Bandos chestplate"],
            "shield": ["Dragon defender"],
            "legs": ["Bandos tassets", "Obsidian platelegs"],
            "hands": ["Ferocious gloves", "Barrows gloves"],
            "feet": ["Primordial boots", "Dragon boots"],
            "ring": ["Berserker ring (i)"],
        },
        "high": {
            # Max stats, ~500m+ budget
            "head": ["Torva full helm"],
            "cape": ["Infernal cape", "Fire cape"],
            "neck": ["Amulet of torture"],
            "weapon": ["Ghrazi rapier", "Blade of saeldor"],
            "body": ["Torva platebody"],
            "shield": ["Avernic defender"],
            "legs": ["Torva platelegs"],
            "hands": ["Ferocious gloves"],
            "feet": ["Primordial boots"],
            "ring": ["Ultor ring", "Bellator ring"],
        },
    },
    "ranged": {
        "low": {
            # ~Lv 50-60, cheap
            "head": ["Archer helm", "Coif"],
            "cape": ["Ava's accumulator"],
            "neck": ["Amulet of glory"],
            "weapon": ["Magic shortbow (i)", "Rune crossbow"],
            "ammo": ["Amethyst arrow", "Broad bolts"],
            "body": ["Black d'hide body"],
            "shield": ["Unholy book"],  # For crossbow
            "legs": ["Black d'hide chaps"],
            "hands": ["Black d'hide vambraces"],
            "feet": ["Snakeskin boots"],
            "ring": ["Explorer's ring 2"],
        },
        "mid": {
            # ~Lv 75-80, Blowpipe era
            "head": ["God coif"],
            "cape": ["Ava's assembler"],
            "neck": ["Necklace of anguish", "Amulet of fury"],
            "weapon": ["Toxic blowpipe"],
            "ammo": ["Amethyst dart"],
            "body": ["Blessed body"],
            "shield": [],  # 2H weapon
            "legs": ["Blessed chaps"],
            "hands": ["Barrows gloves"],
            "feet": ["God d'hide boots"],
            "ring": ["Archers ring (i)"],
        },
        "high": {
            # BowFa / Masori
            "head": ["Crystal helm"],
            "cape": ["Ava's assembler"],
            "neck": ["Necklace of anguish"],
            "weapon": ["Bow of faerdhinen (c)"],
            "ammo": ["Ammo slot"],  # Hidden/None
            "body": ["Crystal body"],
            "shield": [],
            "legs": ["Crystal legs"],
            "hands": ["Barrows gloves", "Zaryte vambraces"],
            "feet": ["Pegasian boots"],
            "ring": ["Venator ring", "Archers ring (i)"],
        },
    },
    "magic": {
        "low": {
            "head": ["Mystic hat"],
            "cape": ["God cape"],
            "neck": ["Amulet of magic"],
            "weapon": ["Iban's staff (u)", "Ancient staff"],
            "body": ["Mystic robe top"],
            "shield": ["Broodoo shield", "Book of darkness"],
            "legs": ["Mystic robe bottom"],
            "hands": ["Mystic gloves"],
            "feet": ["Mystic boots"],
            "ring": ["Seers ring"],
        },
        "mid": {
            "head": ["Ahrim's hood"],
            "cape": ["Imbued god cape"],
            "neck": ["Occult necklace"],
            "weapon": ["Trident of the swamp", "Trident of the seas"],
            "body": ["Ahrim's robetop"],
            "shield": ["Malediction ward", "Book of darkness"],
            "legs": ["Ahrim's robeskirt"],
            "hands": ["Tormented bracelet"],
            "feet": ["Eternal boots", "Infinity boots"],
            "ring": ["Seers ring (i)"],
        },
        "high": {
            "head": ["Ancestral hat"],
            "cape": ["Imbued god cape"],
            "neck": ["Occult necklace"],
            "weapon": ["Tumeken's shadow", "Sanguinesti staff"],
            "body": ["Ancestral robe top"],
            "shield": ["Elidinis' ward (f)"],
            "legs": ["Ancestral robe bottom"],
            "hands": ["Tormented bracelet"],
            "feet": ["Eternal boots"],
            "ring": ["Magus ring"],
        },
    },
}
