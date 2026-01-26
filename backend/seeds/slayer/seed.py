"""Slayer data seeding entrypoint."""
from sqlmodel import Session, SQLModel, select

from backend.db.engine import engine
from backend.models import Monster, SlayerTask, SlayerMaster
from backend.seeds.slayer.monsters import get_monster_definitions
from backend.seeds.slayer.tasks import get_tasks_by_master


def seed_slayer_data() -> None:
    """
    Seed slayer monsters and tasks into the database.
    
    This function:
    1. Creates/updates monster definitions
    2. Creates/updates task definitions for each master
    """
    # Ensure database tables are created before seeding
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        print("Seeding Slayer Monsters & Tasks...")
        
        # 1. Seed Monsters
        monsters = get_monster_definitions()
        for m in monsters:
            existing = session.get(Monster, m.id)
            if not existing:
                session.add(m)
        session.commit()
        
        # 2. Seed Tasks by Master
        tasks_by_master = get_tasks_by_master()
        
        for master, task_defs in tasks_by_master.items():
            for cat, min_q, max_q, weight, skip in task_defs:
                # Find monster by category
                monster = next((m for m in monsters if m.slayer_category == cat), None)
                if monster:
                    # Check if task already exists
                    existing_task = session.exec(
                        select(SlayerTask).where(
                            SlayerTask.master == master,
                            SlayerTask.monster_id == monster.id
                        )
                    ).first()
                    
                    if not existing_task:
                        task = SlayerTask(
                            master=master,
                            monster_id=monster.id,
                            category=cat,
                            quantity_min=min_q,
                            quantity_max=max_q,
                            weight=weight,
                            is_skippable=skip,
                            is_blockable=True
                        )
                        session.add(task)
                        master_name = master.value if hasattr(master, 'value') else str(master)
                        print(f"  Added {master_name} task: {cat}")
                    else:
                        master_name = master.value if hasattr(master, 'value') else str(master)
                        print(f"  {master_name} task already exists: {cat}")
        
        session.commit()
        print("✅ Slayer data seeded!")


if __name__ == "__main__":
    seed_slayer_data()
