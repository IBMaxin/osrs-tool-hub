"""Miscellaneous slayer master task definitions."""

from typing import List, Tuple
from backend.models import SlayerMaster

from .nieve import get_nieve_tasks
from .duradel import get_duradel_tasks
from .konar import get_konar_tasks


def get_turael_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Turael (Combat 0+, Slayer 1+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Turael/Slayer_assignments

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        # Weight 8
        ("Banshees", 15, 30, 8, True),
        ("Cave bugs", 10, 30, 8, True),
        ("Cave crawlers", 15, 30, 8, True),
        ("Cave slime", 10, 20, 8, True),
        ("Cows", 15, 30, 8, True),
        ("Crawling Hands", 15, 30, 8, True),
        ("Icefiends", 15, 20, 8, True),
        ("Lizards", 15, 30, 8, True),
        # Weight 7
        ("Bats", 15, 30, 7, True),
        ("Bears", 10, 20, 7, True),
        ("Dogs", 15, 30, 7, True),
        ("Dwarves", 10, 25, 7, True),
        ("Ghosts", 15, 30, 7, True),
        ("Goblins", 15, 30, 7, True),
        ("Rats", 15, 30, 7, True),
        ("Scorpions", 15, 30, 7, True),
        ("Skeletons", 15, 30, 7, True),
        ("Wolves", 15, 30, 7, True),
        ("Zombies", 15, 30, 7, True),
        # Weight 6
        ("Birds", 15, 30, 6, True),
        ("Kalphite", 15, 30, 6, True),
        ("Monkeys", 15, 30, 6, True),
        ("Spiders", 15, 30, 6, True),
    ]


