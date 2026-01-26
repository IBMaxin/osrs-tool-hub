"""Static data for Slayer tasks advice."""

SLAYER_TASK_DATA = {
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
    "Dust Devils": {
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
    "Blue Dragons": {
        "weakness": ["Stab", "Ranged", "Dragonbane"],
        "items_needed": ["Anti-dragon shield"],
        "attack_style": "Melee (Stab) or Ranged",
        "xp_rate": 15000,
        "profit_rate": 350000,
        "recommendation": "SKIP",
        "reason": "Slow task unless killing Vorkath. Good money for lower levels but inefficient.",
        "locations": ["Taverley Dungeon", "Myths' Guild"]
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
    "Black Demons": {
        "weakness": ["Demonbane"],
        "items_needed": [],
        "attack_style": "Melee (Cannon) or Ranged",
        "xp_rate": 20000,
        "profit_rate": 0,
        "recommendation": "BLOCK",
        "reason": "High weighting, high HP, low drops. Block unless doing Demonic Gorillas.",
        "locations": ["Taverley Dungeon", "Chasm of Fire"]
    },
    "Greater Demons": {
        "weakness": ["Demonbane"],
        "items_needed": [],
        "attack_style": "Melee (Cannon)",
        "xp_rate": 25000,
        "profit_rate": 50000,
        "recommendation": "DO",
        "reason": "Decent cannon task. Can do K'ril Tsutsaroth (Zammy GWD) for boss task.",
        "locations": ["Chasm of Fire", "Stronghold Slayer Cave"]
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
    "Wyrms": {
        "weakness": ["Stab", "Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots"],
        "attack_style": "Melee (Stab) or Ranged",
        "xp_rate": 25000,
        "profit_rate": 250000,
        "recommendation": "BLOCK",
        "reason": "Slow and annoying. Drops are okay but generally considered inefficient.",
        "locations": ["Karuulm Slayer Dungeon"]
    },
    "Drakes": {
        "weakness": ["Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots", "Anti-dragon shield"],
        "attack_style": "Ranged or Melee",
        "xp_rate": 20000,
        "profit_rate": 300000,
        "recommendation": "BLOCK",
        "reason": "High defence, annoying mechanics. Block or skip.",
        "locations": ["Karuulm Slayer Dungeon"]
    },
    "Hydras": {
        "weakness": ["Dragonbane"],
        "items_needed": ["Boots of stone/Brimstone boots"],
        "attack_style": "Ranged (Tbow/BP) or Melee (Lance)",
        "xp_rate": 30000,
        "profit_rate": 2000000,
        "recommendation": "DO",
        "reason": "Alchemical Hydra is one of the best money makers in the game. Always do.",
        "locations": ["Karuulm Slayer Dungeon"]
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
    "Aberrant Spectres": {
        "weakness": [],
        "items_needed": ["Nose peg/Slayer Helmet"],
        "attack_style": "Magic or Ranged",
        "xp_rate": 25000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Good herbs/seeds drops. Decent XP.",
        "locations": ["Slayer Tower", "Stronghold Slayer Cave"]
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
    "Steel Dragons": {
        "weakness": ["Magic", "Stab", "Dragonbane"],
        "items_needed": ["Anti-dragon shield"],
        "attack_style": "Magic (Trident/Sang)",
        "xp_rate": 10000,
        "profit_rate": 150000,
        "recommendation": "SKIP",
        "reason": "Very slow, high defence. Skip unless hunting visage (inefficient).",
        "locations": ["Brimhaven Dungeon", "Catacombs of Kourend"]
    },
     "Iron Dragons": {
        "weakness": ["Magic", "Stab", "Dragonbane"],
        "items_needed": ["Anti-dragon shield"],
        "attack_style": "Magic (Trident/Sang)",
        "xp_rate": 12000,
        "profit_rate": 100000,
        "recommendation": "SKIP",
        "reason": "Very slow. Skip.",
        "locations": ["Brimhaven Dungeon", "Catacombs of Kourend"]
    },
    "Kraken": {
        "weakness": ["Magic"],
        "items_needed": [],
        "attack_style": "Magic",
        "xp_rate": 15000,
        "profit_rate": 800000,
        "recommendation": "DO",
        "reason": "Very AFK boss, good profit. Cave krakens are fast points.",
        "locations": ["Kraken Cove"]
    }
}
