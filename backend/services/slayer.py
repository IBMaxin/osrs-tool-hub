"""Slayer service logic."""
from typing import List, Optional, Dict
from sqlmodel import Session, select, func

from backend.models import Monster, SlayerTask, SlayerMaster


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
        query = select(SlayerTask, Monster).join(Monster).where(SlayerTask.master == master)
        results = self.session.exec(query).all()
        
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
        return tasks

    def suggest_action(self, task_id: int, user_stats: Dict[str, int]) -> Dict:
        """
        Suggest whether to Do, Skip, or Block a task based on stats/efficiency.
        NOTE: This is a basic implementation. Real efficiency requires comprehensive blocklists.
        """
        task = self.session.get(SlayerTask, task_id)
        if not task:
            return {"error": "Task not found"}
        
        monster = self.session.get(Monster, task.monster_id)
        
        recommendation = "DO"
        reason = "Good XP/HR or Profit"
        
        # Simple Logic Examples
        if task.weight > 8 and monster.slayer_xp < 50:
             recommendation = "BLOCK"
             reason = "High weight but low XP (inefficient)"
             
        if monster.name in ["Spiritual Ranger", "Waterfiend", "Killerwatt"]:
             recommendation = "SKIP"
             reason = "Generally considered annoying/slow"

        return {
            "task": monster.name,
            "master": task.master,
            "recommendation": recommendation,
            "reason": reason,
            "stats": {
                "hp": monster.hitpoints,
                "def": monster.defence_level,
                "xp": monster.slayer_xp
            }
        }
