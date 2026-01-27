"""Common slayer task data - frequently assigned tasks."""

COMMON_TASK_DATA = {
    "Abyssal demons": {
        "weakness": ["Slash", "Demonbane"],
        "items_needed": [],
        "attack_style": "Melee (Slash) or Magic (Burst/Barrage)",
        "xp_rate": 35000,
        "profit_rate": 400000,
        "recommendation": "DO",
        "reason": "Great combat XP and chance for Abyssal Whip. Barraging in Catacombs is very high XP.",
        "locations": ["Catacombs of Kourend", "Slayer Tower"]
    },
    "Gargoyles": {
        "weakness": ["Crush"],
        "items_needed": ["Rock hammer"],
        "attack_style": "Melee (Crush)",
        "xp_rate": 22000,
        "profit_rate": 600000,
        "recommendation": "DO",
        "reason": "Excellent consistent profit (alchables). Somewhat slow XP but very AFK.",
        "locations": ["Slayer Tower"]
    },
    "Nechryael": {
        "weakness": ["Demonbane", "Crush"],
        "items_needed": [],
        "attack_style": "Magic (Burst/Barrage)",
        "xp_rate": 55000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Incredible XP/hr when bursting in Catacombs. Break-even or profitable with drops.",
        "locations": ["Catacombs of Kourend", "Slayer Tower"]
    },
    "Bloodveld": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee (Cannon) or Magic (Burst/Barrage)",
        "xp_rate": 45000,
        "profit_rate": 100000,
        "recommendation": "DO",
        "reason": "Great XP, especially mutated variants in Catacombs. Low profit but fast.",
        "locations": ["Catacombs of Kourend", "Stronghold Slayer Cave"]
    },
    "Dust devils": {
        "weakness": [],
        "items_needed": ["Facemask/Slayer Helmet"],
        "attack_style": "Magic (Burst/Barrage)",
        "xp_rate": 65000,
        "profit_rate": 200000,
        "recommendation": "DO",
        "reason": "One of the best XP tasks in the game when bursting. Very profitable too.",
        "locations": ["Catacombs of Kourend", "Smoke Dungeon"]
    },
    "Hellhounds": {
        "weakness": ["Slash"],
        "items_needed": [],
        "attack_style": "Melee",
        "xp_rate": 25000,
        "profit_rate": 0,
        "recommendation": "SKIP",
        "reason": "Low XP and no drops unless doing Cerberus (Boss). Skip if not bossing.",
        "locations": ["Stronghold Slayer Cave", "Catacombs of Kourend"]
    },
    "Dagannoth": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee (Cannon) or Magic (Burst)",
        "xp_rate": 60000,
        "profit_rate": 50000,
        "recommendation": "DO",
        "reason": "Extremely fast XP with a cannon in Lighthouse. Can also do Dagannoth Kings for profit.",
        "locations": ["Lighthouse", "Catacombs of Kourend"]
    },
    "Kalphite": {
        "weakness": ["Keris"],
        "items_needed": [],
        "attack_style": "Melee (Cannon)",
        "xp_rate": 50000,
        "profit_rate": 20000,
        "recommendation": "DO",
        "reason": "Very fast points/XP with cannon (Workers). Can do Kalphite Queen for boss task.",
        "locations": ["Kalphite Cave"]
    },
    "Aberrant spectres": {
        "weakness": [],
        "items_needed": ["Nose peg/Slayer Helmet"],
        "attack_style": "Magic or Ranged",
        "xp_rate": 25000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Good herbs/seeds drops. Decent XP.",
        "locations": ["Slayer Tower", "Stronghold Slayer Cave"]
    },
}
