"""Enum models for the application."""
from enum import Enum


class SlayerMaster(str, Enum):
    """Slayer master enumeration."""
    TURAEL = "Turael"
    SPRIA = "Spria"
    MAZCHNA = "Mazchna"
    VANNAKA = "Vannaka"
    CHAELDAR = "Chaeldar"
    KONAR = "Konar"
    NIEVE = "Nieve"
    DURADEL = "Duradel"


class AttackStyle(str, Enum):
    """Attack style enumeration."""
    STAB = "stab"
    SLASH = "slash"
    CRUSH = "crush"
    MAGIC = "magic"
    RANGED = "ranged"
