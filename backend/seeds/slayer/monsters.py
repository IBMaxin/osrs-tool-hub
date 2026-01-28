"""Slayer monster definitions with comprehensive OSRS Wiki data."""

from backend.models import Monster


def get_monster_definitions() -> list[Monster]:
    """
    Get all monster definitions for seeding.

    Source: OSRS Wiki monster pages

    Returns:
        List of Monster instances with accurate combat stats
    """
    return [
        # High-level demons
        Monster(
            id=415,
            name="Abyssal demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150,
            slayer_category="Abyssal demons",
            is_demon=True,
        ),
        Monster(
            id=84,
            name="Greater demon",
            combat_level=92,
            hitpoints=87,
            slayer_xp=87,
            slayer_category="Greater demons",
            is_demon=True,
        ),
        Monster(
            id=83,
            name="Black demon",
            combat_level=172,
            hitpoints=157,
            slayer_xp=157,
            slayer_category="Black demons",
            is_demon=True,
        ),
        Monster(
            id=16,
            name="Nechryael",
            combat_level=115,
            hitpoints=105,
            slayer_xp=105,
            slayer_category="Nechryael",
            is_demon=True,
        ),
        # Hellhounds and variants
        Monster(
            id=4,
            name="Hellhound",
            combat_level=122,
            hitpoints=116,
            slayer_xp=116,
            slayer_category="Hellhounds",
            is_demon=True,
        ),
        # Spectres and ghosts
        Monster(
            id=11,
            name="Aberrant spectre",
            combat_level=96,
            hitpoints=90,
            slayer_xp=90,
            slayer_category="Aberrant spectres",
        ),
        Monster(
            id=90,
            name="Ankou",
            combat_level=86,
            hitpoints=60,
            slayer_xp=60,
            slayer_category="Ankou",
        ),
        # Bloodvelds
        Monster(
            id=120,
            name="Bloodveld",
            combat_level=76,
            hitpoints=120,
            slayer_xp=120,
            slayer_category="Bloodvelds",
        ),
        # Devils
        Monster(
            id=498,
            name="Smoke devil",
            combat_level=160,
            hitpoints=185,
            slayer_xp=185,
            slayer_category="Smoke devils",
        ),
        Monster(
            id=9,
            name="Dust devil",
            combat_level=93,
            hitpoints=105,
            slayer_xp=105,
            slayer_category="Dust devils",
        ),
        # Gargoyles
        Monster(
            id=122,
            name="Gargoyle",
            combat_level=111,
            hitpoints=105,
            slayer_xp=105,
            slayer_category="Gargoyles",
        ),
        # Dagannoth
        Monster(
            id=54,
            name="Dagannoth",
            combat_level=90,
            hitpoints=70,
            slayer_xp=70,
            slayer_category="Dagannoth",
        ),
        # Kalphites
        Monster(
            id=10,
            name="Kalphite",
            combat_level=28,
            hitpoints=40,
            slayer_xp=40,
            slayer_category="Kalphite",
            is_kalphite=True,
        ),
        # Kraken
        Monster(
            id=31,
            name="Kraken",
            combat_level=291,
            hitpoints=255,
            slayer_xp=255,
            slayer_category="Kraken",
        ),
        Monster(
            id=32,
            name="Cave kraken",
            combat_level=127,
            hitpoints=125,
            slayer_xp=125,
            slayer_category="Cave kraken",
        ),
        # Hydras and Fossil Island creatures
        Monster(
            id=24,
            name="Hydra",
            combat_level=194,
            hitpoints=300,
            slayer_xp=660,
            slayer_category="Hydras",
            is_dragon=True,
        ),
        Monster(
            id=14,
            name="Wyrm",
            combat_level=62,
            hitpoints=100,
            slayer_xp=133.2,
            slayer_category="Wyrms",
            is_dragon=True,
        ),
        Monster(
            id=15,
            name="Drake",
            combat_level=84,
            hitpoints=250,
            slayer_xp=316.8,
            slayer_category="Drakes",
            is_dragon=True,
        ),
        # Metal dragons
        Monster(
            id=270,
            name="Bronze dragon",
            combat_level=131,
            hitpoints=80,
            slayer_xp=80,
            slayer_category="Bronze dragons",
            is_dragon=True,
        ),
        Monster(
            id=274,
            name="Iron dragon",
            combat_level=189,
            hitpoints=160,
            slayer_xp=173.2,
            slayer_category="Iron dragons",
            is_dragon=True,
        ),
        Monster(
            id=273,
            name="Steel dragon",
            combat_level=246,
            hitpoints=210,
            slayer_xp=220.2,
            slayer_category="Steel dragons",
            is_dragon=True,
        ),
        Monster(
            id=5362,
            name="Mithril dragon",
            combat_level=304,
            hitpoints=255,
            slayer_xp=273,
            slayer_category="Mithril dragons",
            is_dragon=True,
        ),
        Monster(
            id=8090,
            name="Adamant dragon",
            combat_level=338,
            hitpoints=300,
            slayer_xp=331.8,
            slayer_category="Adamant dragons",
            is_dragon=True,
        ),
        Monster(
            id=8091,
            name="Rune dragon",
            combat_level=380,
            hitpoints=330,
            slayer_xp=382.5,
            slayer_category="Rune dragons",
            is_dragon=True,
        ),
        # Chromatic dragons
        Monster(
            id=262,
            name="Black dragon",
            combat_level=227,
            hitpoints=190,
            slayer_xp=199.5,
            slayer_category="Black dragons",
            is_dragon=True,
        ),
        Monster(
            id=268,
            name="Blue dragon",
            combat_level=111,
            hitpoints=105,
            slayer_xp=107.5,
            slayer_category="Blue dragons",
            is_dragon=True,
        ),
        Monster(
            id=269,
            name="Red dragon",
            combat_level=152,
            hitpoints=140,
            slayer_xp=145.5,
            slayer_category="Red dragons",
            is_dragon=True,
        ),
        # Wyverns
        Monster(
            id=466,
            name="Skeletal wyvern",
            combat_level=140,
            hitpoints=210,
            slayer_xp=210,
            slayer_category="Skeletal wyverns",
        ),
        Monster(
            id=8071,
            name="Ancient wyvern",
            combat_level=210,
            hitpoints=275,
            slayer_xp=312.3,
            slayer_category="Fossil Island wyverns",
        ),
        # TzHaar
        Monster(
            id=2190,
            name="TzHaar-Ket",
            combat_level=149,
            hitpoints=130,
            slayer_xp=104,
            slayer_category="TzHaar",
        ),
        # Fire giants
        Monster(
            id=109,
            name="Fire giant",
            combat_level=86,
            hitpoints=111,
            slayer_xp=111,
            slayer_category="Fire giants",
        ),
        # Waterfiends
        Monster(
            id=5361,
            name="Waterfiend",
            combat_level=115,
            hitpoints=95,
            slayer_xp=128,
            slayer_category="Waterfiends",
        ),
        # Aviansies
        Monster(
            id=3169,
            name="Aviansie",
            combat_level=69,
            hitpoints=80,
            slayer_xp=86.9,
            slayer_category="Aviansies",
        ),
        # Spiritual creatures
        Monster(
            id=2244,
            name="Spiritual warrior",
            combat_level=98,
            hitpoints=96,
            slayer_xp=98.5,
            slayer_category="Spiritual creatures",
        ),
        # Suqah
        Monster(
            id=4527,
            name="Suqah",
            combat_level=111,
            hitpoints=106,
            slayer_xp=106,
            slayer_category="Suqah",
        ),
        # Elves
        Monster(
            id=2359,
            name="Iorwerth Archer",
            combat_level=108,
            hitpoints=104,
            slayer_xp=105,
            slayer_category="Elves",
        ),
        # Trolls
        Monster(
            id=1106,
            name="Mountain troll",
            combat_level=69,
            hitpoints=50,
            slayer_xp=50,
            slayer_category="Trolls",
        ),
        # Mutated zygomites
        Monster(
            id=3347,
            name="Mutated zygomite",
            combat_level=74,
            hitpoints=65,
            slayer_xp=75,
            slayer_category="Mutated zygomites",
        ),
        # Nieve/Steve specific
        Monster(
            id=2831,
            name="Brine rat",
            combat_level=70,
            hitpoints=50,
            slayer_xp=45,
            slayer_category="Brine rats",
        ),
        Monster(
            id=1626,
            name="Turoth",
            combat_level=83,
            hitpoints=76,
            slayer_xp=76,
            slayer_category="Turoth",
        ),
        Monster(
            id=6575,
            name="Scabarite",
            combat_level=73,
            hitpoints=85,
            slayer_xp=85,
            slayer_category="Scabarites",
        ),
        # Boss placeholder (for boss tasks)
        Monster(
            id=9999,
            name="Boss",
            combat_level=200,
            hitpoints=500,
            slayer_xp=1000,
            slayer_category="Boss",
        ),
    ]
