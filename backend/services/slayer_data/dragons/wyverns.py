"""Wyvern and related dragon slayer task data."""

WYVERNS_TASK_DATA = {
    "Drakes": {
        "weakness": ["Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots", "Anti-dragon shield"],
        "attack_style": "Ranged or Melee",
        "xp_rate": 20000,
        "profit_rate": 300000,
        "recommendation": "BLOCK",
        "reason": "High defence, annoying mechanics. Block or skip.",
        "locations": ["Karuulm Slayer Dungeon"],
    },
    "Hydras": {
        "weakness": ["Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots"],
        "attack_style": "Ranged (Tbow/BP) or Melee (Lance)",
        "xp_rate": 30000,
        "profit_rate": 2000000,
        "recommendation": "DO",
        "reason": "Alchemical Hydra is one of the best money makers in the game. Always do.",
        "locations": ["Karuulm Slayer Dungeon"],
    },
    "Wyrms": {
        "weakness": ["Stab", "Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots"],
        "attack_style": "Melee (Stab) or Ranged",
        "xp_rate": 25000,
        "profit_rate": 250000,
        "recommendation": "BLOCK",
        "reason": "Slow and annoying. Drops are okay but generally considered inefficient.",
        "locations": ["Karuulm Slayer Dungeon"],
    },
}
