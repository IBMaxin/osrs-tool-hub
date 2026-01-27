"""Special slayer task data - unique monsters and bosses."""

SPECIAL_TASK_DATA = {
    "Kraken": {
        "weakness": ["Magic"],
        "items_needed": [],
        "attack_style": "Magic",
        "xp_rate": 15000,
        "profit_rate": 800000,
        "recommendation": "DO",
        "reason": "Very AFK boss, good profit. Cave krakens are fast points.",
        "locations": ["Kraken Cove"]
    },
    "Cave kraken": {
        "weakness": ["Magic"],
        "items_needed": [],
        "attack_style": "Magic",
        "xp_rate": 25000,
        "profit_rate": 200000,
        "recommendation": "DO",
        "reason": "Fast points task, decent XP. Good for slayer points farming.",
        "locations": ["Kraken Cove"]
    },
    "Fire giants": {
        "weakness": ["Crush"],
        "items_needed": [],
        "attack_style": "Melee (Cannon)",
        "xp_rate": 30000,
        "profit_rate": 100000,
        "recommendation": "DO",
        "reason": "Good cannon task for lower levels. Decent XP and some profit.",
        "locations": ["Catacombs of Kourend", "Waterfall Dungeon"]
    },
    "Dark Beasts": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee",
        "xp_rate": 15000,
        "profit_rate": 150000,
        "recommendation": "DO",
        "reason": "Very quick points task. Extend if you want AFK, otherwise just do for points.",
        "locations": ["Mourner Tunnels"]
    },
    "Dark beasts": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee",
        "xp_rate": 15000,
        "profit_rate": 150000,
        "recommendation": "DO",
        "reason": "Very quick points task. Extend if you want AFK, otherwise just do for points.",
        "locations": ["Mourner Tunnels"]
    },
    "Suqah": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee (Cannon)",
        "xp_rate": 60000,
        "profit_rate": 0,
        "recommendation": "DO",
        "reason": "One of the fastest XP tasks in the game with cannon. No loot.",
        "locations": ["Lunar Isle"]
    },
    "TzHaar": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee or Ranged",
        "xp_rate": 20000,
        "profit_rate": 0,
        "recommendation": "SKIP",
        "reason": "Skip unless choosing Jad (Fight Caves) or Zuk (Inferno) for massive XP drop.",
        "locations": ["Mor Ul Rek"]
    },
    "Spiritual Creatures": {
        "weakness": [],
        "items_needed": ["God protection"],
        "attack_style": "Ranged/Melee",
        "xp_rate": 15000,
        "profit_rate": 100000,
        "recommendation": "BLOCK",
        "reason": "Generally slow and annoying. Mages drop D boots but rare.",
        "locations": ["God Wars Dungeon"]
    },
}
