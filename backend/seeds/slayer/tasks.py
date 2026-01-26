"""Slayer task definitions by master."""
from typing import List, Tuple

from backend.models import SlayerMaster


def get_duradel_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Duradel.
    
    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        ("Abyssal demons", 120, 185, 12, True),
        ("Aberrant spectres", 135, 175, 8, True),
        ("Smoke devils", 135, 185, 9, True),
        ("Gargoyles", 130, 200, 9, True),
        ("Nechryaels", 130, 200, 9, True),
        ("Bloodvelds", 130, 200, 8, True),
        ("Dagannoth", 130, 200, 9, True),
        ("Kalphite", 130, 200, 9, True),
        ("Hellhounds", 130, 200, 10, True),
        ("Dust devils", 120, 170, 6, True),
        ("Wyrms", 125, 160, 8, True),
        ("Drakes", 80, 145, 8, True),
        ("Hydras", 135, 160, 10, True),
        ("Kraken", 100, 120, 9, True),
    ]


def get_nieve_tasks() -> List[Tuple[str, int, int, int, bool]]:
    """
    Get task definitions for Nieve.
    
    Returns:
        List of tuples: (category, min_quantity, max_quantity, weight, is_skippable)
    """
    return [
        ("Abyssal demons", 120, 185, 12, True),
        ("Aberrant spectres", 135, 175, 8, True),
        ("Smoke devils", 135, 185, 9, True),
        ("Gargoyles", 130, 200, 9, True),
        ("Nechryaels", 130, 200, 9, True),
        ("Bloodvelds", 130, 200, 8, True),
        ("Dagannoth", 130, 200, 9, True),
        ("Kalphite", 130, 200, 9, True),
        ("Hellhounds", 130, 200, 10, True),
        ("Dust devils", 120, 170, 6, True),
        ("Wyrms", 125, 160, 8, True),
        ("Drakes", 80, 145, 8, True),
        ("Hydras", 135, 160, 10, True),
        ("Kraken", 100, 120, 9, True),
    ]


def get_tasks_by_master() -> dict:
    """
    Get all task definitions organized by master.
    
    Returns:
        Dictionary mapping SlayerMaster to task definitions
    """
    return {
        SlayerMaster.DURADEL: get_duradel_tasks(),
        SlayerMaster.NIEVE: get_nieve_tasks(),
    }
