"""Dragons Wyverns slayer task data."""

DRAGONS_WYVERNS_TASK_DATA = {
    "Fossil Island wyverns": {
        "weakness": ["Stab", "Dragonbane"],
        "items_needed": [
            "Elemental Shield, Mind Shield, Dragonfire Shield, Dragonfire Ward, OR Ancient Wyvern Shield (MANDATORY - anti-dragon shield does NOT work)"
        ],
        "attack_style": "Melee (Stab) or Ranged",
        "xp_rate": 25000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Decent Prayer XP from wyvern bones, valuable drops (fossils, seaweed spores), chance at rare Wyvern Visage. Spitting Wyverns are fastest to kill.",
        "locations": [
            {
                "name": "Wyvern Cave (Task-only)",
                "requirements": [
                    "66 Slayer (Spitting/Taloned/Long-tailed) OR 82 Slayer (Ancient)",
                    "60 Combat",
                    "Bone Voyage quest",
                    "Elemental Workshop I quest",
                ],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Task-only cave accessed via trapdoor in Mushroom Forest. Spitting Wyverns (Level 139) are fastest to kill - use ranged attacks and weaker icy breath. All wyverns use icy breath that requires specific shields (NOT anti-dragon shield).",
                "pros": [
                    "Task-only area",
                    "Spitting Wyverns fastest",
                    "Decent Prayer XP from bones",
                    "Fossils and seaweed spores",
                    "Chance at Wyvern Visage",
                ],
                "cons": [
                    "Requires specific shields (Elemental/Mind/Dragonfire/Ancient Wyvern)",
                    "Icy breath attacks",
                    "Cannot use anti-dragon shield",
                    "Ancient Wyvern Shield needed for complete freeze immunity",
                ],
                "best_for": "Prayer training and fossil collection",
            },
            {
                "name": "Wyvern Cave (Regular)",
                "requirements": [
                    "66 Slayer (Spitting/Taloned/Long-tailed) OR 82 Slayer (Ancient)",
                    "60 Combat",
                    "Bone Voyage quest",
                    "Elemental Workshop I quest",
                ],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Regular cave south of Museum Camp. Same wyvern variants available. Spitting Wyverns recommended for quick completion.",
                "pros": ["Alternative entrance", "Same wyverns available"],
                "cons": [
                    "May be more crowded",
                    "Same shield requirements",
                    "Same icy breath mechanics",
                ],
                "best_for": "If task-only area unavailable",
            },
        ],
        "alternatives": [
            {
                "name": "Spitting Wyvern",
                "notes": "Level 139, requires 66 Slayer. Fastest to kill. Uses ranged attacks and weaker icy breath. Recommended for quick task completion.",
                "recommended_for": "Fast task completion",
            },
            {
                "name": "Taloned Wyvern",
                "notes": "Level 147, requires 66 Slayer. Uses typeless magic attacks, melee, and icy breath.",
                "recommended_for": "Alternative if Spitting unavailable",
            },
            {
                "name": "Long-tailed Wyvern",
                "notes": "Level 152, requires 66 Slayer. Similar to Taloned but slightly stronger.",
                "recommended_for": "Alternative if Spitting unavailable",
            },
            {
                "name": "Ancient Wyvern",
                "notes": "Level 210, requires 82 Slayer. Highest defence and hitpoints. Best drops but slowest kills.",
                "recommended_for": "High-level players (82 Slayer) for best rewards",
            },
        ],
        "strategy": "Kill Spitting Wyverns for fastest completion - they use ranged attacks (can be prayed against) and weaker icy breath. Bring Elemental Shield, Mind Shield, Dragonfire Shield, Dragonfire Ward, or Ancient Wyvern Shield (anti-dragon shield does NOT work). Only Ancient Wyvern Shield provides complete freeze immunity. Protect from Magic doesn't work against icy breath. Collect wyvern bones for Prayer XP, fossils, and seaweed spores. Chance at rare Wyvern Visage drop.",
    },
}
