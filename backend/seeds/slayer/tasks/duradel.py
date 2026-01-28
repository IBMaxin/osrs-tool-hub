"""Duradel slayer task definitions."""

from typing import List, Tuple


def get_duradel_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Duradel (Combat 100+, Slayer 50+).

    Source: OSRS Wiki - https://oldschool.runescape.wiki/w/Duradel

    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        # Weight 12
        ("Abyssal demons", 120, 185, 12, True),
        # Weight 10
        ("Black demons", 180, 250, 10, True),
        ("Greater demons", 150, 200, 10, True),
        ("Hellhounds", 130, 200, 10, True),
        ("Hydras", 125, 190, 10, True),
        # Weight 9
        ("Bloodvelds", 130, 200, 9, True),
        ("Dagannoth", 130, 200, 9, True),
        ("Gargoyles", 130, 200, 9, True),
        ("Kalphite", 130, 200, 9, True),
        ("Kraken", 100, 120, 9, True),
        ("Nechryael", 130, 200, 9, True),
        ("Smoke devils", 130, 200, 9, True),
        # Weight 8
        ("Aberrant spectres", 130, 200, 8, True),
        ("Ankou", 50, 90, 8, True),
        ("Black dragons", 30, 60, 8, True),
        ("Cave kraken", 100, 120, 8, True),
        ("Drakes", 75, 135, 8, True),
        ("Fire giants", 130, 200, 8, True),
        ("Skeletal wyverns", 5, 12, 8, True),
        ("Wyrms", 100, 160, 8, True),
        # Weight 7
        ("Bronze dragons", 30, 60, 7, True),
        ("Fossil Island wyverns", 20, 60, 7, True),
        ("Iron dragons", 30, 60, 7, True),
        ("Steel dragons", 30, 60, 7, True),
        ("Suqah", 60, 90, 7, True),
        ("TzHaar", 110, 180, 7, True),
        ("Waterfiends", 130, 200, 7, True),
        # Weight 6
        ("Blue dragons", 110, 170, 6, True),
        ("Dust devils", 130, 200, 6, True),
        ("Elves", 60, 90, 6, True),
        ("Mithril dragons", 5, 10, 6, True),
        ("Mutated zygomites", 10, 25, 6, True),
        ("Red dragons", 30, 60, 6, True),
        ("Trolls", 120, 150, 6, True),
        # Weight 5
        ("Adamant dragons", 4, 9, 5, True),
        ("Aviansies", 120, 200, 5, True),
        ("Rune dragons", 3, 8, 5, True),
        ("Spiritual creatures", 120, 185, 5, True),
        # Weight 2
        ("Boss", 3, 35, 2, True),
    ]
