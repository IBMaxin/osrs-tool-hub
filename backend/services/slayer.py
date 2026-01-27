"""Slayer service logic."""
from typing import List, Optional, Dict
from sqlmodel import Session, select, func

from backend.models import Monster, SlayerTask, SlayerMaster
from backend.services.slayer_data import SLAYER_TASK_DATA


class SlayerService:
    def __init__(self, session: Session):
        self.session = session

    def get_masters(self) -> List[str]:
        """Get all slayer masters."""
        return [master.value for master in SlayerMaster]

    def get_tasks(self, master: SlayerMaster) -> List[Dict]:
        """
        Get all tasks assignable by a specific master.
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"SlayerService.get_tasks called with master: {master} (type: {type(master)}, value: {master.value if hasattr(master, 'value') else master})")
        
        query = select(SlayerTask, Monster).join(Monster).where(SlayerTask.master == master)
        results = self.session.exec(query).all()
        logger.info(f"Query returned {len(results)} results")
        
        tasks = []
        for task, monster in results:
            tasks.append({
                "task_id": task.id,
                "monster_name": monster.name,
                "monster_id": monster.id,
                "category": task.category,
                "amount": f"{task.quantity_min}-{task.quantity_max}",
                "weight": task.weight,
                "combat_level": monster.combat_level,
                "slayer_xp": monster.slayer_xp,
                "is_skippable": task.is_skippable,
                "is_blockable": task.is_blockable
            })
        
        # Sort by weight descending (highest probability first)
        tasks.sort(key=lambda x: x["weight"], reverse=True)
        logger.info(f"Returning {len(tasks)} tasks")
        return tasks

    def suggest_action(self, task_id: int, user_stats: Dict[str, int]) -> Dict:
        """
        Suggest whether to Do, Skip, or Block a task based on stats/efficiency.
        Uses rich metadata from SLAYER_TASK_DATA if available.
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
                "xp": monster.slayer_xp
            },
            "meta": {
                "xp_rate": xp_rate,
                "profit_rate": profit_rate,
                "attack_style": attack_style,
                "items_needed": items_needed,
                "weakness": weakness
            }
        }
