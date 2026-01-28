"""Slayer Tower slayer task data."""

SLAYER_TOWER_TASK_DATA = {
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
                "best_for": "AFK profit making",
            }
        ],
        "alternatives": [
            {
                "name": "Grotesque Guardians",
                "notes": "Superior boss variant. Requires 75 Slayer. Much higher profit but not AFK.",
                "recommended_for": "Experienced players with good gear",
            }
        ],
        "strategy": "Use Guthan's for AFK healing, or blood fury. Wear full Guthans and stay for entire task. Remember to bring rock hammer to finish them.",
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
                "best_for": "Consistent profit from herbs",
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
                "best_for": "If Slayer Tower is crowded",
            },
        ],
        "alternatives": [
            {
                "name": "Deviant spectres",
                "notes": "Superior variant in Catacombs. Better drops.",
                "recommended_for": "Superior slayer encounters",
            }
        ],
        "strategy": "Use magic or ranged. Safespot to avoid melee damage. Collect all herb drops for profit. Must wear nose peg or slayer helmet.",
    },
}
