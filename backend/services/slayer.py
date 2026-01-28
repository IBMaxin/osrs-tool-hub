"""Slayer service logic."""

from typing import List, Dict
from sqlmodel import Session, select

from backend.models import Monster, SlayerTask, SlayerMaster
from backend.services.slayer_data import SLAYER_TASK_DATA


class SlayerService:
    def __init__(self, session: Session):
        self.session = session

    def get_masters(self) -> List[str]:
        """Get all slayer masters."""
        return [master.value for master in SlayerMaster]

    def get_tasks(self, master: SlayerMaster) -> List[Dict]:
        """Get all tasks assignable by a specific master.

        Args:
            master: The slayer master to get tasks for

        Returns:
            List of task dictionaries with monster and task information
        """
        query = select(SlayerTask, Monster).join(Monster).where(SlayerTask.master == master)
        results = self.session.exec(query).all()

        tasks = []
        for task, monster in results:
            tasks.append(
                {
                    "task_id": task.id,
                    "monster_name": monster.name,
                    "monster_id": monster.id,
                    "category": task.category,
                    "amount": f"{task.quantity_min}-{task.quantity_max}",
                    "weight": task.weight,
                    "combat_level": monster.combat_level,
                    "slayer_xp": monster.slayer_xp,
                    "is_skippable": task.is_skippable,
                    "is_blockable": task.is_blockable,
                }
            )

        # Sort by weight descending (highest probability first)
        tasks.sort(key=lambda x: x["weight"], reverse=True)
        return tasks

    def get_task_locations(self, task_id: int) -> Dict:
        """Get detailed location information for a slayer task.

        Retrieves location data including:
        - Available locations with requirements
        - Pros/cons for each location
        - Combat type (multi/single)
        - Cannon and safespot availability
        - Alternative monsters
        - Strategy recommendations

        Args:
            task_id: The slayer task ID

        Returns:
            Dictionary with location information and strategy, or error if task not found

        Example:
            {
                "task_id": 123,
                "monster_name": "Abyssal demon",
                "category": "Abyssal demons",
                "locations": [
                    {
                        "name": "Slayer Tower",
                        "requirements": [],
                        "multi_combat": True,
                        "cannon": False,
                        "safespot": False,
                        "notes": "Most popular location...",
                        "pros": ["Close to bank", ...],
                        "cons": ["Can be crowded"],
                        "best_for": "Melee training"
                    }
                ],
                "alternatives": [],
                "strategy": "Use Arclight for +70% damage...",
                "weakness": ["Slash", "Demonbane"],
                "items_needed": []
            }
        """
        # Get task from database
        task = self.session.get(SlayerTask, task_id)
        if not task:
            return {"error": "Task not found"}

        # Get monster information
        monster = self.session.get(Monster, task.monster_id)
        if not monster:
            return {"error": "Monster not found"}

        # Try to find task data by category (preferred) or monster name (fallback)
        task_data = SLAYER_TASK_DATA.get(task.category) or SLAYER_TASK_DATA.get(monster.name) or {}

        # Extract location data with safe defaults
        locations = task_data.get("locations", [])

        # Handle legacy format (list of strings) vs new format (list of dicts)
        formatted_locations = []
        for loc in locations:
            if isinstance(loc, str):
                # Legacy format - convert to minimal dict
                formatted_locations.append(
                    {
                        "name": loc,
                        "requirements": [],
                        "multi_combat": None,
                        "cannon": None,
                        "safespot": None,
                        "notes": "",
                        "pros": [],
                        "cons": [],
                        "best_for": "",
                    }
                )
            elif isinstance(loc, dict):
                # New format - use as-is
                formatted_locations.append(loc)

        return {
            "task_id": task_id,
            "monster_name": monster.name,
            "monster_id": monster.id,
            "category": task.category,
            "master": task.master.value,
            "locations": formatted_locations,
            "alternatives": task_data.get("alternatives", []),
            "strategy": task_data.get("strategy", ""),
            "weakness": task_data.get("weakness", []),
            "items_needed": task_data.get("items_needed", []),
            "attack_style": task_data.get("attack_style", ""),
            "has_detailed_data": (
                len(formatted_locations) > 0 and isinstance(locations[0], dict)
                if locations
                else False
            ),
        }

    def suggest_action(self, task_id: int, user_stats: Dict[str, int]) -> Dict:
        """Suggest whether to Do, Skip, or Block a task based on stats/efficiency.

        Uses rich metadata from SLAYER_TASK_DATA if available.

        Args:
            task_id: The slayer task ID
            user_stats: Dictionary with player stats (slayer, combat)

        Returns:
            Dictionary with recommendation, reason, and task metadata
        """
        task = self.session.get(SlayerTask, task_id)
        if not task:
            return {"error": "Task not found"}

        monster = self.session.get(Monster, task.monster_id)

        # Defaults
        recommendation = "DO"
        reason = "Good XP/HR or Profit"
        xp_rate = 0
        profit_rate = 0
        attack_style = "Generic Melee/Ranged"
        items_needed = []
        weakness = []

        # Try to find data by Category first (usually matches wiki), then Monster Name
        task_data = SLAYER_TASK_DATA.get(task.category) or SLAYER_TASK_DATA.get(monster.name)

        if task_data:
            recommendation = task_data.get("recommendation", recommendation)
            reason = task_data.get("reason", reason)
            xp_rate = task_data.get("xp_rate", 0)
            profit_rate = task_data.get("profit_rate", 0)
            attack_style = task_data.get("attack_style", attack_style)
            items_needed = task_data.get("items_needed", [])
            weakness = task_data.get("weakness", [])
        else:
            # Fallback Logic
            if task.weight > 8 and monster.slayer_xp < 50:
                recommendation = "BLOCK"
                reason = "High weight but low XP (inefficient)"
            elif monster.name in ["Spiritual Ranger", "Waterfiend", "Killerwatt", "Cave Kraken"]:
                recommendation = "SKIP"
                reason = "Generally considered annoying/slow"

        return {
            "task": monster.name,
            "category": task.category,
            "master": task.master,
            "recommendation": recommendation,
            "reason": reason,
            "stats": {
                "hp": monster.hitpoints,
                "def": monster.defence_level,
                "xp": monster.slayer_xp,
            },
            "meta": {
                "xp_rate": xp_rate,
                "profit_rate": profit_rate,
                "attack_style": attack_style,
                "items_needed": items_needed,
                "weakness": weakness,
            },
        }
