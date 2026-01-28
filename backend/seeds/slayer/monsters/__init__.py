"""Slayer monster definitions with comprehensive OSRS Wiki data."""

from backend.models import Monster

from .demons import get_demon_monsters
from .dragons import get_dragon_monsters
from .undead import get_undead_monsters
from .beasts import get_beast_monsters
from .misc import get_misc_monsters


def get_monster_definitions() -> list[Monster]:
    """
    Get all monster definitions for seeding.

    Source: OSRS Wiki monster pages

    Returns:
        List of Monster instances with accurate combat stats
    """
    return (
        get_demon_monsters()
        + get_dragon_monsters()
        + get_undead_monsters()
        + get_beast_monsters()
        + get_misc_monsters()
    )


__all__ = [
    "get_monster_definitions",
    "get_demon_monsters",
    "get_dragon_monsters",
    "get_undead_monsters",
    "get_beast_monsters",
    "get_misc_monsters",
]
