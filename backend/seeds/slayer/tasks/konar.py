"""Konar slayer task definitions."""

from typing import List, Tuple


def get_konar_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Konar quo Maten (Combat 75+, Slayer 1+).

    Note: Konar assigns location-specific tasks with keys to the brimstone chest.

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
        # Weight 9
        ("Bloodvelds", 130, 200, 9, True),
        ("Dagannoth", 130, 200, 9, True),
        ("Fire giants", 130, 200, 9, True),
        ("Gargoyles", 130, 200, 9, True),
        ("Kalphite", 130, 200, 9, True),
        ("Nechryael", 130, 200, 9, True),
        # Weight 8
        ("Aberrant spectres", 130, 200, 8, True),
        ("Black dragons", 30, 60, 8, True),
        ("Cave kraken", 100, 120, 8, True),
        ("Drakes", 75, 135, 8, True),
        ("Smoke devils", 130, 200, 8, True),
        ("Wyrms", 100, 160, 8, True),
        # Additional tasks...
        ("Blue dragons", 110, 170, 6, True),
        ("Dust devils", 130, 200, 6, True),
        ("Hydras", 125, 190, 6, True),
    ]
