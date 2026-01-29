"""Misc slayer task data - Part 1."""

MISC_TASK_DATA_PART1 = {
    "Dagannoth": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee (Cannon) or Magic (Burst)",
        "xp_rate": 60000,
        "profit_rate": 50000,
        "recommendation": "DO",
        "reason": "Extremely fast XP with a cannon in Lighthouse. Can also do Dagannoth Kings for profit.",
        "locations": [
            {
                "name": "Lighthouse",
                "requirements": ["Horror from the Deep quest"],
                "multi_combat": True,
                "cannon": True,
                "safespot": True,
                "notes": "Best location. Cannon dagannoths on bottom floor. Very fast task.",
                "pros": ["Cannon allowed", "Safespot available", "Very fast", "Excellent XP/hr"],
                "cons": ["Uses many cannonballs", "Requires quest"],
                "best_for": "Fast XP with cannon",
            },
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Alternative without cannon. Can burst but less efficient.",
                "pros": ["Prayer restoration", "No cannonball cost"],
                "cons": ["Slower than Lighthouse", "Spread out spawns"],
                "best_for": "If out of cannonballs",
            },
        ],
        "alternatives": [
            {
                "name": "Dagannoth Kings",
                "notes": "Boss trio. Excellent profit (Dragon axes, Berserker ring, Archers ring, Seers ring). Requires tribrid gear.",
                "recommended_for": "Experienced players with tribrid setup",
            }
        ],
        "strategy": "Cannon in Lighthouse for maximum XP. Safespot behind rocks. Bring many cannonballs. Do DKs if you have good gear and want profit over XP.",
    },
    "Kalphite": {
        "weakness": ["Keris"],
        "items_needed": [],
        "attack_style": "Melee (Cannon)",
        "xp_rate": 50000,
        "profit_rate": 20000,
        "recommendation": "DO",
        "reason": "Very fast points/XP with cannon (Workers). Can do Kalphite Queen for boss task.",
        "locations": [
            {
                "name": "Kalphite Cave",
                "requirements": [],
                "multi_combat": True,
                "cannon": True,
                "safespot": True,
                "notes": "Kill Workers in main cave. Very fast with cannon. Safespot available.",
                "pros": ["Cannon allowed", "Safespot available", "Very fast", "No requirements"],
                "cons": ["Low profit", "Uses cannonballs"],
                "best_for": "Fast slayer points",
            }
        ],
        "alternatives": [
            {
                "name": "Kalphite Queen",
                "notes": "Boss variant. Dragon chainbody drop. Requires gear switches (ranged + melee).",
                "recommended_for": "Players wanting boss slayer",
            }
        ],
        "strategy": "Cannon Kalphite Workers for fastest task completion. Use Keris partisan if you have it for bonus damage. Safespot to minimize damage taken.",
    },
    "Turoth": {
        "weakness": ["Leaf-bladed weapons", "Broad arrows/bolts", "Magic Dart"],
        "items_needed": [
            "Leaf-bladed battleaxe/sword/spear/axe",
            "Broad arrows/bolts",
            "OR Slayer's staff (e) for Magic Dart",
        ],
        "attack_style": "Melee (Leaf-bladed) or Ranged (Broad bolts) or Magic (Magic Dart)",
        "xp_rate": 20000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Good profit from herbs, seeds, and alchables. Decent XP with leaf-bladed battleaxe.",
        "locations": [
            {
                "name": "Fremennik Slayer Dungeon",
                "requirements": ["55 Slayer"],
                "multi_combat": False,
                "cannon": False,
                "safespot": True,
                "notes": "Only location for Turoths. Non-aggressive. Can use Protect from Melee. Agility shortcuts available (62 and 81 Agility).",
                "pros": [
                    "Non-aggressive",
                    "Safespot available",
                    "Good herb/seed drops",
                    "Decent profit",
                    "Agility shortcuts speed up access",
                ],
                "cons": [
                    "Single combat",
                    "Requires specific weapons (leaf-bladed or broad)",
                    "Only one location",
                ],
                "best_for": "Profit-focused slayer with herb collection",
            }
        ],
        "alternatives": [],
        "strategy": "Use leaf-bladed battleaxe for best melee DPS, or broad bolts with rune crossbow for ranged. Magic Dart is viable but slower. Must use leaf-bladed weapons, broad arrows/bolts, or Magic Dart - all other damage types deal 0 damage. Collect all herbs and seeds for profit. Use Protect from Melee to avoid all damage.",
    },
    "Scabarites": {
        "weakness": ["Keris", "Keris partisan"],
        "items_needed": ["Water source (for desert heat)", "Keris or Keris partisan recommended"],
        "attack_style": "Melee (Keris/Keris partisan)",
        "xp_rate": 18000,
        "profit_rate": 50000,
        "recommendation": "SKIP",
        "reason": "Low XP, low profit, annoying task. Only do if you need slayer points quickly.",
        "locations": [
            {
                "name": "Uzer Mastaba",
                "requirements": [
                    "Contact! quest (partial completion)",
                    "The Curse of Arrav quest (partial)",
                ],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Fastest and safest spot. Small scarabs have only 40 HP and low Defence. No drops but very fast kills.",
                "pros": ["Fastest completion", "Safest location", "Low HP enemies", "Easy to kill"],
                "cons": ["No drops", "Requires quest completion", "Single combat"],
                "best_for": "Fast task completion for slayer points",
            },
            {
                "name": "Sophanem Dungeon",
                "requirements": ["Contact! quest (most of it)", "Icthlarin's Little Helper quest"],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Safest option for lower-level players. Access via magic carpet from Pollnivneach.",
                "pros": ["Safest location", "Good for lower levels", "Easy access"],
                "cons": ["Requires quests", "Single combat", "Lower spawn rate"],
                "best_for": "Lower-level players",
            },
            {
                "name": "Ruins of Ullek (Scabaras Dungeon)",
                "requirements": ["Contact! quest"],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "2nd level has high numbers and close spawns. More dangerous than Sophanem. Bring water source for desert heat.",
                "pros": ["High spawn density", "Close together", "Good for task completion"],
                "cons": ["More dangerous", "Desert heat requires water", "Further from bank"],
                "best_for": "Efficient task completion",
            },
        ],
        "alternatives": [
            {
                "name": "Scarab swarms",
                "notes": "Count towards task. Found in same locations.",
                "recommended_for": "Task completion",
            },
            {
                "name": "Locust riders",
                "notes": "Count towards task. Found in same locations.",
                "recommended_for": "Task completion",
            },
            {
                "name": "Scarab Mages",
                "notes": "Count towards task. Found in same locations.",
                "recommended_for": "Task completion",
            },
        ],
        "strategy": "Use Keris or Keris partisan for bonus damage. Uzer Mastaba is fastest for completion. Bring water source if going to Ruins of Ullek. This is generally a skip task unless you need points quickly.",
    },
}
