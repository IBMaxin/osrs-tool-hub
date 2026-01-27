from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from backend.main import app
from backend.models import Monster, SlayerTask, SlayerMaster
from backend.database import get_session
import pytest

# Use StaticPool to share the same in-memory database across threads/connections
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def create_test_db():
    SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

# Create client without global override - we'll set it per-test
client = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    # Apply dependency override for this test only
    app.dependency_overrides[get_session] = get_test_session
    try:
        # Create tables before each test
        create_test_db()
        with Session(engine) as session:
            yield session
        # Clean up after each test
        SQLModel.metadata.drop_all(engine)
    finally:
        # Always clear dependency override after test
        app.dependency_overrides.clear()

def test_get_slayer_masters(session: Session):
    response = client.get("/api/v1/slayer/masters")
    assert response.status_code == 200
    assert "Konar" in response.json()
    assert "Duradel" in response.json()

def test_get_tasks_for_master(session: Session):
    # Seed Data
    monster = Monster(id=1, name="Abyssal Demon", combat_level=124, hitpoints=150, slayer_xp=150)
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=monster.id,
        category="Abyssal demons",
        quantity_min=120,
        quantity_max=185,
        weight=12,
        is_skippable=True
    )
    session.add(task)
    session.commit()

    response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
    assert response.status_code == 200
    data = response.json()
    # Find our specific task in the results (there may be other tasks from fixtures)
    abyssal_task = next((t for t in data if t["monster_name"] == "Abyssal Demon"), None)
    assert abyssal_task is not None, "Abyssal Demon task should be in results"
    assert abyssal_task["weight"] == 12

def test_suggest_action(session: Session):
    # Seed Data
    monster = Monster(id=2, name="Waterfiend", combat_level=115, hitpoints=120, slayer_xp=128)
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=monster.id,
        category="Waterfiends",
        quantity_min=130,
        quantity_max=170,
        weight=8,
        is_skippable=True
    )
    session.add(task)
    session.commit()

    response = client.get(f"/api/v1/slayer/advice/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"] == "SKIP"
    assert data["task"] == "Waterfiend"
