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
        "locations": [
            {
                "name": "Slayer Tower",
                "requirements": [],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Most popular location. Top floor has many spawns.",
                "pros": ["Close to Canifis bank", "Many spawn points", "Easy access"],
                "cons": ["Can be crowded on peak hours"],
                "best_for": "Melee training or casual slayer"
            },
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Restores prayer via bone drops. Superior encounters possible. Drops ancient shards and totem pieces.",
                "pros": ["Prayer restoration", "Totem pieces", "Ancient shards", "Superior encounters", "Excellent for bursting/barraging"],
                "cons": ["Requires Arceuus favour", "Further from bank", "Need to navigate dungeon"],
                "best_for": "Bursting/barraging for maximum XP and superior encounters"
            }
        ],
        "alternatives": [],
        "strategy": "Use Arclight for +70% damage bonus against demons. For maximum XP, barrage in Catacombs. For afk melee, use Slayer Tower with guthan's or blood barrage for healing."
    },
    "Dust devils": {
        "weakness": [],
        "items_needed": ["Facemask/Slayer Helmet"],
        "attack_style": "Magic (Burst/Barrage)",
        "xp_rate": 65000,
        "profit_rate": 200000,
        "recommendation": "DO",
        "reason": "One of the best XP tasks in the game when bursting. Very profitable too.",
        "locations": [
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Best location for bursting. Stack dust devils in corner for maximum efficiency.",
                "pros": ["Prayer restoration", "Totem pieces", "Ancient shards", "Superior encounters", "Perfect for bursting"],
                "cons": ["Requires favour", "Need to navigate to location"],
                "best_for": "Bursting for maximum XP/hr"
            },
            {
                "name": "Smoke Dungeon",
                "requirements": ["Desert Treasure quest (for Pollnivneach entrance)"],
                "multi_combat": False,
                "cannon": True,
                "safespot": True,
                "notes": "Single-way combat. Can use cannon but not ideal for bursting.",
                "pros": ["Cannon allowed", "Safespot available"],
                "cons": ["Single combat", "Not ideal for bursting", "Requires desert treasure"],
                "best_for": "Solo cannon slayer (not recommended)"
            }
        ],
        "alternatives": [],
        "strategy": "Always burst in Catacombs. Stack 9+ dust devils in corner, use Ice Barrage. Bring Slayer Helmet (i) for magic bonus. Prayer gear recommended."
    },
    "Nechryael": {
        "weakness": ["Demonbane", "Crush"],
        "items_needed": [],
        "attack_style": "Magic (Burst/Barrage)",
        "xp_rate": 55000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Incredible XP/hr when bursting in Catacombs. Break-even or profitable with drops.",
        "locations": [
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Best location. Death spawns stack nicely for bursting. Greater Nechryael possible.",
                "pros": ["Prayer restoration", "Totem pieces", "Superior encounters (Greater Nechryael)", "Death spawns for extra XP"],
                "cons": ["Requires favour", "Need to manage death spawns"],
                "best_for": "Bursting for maximum XP/hr"
            },
            {
                "name": "Slayer Tower",
                "requirements": [],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Alternative location but less efficient than Catacombs.",
                "pros": ["Easy access", "No requirements"],
                "cons": ["No prayer restoration", "Less efficient spawns", "No superior encounters"],
                "best_for": "If Arceuus favour not obtained"
            },
            {
                "name": "Iorwerth Dungeon",
                "requirements": ["Song of the Elves quest"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Good spawn density. Requires high-level quest completion.",
                "pros": ["Good spawn density", "Crystal shards from elves nearby"],
                "cons": ["High quest requirement", "Further from bank"],
                "best_for": "Post-quest alternative to Catacombs"
            }
        ],
        "alternatives": [],
        "strategy": "Burst in Catacombs for best XP. Let death spawns stack, then barrage them all. Use Arclight for melee if low on runes. Slayer Helmet (i) highly recommended."
    },
    "Gargoyles": {
        "weakness": ["Crush"],
        "items_needed": ["Rock hammer"],
        "attack_style": "Melee (Crush)",
        "xp_rate": 22000,
        "profit_rate": 600000,
        "recommendation": "DO",
        "reason": "Excellent consistent profit (alchables). Somewhat slow XP but very AFK.",
        "locations": [
            {
                "name": "Slayer Tower",
                "requirements": [],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Only location. Top floor near Abyssal demons. Very AFK with guthan's.",
                "pros": ["Only one spot", "Very AFK", "Consistent profit", "Close to bank"],
                "cons": ["Single combat", "Can be crowded"],
                "best_for": "AFK profit making"
            }
        ],
        "alternatives": [
            {
                "name": "Grotesque Guardians",
                "notes": "Superior boss variant. Requires 75 Slayer. Much higher profit but not AFK.",
                "recommended_for": "Experienced players with good gear"
            }
        ],
        "strategy": "Use Guthan's for AFK healing, or blood fury. Wear full Guthans and stay for entire task. Remember to bring rock hammer to finish them."
    },
    "Bloodveld": {
        "weakness": [],
        "items_needed": [],
        "attack_style": "Melee (Cannon) or Magic (Burst/Barrage)",
        "xp_rate": 45000,
        "profit_rate": 100000,
        "recommendation": "DO",
        "reason": "Great XP, especially mutated variants in Catacombs. Low profit but fast.",
        "locations": [
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Mutated Bloodvelds. Best for bursting. Prayer restoration from bones.",
                "pros": ["Prayer restoration", "Mutated variants", "Superior encounters", "Totem pieces"],
                "cons": ["Requires favour"],
                "best_for": "Bursting for maximum XP"
            },
            {
                "name": "Stronghold Slayer Cave",
                "requirements": [],
                "multi_combat": True,
                "cannon": True,
                "safespot": False,
                "notes": "Good for cannon. Close to bank via Ring of Slaying.",
                "pros": ["Cannon allowed", "Easy access with Ring of Slaying", "No requirements"],
                "cons": ["No prayer restoration", "Regular bloodvelds only"],
                "best_for": "Cannon slayer training"
            },
            {
                "name": "Meiyerditch Laboratories",
                "requirements": ["Sins of the Father quest"],
                "multi_combat": False,
                "cannon": False,
                "safespot": False,
                "notes": "Vyrewatch Sentinels count as bloodvelds. Very high profit.",
                "pros": ["Excellent profit", "Blood shards", "Counts for bloodveld task"],
                "cons": ["High quest requirement", "Single combat", "Slower than bursting"],
                "best_for": "Profit-focused players post-quest"
            }
        ],
        "alternatives": [],
        "strategy": "Burst mutated bloodvelds in Catacombs for XP. Use cannon in Stronghold for casual slayer. Do Vyrewatch Sentinels if you need GP."
    },
    "Hellhounds": {
        "weakness": ["Slash"],
        "items_needed": [],
        "attack_style": "Melee",
        "xp_rate": 25000,
        "profit_rate": 0,
        "recommendation": "SKIP",
        "reason": "Low XP and no drops unless doing Cerberus (Boss). Skip if not bossing.",
        "locations": [
            {
                "name": "Stronghold Slayer Cave",
                "requirements": [],
                "multi_combat": True,
                "cannon": True,
                "safespot": False,
                "notes": "Best spot for cannon. Still not worth doing unless bossing.",
                "pros": ["Cannon allowed", "Easy access"],
                "cons": ["Zero drops", "Waste of cannonballs"],
                "best_for": "Skip this task"
            },
            {
                "name": "Catacombs of Kourend",
                "requirements": ["20% Arceuus favour"],
                "multi_combat": True,
                "cannon": False,
                "safespot": False,
                "notes": "Prayer restoration but still not worth it.",
                "pros": ["Prayer restoration", "Totem pieces"],
                "cons": ["No drops", "Slow"],
                "best_for": "Skip this task"
            }
        ],
        "alternatives": [
            {
                "name": "Cerberus",
                "notes": "Boss variant requires 91 Slayer. Excellent drops (Primordial/Pegasian/Eternal crystals).",
                "recommended_for": "High-level players only. Otherwise skip task."
            }
        ],
        "strategy": "Skip unless you can kill Cerberus (91 Slayer). If forced to do regular hellhounds, cannon in Stronghold for fastest completion."
    },
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
                "best_for": "Fast XP with cannon"
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
                "best_for": "If out of cannonballs"
            }
        ],
        "alternatives": [
            {
                "name": "Dagannoth Kings",
                "notes": "Boss trio. Excellent profit (Dragon axes, Berserker ring, Archers ring, Seers ring). Requires tribrid gear.",
                "recommended_for": "Experienced players with tribrid setup"
            }
        ],
        "strategy": "Cannon in Lighthouse for maximum XP. Safespot behind rocks. Bring many cannonballs. Do DKs if you have good gear and want profit over XP."
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
                "best_for": "Fast slayer points"
            }
        ],
        "alternatives": [
            {
                "name": "Kalphite Queen",
                "notes": "Boss variant. Dragon chainbody drop. Requires gear switches (ranged + melee).",
                "recommended_for": "Players wanting boss slayer"
            }
        ],
        "strategy": "Cannon Kalphite Workers for fastest task completion. Use Keris partisan if you have it for bonus damage. Safespot to minimize damage taken."
    },
    "Aberrant spectres": {
        "weakness": [],
        "items_needed": ["Nose peg/Slayer Helmet"],
        "attack_style": "Magic or Ranged",
        "xp_rate": 25000,
        "profit_rate": 300000,
        "recommendation": "DO",
        "reason": "Good herbs/seeds drops. Decent XP.",
        "locations": [
            {
                "name": "Slayer Tower",
                "requirements": [],
                "multi_combat": False,
                "cannon": False,
                "safespot": True,
                "notes": "Most common location. Good herb drops. Safespot available.",
                "pros": ["Good herb/seed drops", "Safespot available", "Easy access"],
                "cons": ["Single combat", "Can be crowded"],
                "best_for": "Consistent profit from herbs"
            },
            {
                "name": "Stronghold Slayer Cave",
                "requirements": [],
                "multi_combat": False,
                "cannon": False,
                "safespot": True,
                "notes": "Alternative location with Ring of Slaying teleport.",
                "pros": ["Easy access with ring", "Less crowded"],
                "cons": ["Single combat", "Same as Slayer Tower"],
                "best_for": "If Slayer Tower is crowded"
            }
        ],
        "alternatives": [
            {
                "name": "Deviant spectres",
                "notes": "Superior variant in Catacombs. Better drops.",
                "recommended_for": "Superior slayer encounters"
            }
        ],
        "strategy": "Use magic or ranged. Safespot to avoid melee damage. Collect all herb drops for profit. Must wear nose peg or slayer helmet."
    },
}
