"""Shared test fixtures and configuration for E2E tests."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from typing import Generator

from backend.main import app
from backend.db.session import get_session
from backend.models import Item, PriceSnapshot, Monster, SlayerTask, SlayerMaster


# Create in-memory SQLite database for testing
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_test_session() -> Generator[Session, None, None]:
    """Test database session generator."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Create and drop test database tables for each test.

    This fixture:
    1. Overrides the app's get_session dependency to use test database
    2. Creates all tables
    3. Yields for test execution
    4. Drops all tables
    5. Clears dependency overrides
    """
    # Override dependency BEFORE creating tables
    app.dependency_overrides[get_session] = get_test_session

    # Create all tables
    SQLModel.metadata.create_all(test_engine)

    yield

    # Cleanup
    SQLModel.metadata.drop_all(test_engine)
    app.dependency_overrides.clear()
    # Note: Don't dispose test_engine here as it's module-level and reused


@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    """Provide a test database session.

    This fixture is for tests that need direct database access.
    The setup_test_db fixture (autouse=True) ensures tables exist.
    """
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def client() -> TestClient:
    """Provide a test client for API requests.

    The client will use the test database via dependency override
    set up in setup_test_db fixture.
    """
    return TestClient(app)


@pytest.fixture
def sample_items(session: Session) -> list[Item]:
    """Create sample items for testing."""
    items = [
        Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            high_price=1500000,
            low_price=1400000,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=70,
            icon_url="https://oldschool.runescape.wiki/images/Abyssal_whip_detail.png",
        ),
        Item(
            id=314,
            name="Feather",
            members=False,
            limit=13000,
            value=2,
            high_price=3,
            low_price=3,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=13000,
        ),
        Item(
            id=20997,
            name="Twisted bow",
            members=True,
            limit=8,
            value=1000000000,
            high_price=1_600_000_000,
            low_price=1_550_000_000,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=8,
        ),
        Item(
            id=11802,
            name="Saradomin godsword",
            members=True,
            limit=8,
            value=50000000,
            high_price=52_000_000,
            low_price=50_000_000,
            high_time=1700000000,
            low_time=1700000000,
            buy_limit=8,
        ),
    ]
    for item in items:
        session.add(item)
    session.commit()
    return items


@pytest.fixture
def sample_price_snapshots(session: Session, sample_items: list[Item]) -> list[PriceSnapshot]:
    """Create sample price snapshots for testing."""
    snapshots = [
        PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
            high_time=1700000000,
            low_time=1700000000,
        ),
        PriceSnapshot(
            item_id=314,
            high_price=3,
            low_price=3,
            high_volume=1000000,
            low_volume=1000000,
            high_time=1700000000,
            low_time=1700000000,
        ),
        PriceSnapshot(
            item_id=20997,
            high_price=1_600_000_000,
            low_price=1_550_000_000,
            high_volume=50,
            low_volume=50,
            high_time=1700000000,
            low_time=1700000000,
        ),
        PriceSnapshot(
            item_id=11802,
            high_price=52_000_000,
            low_price=50_000_000,
            high_volume=200,
            low_volume=150,
            high_time=1700000000,
            low_time=1700000000,
        ),
    ]
    for snapshot in snapshots:
        session.add(snapshot)
    session.commit()
    return snapshots


@pytest.fixture
def sample_monsters(session: Session) -> list[Monster]:
    """Create sample monsters for slayer testing."""
    monsters = [
        Monster(
            id=415,
            name="Abyssal demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150.0,
            defence_level=70,
            is_demon=True,
            is_slayer_monster=True,
        ),
        Monster(
            id=2005,
            name="Waterfiend",
            combat_level=115,
            hitpoints=120,
            slayer_xp=128.0,
            defence_level=65,
            is_slayer_monster=True,
        ),
        Monster(
            id=1648,
            name="Dragon",
            combat_level=83,
            hitpoints=100,
            slayer_xp=60.0,
            defence_level=60,
            is_dragon=True,
            is_slayer_monster=True,
        ),
    ]
    for monster in monsters:
        session.add(monster)
    session.commit()
    return monsters


@pytest.fixture
def sample_slayer_tasks(session: Session, sample_monsters: list[Monster]) -> list[SlayerTask]:
    """Create sample slayer tasks for testing."""
    tasks = [
        SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=415,
            category="Abyssal demons",
            quantity_min=120,
            quantity_max=185,
            weight=12,
            is_skippable=True,
            is_blockable=True,
        ),
        SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=2005,
            category="Waterfiends",
            quantity_min=130,
            quantity_max=170,
            weight=8,
            is_skippable=True,
            is_blockable=True,
        ),
        SlayerTask(
            master=SlayerMaster.KONAR,
            monster_id=1648,
            category="Dragons",
            quantity_min=100,
            quantity_max=150,
            weight=10,
            is_skippable=True,
            is_blockable=True,
        ),
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    return tasks