def get_spria_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Spria (Combat 0+, Slayer 1+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Spria
    Note: Spria has the same tasks as Turael plus Sourhogs.

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    turael_tasks = get_turael_tasks()
    # Add Sourhogs which are unique to Spria
    turael_tasks.append(("Sourhogs", 15, 25, 6, True))
    return turael_tasks


def get_mazchna_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Mazchna (Combat 20+, Slayer 1+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Mazchna

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        # Weight 8
        ("Banshees", 30, 50, 8, True),
        ("Catablepon", 20, 30, 8, True),
        ("Cave bugs", 10, 20, 8, True),
        ("Cave crawlers", 30, 50, 8, True),
        ("Cave slime", 10, 20, 8, True),
        ("Cockatrice", 30, 50, 8, True),
        ("Crawling Hands", 30, 50, 8, True),
        ("Lizards", 30, 50, 8, True),
        ("Mogres", 30, 50, 8, True),
        ("Pyrefiends", 30, 50, 8, True),
        ("Rockslugs", 30, 50, 8, True),
        ("Shades", 30, 70, 8, True),
        # Weight 7
        ("Bats", 30, 50, 7, True),
        ("Dogs", 30, 50, 7, True),
        ("Flesh Crawlers", 15, 25, 7, True),
        ("Ghosts", 30, 50, 7, True),
        ("Ghouls", 10, 20, 7, True),
        ("Hill Giants", 30, 50, 7, True),
        ("Hobgoblins", 30, 50, 7, True),
        ("Ice warriors", 40, 50, 7, True),
        ("Kalphite", 30, 50, 7, True),
        ("Scorpions", 30, 50, 7, True),
        ("Skeletons", 30, 50, 7, True),
        ("Vampyres", 10, 20, 7, True),
        ("Wall beasts", 10, 20, 7, True),
        ("Wolves", 30, 50, 7, True),
        ("Zombies", 30, 50, 7, True),
        # Weight 6
        ("Bears", 30, 50, 6, True),
        ("Killerwatts", 30, 50, 6, True),
    ]


def get_vannaka_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Vannaka (Combat 40+, Slayer 1+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Vannaka

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        # Weight 8
        ("Aberrant spectres", 40, 90, 8, True),
        ("Basilisks", 40, 90, 8, True),
        ("Bloodveld", 40, 90, 8, True),
        ("Cockatrice", 40, 90, 8, True),
        ("Dust devils", 40, 90, 8, True),
        ("Harpie Bug Swarms", 40, 90, 8, True),
        ("Infernal Mages", 40, 90, 8, True),
        ("Jellies", 40, 90, 8, True),
        ("Jungle horrors", 40, 90, 8, True),
        ("Otherworldly beings", 40, 90, 8, True),
        ("Pyrefiends", 40, 90, 8, True),
        ("Shades", 40, 90, 8, True),
        ("Shadow warriors", 30, 80, 8, True),
        ("Spiritual creatures", 40, 90, 8, True),
        ("Turoth", 30, 90, 8, True),
        # Weight 7
        ("Ankou", 25, 35, 7, True),
        ("Blue dragons", 40, 90, 7, True),
        ("Brine rats", 40, 90, 7, True),
        ("Dagannoth", 40, 90, 7, True),
        ("Elves", 30, 70, 7, True),
        ("Fever spiders", 30, 90, 7, True),
        ("Fire giants", 40, 90, 7, True),
        ("Ghouls", 10, 40, 7, True),
        ("Hellhounds", 30, 60, 7, True),
        ("Hill Giants", 40, 90, 7, True),
        ("Hobgoblins", 40, 90, 7, True),
        ("Ice giants", 30, 80, 7, True),
        ("Ice warriors", 40, 90, 7, True),
        ("Kalphite", 40, 90, 7, True),
        ("Kurask", 40, 90, 7, True),
        ("Lesser demons", 40, 90, 7, True),
        ("Mogres", 40, 90, 7, True),
        ("Molanisks", 40, 50, 7, True),
        ("Moss giants", 40, 90, 7, True),
        ("Ogres", 40, 90, 7, True),
        ("Trolls", 40, 90, 7, True),
        ("Vampyres", 10, 20, 7, True),
        ("Werewolves", 30, 60, 7, True),
        # Weight 6
        ("Crocodiles", 40, 90, 6, True),
        ("Sea snakes", 40, 90, 6, True),
        ("Terror dogs", 20, 45, 6, True),
        # Weight 5
        ("Abyssal demons", 40, 90, 5, True),
        ("Gargoyles", 40, 90, 5, True),
        ("Nechryael", 40, 90, 5, True),
    ]


def get_chaeldar_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Chaeldar (Combat 70+, Slayer 1+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Chaeldar

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        # Weight 12
        ("Abyssal demons", 70, 130, 12, True),
        ("Cave kraken", 30, 50, 12, True),
        ("Fire giants", 70, 130, 12, True),
        ("Kurask", 70, 130, 12, True),
        ("Nechryael", 70, 130, 12, True),
        ("Spiritual creatures", 70, 130, 12, True),
        # Weight 11
        ("Dagannoth", 70, 130, 11, True),
        ("Gargoyles", 70, 130, 11, True),
        ("Kalphite", 70, 130, 11, True),
        ("Trolls", 70, 130, 11, True),
        # Weight 10
        ("Black demons", 70, 130, 10, True),
        ("Cave horrors", 70, 130, 10, True),
        ("Jellies", 70, 130, 10, True),
        ("Jungle horrors", 70, 130, 10, True),
        ("Turoth", 70, 130, 10, True),
        # Weight 9
        ("Aviansies", 70, 130, 9, True),
        ("Dust devils", 70, 130, 9, True),
        ("Greater demons", 70, 130, 9, True),
        ("Hellhounds", 70, 130, 9, True),
        ("Lesser demons", 70, 130, 9, True),
        # Weight 8
        ("Aberrant spectres", 70, 130, 8, True),
        ("Basilisks", 70, 130, 8, True),
        ("Bloodveld", 70, 130, 8, True),
        ("Blue dragons", 70, 130, 8, True),
        ("Elves", 70, 130, 8, True),
        ("Shadow warriors", 70, 130, 8, True),
        ("TzHaar", 90, 150, 8, True),
        # Weight 7
        ("Brine rats", 70, 130, 7, True),
        ("Fever spiders", 70, 130, 7, True),
        ("Fossil Island Wyverns", 10, 20, 7, True),
        ("Mutated zygomites", 8, 15, 7, True),
        ("Skeletal Wyverns", 10, 20, 7, True),
        # Weight 6
        ("Lizardmen", 50, 90, 6, True),
        ("Vampyres", 80, 100, 6, True),
        ("Warped creatures", 70, 130, 6, True),
        ("Wyrms", 60, 100, 6, True),
        # Weight 4
        ("Lesser Nagua", 50, 100, 4, True),
    ]


def get_tasks_by_master() -> dict:
    """
    Get all task definitions organized by master.

    Returns:
        Dictionary mapping SlayerMaster to task definitions
    """
    return {
        SlayerMaster.TURAEL: get_turael_tasks(),
        SlayerMaster.SPRIA: get_spria_tasks(),
        SlayerMaster.MAZCHNA: get_mazchna_tasks(),
        SlayerMaster.VANNAKA: get_vannaka_tasks(),
        SlayerMaster.CHAELDAR: get_chaeldar_tasks(),
        SlayerMaster.KONAR: get_konar_tasks(),
        SlayerMaster.NIEVE: get_nieve_tasks(),
        SlayerMaster.DURADEL: get_duradel_tasks(),
    }
