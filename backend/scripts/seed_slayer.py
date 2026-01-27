"""Seed script for Slayer data."""
from sqlmodel import Session, SQLModel
from backend.database import engine
from backend.models import Monster, SlayerTask, SlayerMaster

def seed_slayer_data():
    # Ensure database tables are created before seeding
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        print("Seeding Slayer Monsters & Tasks...")
        
        # 1. Define Monsters
        monsters = [
            Monster(id=415, name="Abyssal demon", combat_level=124, hitpoints=150, slayer_xp=150, slayer_category="Abyssal demons", is_demon=True),
            Monster(id=11, name="Aberrant spectre", combat_level=96, hitpoints=90, slayer_xp=90, slayer_category="Aberrant spectres"),
            Monster(id=498, name="Smoke devil", combat_level=160, hitpoints=185, slayer_xp=185, slayer_category="Smoke devils"),
            Monster(id=122, name="Gargoyle", combat_level=111, hitpoints=105, slayer_xp=105, slayer_category="Gargoyles"),
            Monster(id=16, name="Nechryael", combat_level=115, hitpoints=105, slayer_xp=105, slayer_category="Nechryaels", is_demon=True),
            Monster(id=120, name="Bloodveld", combat_level=76, hitpoints=120, slayer_xp=120, slayer_category="Bloodvelds"),
            Monster(id=54, name="Dagannoth", combat_level=90, hitpoints=70, slayer_xp=70, slayer_category="Dagannoth"),
            Monster(id=10, name="Kalphite", combat_level=28, hitpoints=40, slayer_xp=40, slayer_category="Kalphite", is_kalphite=True),
            Monster(id=4, name="Hellhound", combat_level=122, hitpoints=116, slayer_xp=116, slayer_category="Hellhounds", is_demon=True),
            Monster(id=9, name="Dust devil", combat_level=93, hitpoints=105, slayer_xp=105, slayer_category="Dust devils"),
            Monster(id=14, name="Wyrm", combat_level=62, hitpoints=100, slayer_xp=133.2, slayer_category="Wyrms", is_dragon=True),
            Monster(id=15, name="Drake", combat_level=84, hitpoints=250, slayer_xp=316.8, slayer_category="Drakes", is_dragon=True),
            Monster(id=24, name="Hydra", combat_level=194, hitpoints=300, slayer_xp=660, slayer_category="Hydras", is_dragon=True),
            Monster(id=31, name="Kraken", combat_level=291, hitpoints=255, slayer_xp=255, slayer_category="Kraken"),
            # Additional monsters
            Monster(id=19, name="Black demon", combat_level=172, hitpoints=178, slayer_xp=178, slayer_category="Black demons", is_demon=True),
            Monster(id=20, name="Greater demon", combat_level=92, hitpoints=87, slayer_xp=87, slayer_category="Greater demons", is_demon=True),
            Monster(id=21, name="Blue dragon", combat_level=111, hitpoints=107, slayer_xp=107, slayer_category="Blue dragons", is_dragon=True),
            Monster(id=22, name="Steel dragon", combat_level=246, hitpoints=180, slayer_xp=180, slayer_category="Steel dragons", is_dragon=True),
            Monster(id=23, name="Iron dragon", combat_level=189, hitpoints=150, slayer_xp=150, slayer_category="Iron dragons", is_dragon=True),
            Monster(id=25, name="Dark beast", combat_level=182, hitpoints=140, slayer_xp=140, slayer_category="Dark beasts"),
            Monster(id=26, name="Suqah", combat_level=111, hitpoints=84, slayer_xp=84, slayer_category="Suqah"),
            Monster(id=27, name="TzHaar", combat_level=103, hitpoints=100, slayer_xp=100, slayer_category="TzHaar"),
            Monster(id=28, name="Spiritual mage", combat_level=83, hitpoints=75, slayer_xp=75, slayer_category="Spiritual Creatures"),
            Monster(id=29, name="Spiritual ranger", combat_level=63, hitpoints=60, slayer_xp=60, slayer_category="Spiritual Creatures"),
            Monster(id=30, name="Spiritual warrior", combat_level=68, hitpoints=65, slayer_xp=65, slayer_category="Spiritual Creatures"),
            Monster(id=32, name="Cave kraken", combat_level=127, hitpoints=90, slayer_xp=90, slayer_category="Cave kraken"),
            Monster(id=33, name="Fire giant", combat_level=86, hitpoints=111, slayer_xp=111, slayer_category="Fire giants"),
            Monster(id=34, name="Mithril dragon", combat_level=304, hitpoints=255, slayer_xp=255, slayer_category="Mithril dragons", is_dragon=True),
            Monster(id=35, name="Adamant dragon", combat_level=338, hitpoints=240, slayer_xp=240, slayer_category="Adamant dragons", is_dragon=True),
            Monster(id=36, name="Rune dragon", combat_level=380, hitpoints=255, slayer_xp=255, slayer_category="Rune dragons", is_dragon=True),
        ]
        
        for m in monsters:
            existing = session.get(Monster, m.id)
            if not existing:
                session.add(m)
        session.commit()
        
        # 2. Define Tasks (Duradel)
        duradel_tasks = [
            ("Abyssal demons", 120, 185, 12, True),
            ("Aberrant spectres", 135, 175, 8, True),
            ("Smoke devils", 135, 185, 9, True),
            ("Gargoyles", 130, 200, 9, True),
            ("Nechryaels", 130, 200, 9, True),
            ("Bloodvelds", 130, 200, 8, True),
            ("Dagannoth", 130, 200, 9, True),
            ("Kalphite", 130, 200, 9, True),
            ("Hellhounds", 130, 200, 10, True),
            ("Dust devils", 120, 170, 6, True),
            ("Wyrms", 125, 160, 8, True),
            ("Drakes", 80, 145, 8, True),
            ("Hydras", 135, 160, 10, True),
            ("Kraken", 100, 120, 9, True),
        ]
        
        for cat, min_q, max_q, weight, skip in duradel_tasks:
            # Find monster by category
            # In a real app we'd map this better, but for MVP we match category string
            monster = next((m for m in monsters if m.slayer_category == cat), None)
            if monster:
                # Check if task already exists
                from sqlmodel import select
                existing_task = session.exec(
                    select(SlayerTask).where(
                        SlayerTask.master == SlayerMaster.DURADEL,
                        SlayerTask.monster_id == monster.id
                    )
                ).first()
                
                if not existing_task:
                    task = SlayerTask(
                        master=SlayerMaster.DURADEL,
                        monster_id=monster.id,
                        category=cat,
                        quantity_min=min_q,
                        quantity_max=max_q,
                        weight=weight,
                        is_skippable=skip,
                        is_blockable=True
                    )
                    session.add(task)
                    print(f"  Added task: {cat}")
                else:
                    print(f"  Task already exists: {cat}")
        
        # 3. Define Tasks (Nieve) - Nieve assigns different tasks than Duradel
        nieve_tasks = [
            ("Abyssal demons", 120, 185, 12, True),
            ("Aberrant spectres", 135, 175, 8, True),
            ("Gargoyles", 130, 200, 9, True),
            ("Nechryaels", 130, 200, 9, True),
            ("Bloodvelds", 130, 200, 8, True),
            ("Dagannoth", 130, 200, 9, True),
            ("Kalphite", 130, 200, 9, True),
            ("Hellhounds", 130, 200, 10, True),
            ("Dust devils", 120, 170, 6, True),
            ("Black demons", 120, 200, 9, True),
            ("Greater demons", 120, 200, 8, True),
            ("Blue dragons", 100, 150, 7, True),
            ("Fire giants", 120, 200, 8, True),
            ("Dark beasts", 100, 200, 9, True),
            ("Suqah", 100, 200, 8, True),
            ("TzHaar", 100, 200, 6, True),
            ("Spiritual Creatures", 100, 200, 7, True),
            ("Cave kraken", 100, 200, 8, True),
            ("Steel dragons", 30, 50, 6, True),
            ("Iron dragons", 30, 50, 6, True),
        ]
        
        for cat, min_q, max_q, weight, skip in nieve_tasks:
            monster = next((m for m in monsters if m.slayer_category == cat), None)
            if monster:
                from sqlmodel import select
                existing_task = session.exec(
                    select(SlayerTask).where(
                        SlayerTask.master == SlayerMaster.NIEVE,
                        SlayerTask.monster_id == monster.id
                    )
                ).first()
                
                if not existing_task:
                    task = SlayerTask(
                        master=SlayerMaster.NIEVE,
                        monster_id=monster.id,
                        category=cat,
                        quantity_min=min_q,
                        quantity_max=max_q,
                        weight=weight,
                        is_skippable=skip,
                        is_blockable=True
                    )
                    session.add(task)
                    print(f"  Added Nieve task: {cat}")
                else:
                    print(f"  Nieve task already exists: {cat}")
        
        session.commit()
        print("✅ Slayer data seeded!")

if __name__ == "__main__":
    seed_slayer_data()
