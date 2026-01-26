"""Check if slayer data exists in the database."""
from sqlmodel import Session, select, func
from backend.database import engine
from backend.models import SlayerTask, Monster, SlayerMaster

def check_slayer_data():
    """Check if slayer data exists."""
    with Session(engine) as session:
        monster_count = session.exec(select(func.count(Monster.id))).one()
        task_count = session.exec(select(func.count(SlayerTask.id))).one()
        
        print(f"\n📊 Slayer Data Status:")
        print(f"  Monsters: {monster_count}")
        print(f"  Tasks: {task_count}")
        
        if task_count > 0:
            # Show tasks by master
            for master in SlayerMaster:
                master_tasks = session.exec(
                    select(func.count(SlayerTask.id)).where(SlayerTask.master == master)
                ).one()
                if master_tasks > 0:
                    print(f"  {master.value}: {master_tasks} tasks")
        
        if monster_count == 0 or task_count == 0:
            print("\n⚠️  Slayer data is missing!")
            print("   Run: python -m backend.scripts.seed_slayer")
            return False
        else:
            print("\n✅ Slayer data exists!")
            return True

if __name__ == "__main__":
    check_slayer_data()
