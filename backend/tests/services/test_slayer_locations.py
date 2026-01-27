"""Unit tests for slayer location retrieval functionality."""
import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from unittest.mock import patch

from backend.services.slayer import SlayerService
from backend.models import Monster, SlayerTask, SlayerMaster


# Test engine
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


@pytest.fixture
def session():
    """Create a test database session."""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as test_session:
        yield test_session
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def sample_monster(session: Session) -> Monster:
    """Create a sample monster for testing."""
    monster = Monster(
        id=1,
        name="Abyssal demon",
        combat_level=124,
        hitpoints=150,
        slayer_xp=150,
        defence_level=60,
        magic_level=1,
        ranged_level=1,
        defence_stab=20,
        defence_slash=20,
        defence_crush=20,
        defence_magic=20,
        defence_ranged=20,
        is_slayer_monster=True
    )
    session.add(monster)
    session.commit()
    session.refresh(monster)
    return monster


@pytest.fixture
def sample_task(session: Session, sample_monster: Monster) -> SlayerTask:
    """Create a sample slayer task for testing."""
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=sample_monster.id,
        category="Abyssal demons",
        quantity_min=120,
        quantity_max=185,
        weight=12,
        is_skippable=True,
        is_blockable=True
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def test_get_task_locations_success(session: Session, sample_task: SlayerTask):
    """Test successful retrieval of location data."""
    service = SlayerService(session)
    result = service.get_task_locations(sample_task.id)
    
    # Verify basic fields
    assert "error" not in result
    assert result["task_id"] == sample_task.id
    assert result["monster_name"] == "Abyssal demon"
    assert result["category"] == "Abyssal demons"
    assert result["master"] == "Duradel"  # Capitalized from enum
    
    # Verify locations structure
    assert "locations" in result
    assert isinstance(result["locations"], list)
    assert len(result["locations"]) > 0
    
    # Verify first location has detailed data
    first_location = result["locations"][0]
    assert "name" in first_location
    assert "requirements" in first_location
    assert "multi_combat" in first_location
    assert "cannon" in first_location
    assert "safespot" in first_location
    assert "notes" in first_location
    assert "pros" in first_location
    assert "cons" in first_location
    assert "best_for" in first_location
    
    # Verify metadata fields
    assert "alternatives" in result
    assert "strategy" in result
    assert "weakness" in result
    assert "items_needed" in result
    assert "has_detailed_data" in result
    assert result["has_detailed_data"] is True  # Abyssal demons has detailed data


def test_get_task_locations_multiple_locations(session: Session, sample_task: SlayerTask):
    """Test that multiple locations are returned correctly."""
    service = SlayerService(session)
    result = service.get_task_locations(sample_task.id)
    
    # Abyssal demons should have 2 locations (Slayer Tower + Catacombs)
    assert len(result["locations"]) == 2
    
    location_names = [loc["name"] for loc in result["locations"]]
    assert "Slayer Tower" in location_names
    assert "Catacombs of Kourend" in location_names


def test_get_task_locations_with_requirements(session: Session, sample_task: SlayerTask):
    """Test that location requirements are properly included."""
    service = SlayerService(session)
    result = service.get_task_locations(sample_task.id)
    
    # Find Catacombs location (has requirements)
    catacombs = next(
        (loc for loc in result["locations"] if loc["name"] == "Catacombs of Kourend"),
        None
    )
    
    assert catacombs is not None
    assert "requirements" in catacombs
    assert "20% Arceuus favour" in catacombs["requirements"]
    assert catacombs["multi_combat"] is True
    assert catacombs["cannon"] is False


def test_get_task_locations_with_strategy(session: Session, sample_task: SlayerTask):
    """Test that strategy recommendations are included."""
    service = SlayerService(session)
    result = service.get_task_locations(sample_task.id)
    
    assert "strategy" in result
    assert len(result["strategy"]) > 0
    assert "Arclight" in result["strategy"]  # Abyssal demons strategy mentions Arclight


def test_get_task_locations_with_weakness(session: Session, sample_task: SlayerTask):
    """Test that monster weaknesses are included."""
    service = SlayerService(session)
    result = service.get_task_locations(sample_task.id)
    
    assert "weakness" in result
    assert "Slash" in result["weakness"]
    assert "Demonbane" in result["weakness"]


def test_get_task_locations_not_found(session: Session):
    """Test handling of non-existent task ID."""
    service = SlayerService(session)
    result = service.get_task_locations(99999)
    
    assert "error" in result
    assert result["error"] == "Task not found"


def test_get_task_locations_legacy_format(session: Session):
    """Test handling of legacy location format (list of strings)."""
    # Create a monster with legacy format location data
    monster = Monster(
        id=2,
        name="Black demons",
        combat_level=172,
        hitpoints=157,
        slayer_xp=157,
        defence_level=60,
        magic_level=1,
        ranged_level=1,
        defence_stab=20,
        defence_slash=20,
        defence_crush=20,
        defence_magic=20,
        defence_ranged=20,
        is_slayer_monster=True
    )
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=monster.id,
        category="Black Demons",  # Has legacy format in demon data
        quantity_min=130,
        quantity_max=200,
        weight=8,
        is_skippable=True,
        is_blockable=True
    )
    session.add(task)
    session.commit()
    
    service = SlayerService(session)
    result = service.get_task_locations(task.id)
    
    # Should still return data, but locations will be minimal dicts
    assert "error" not in result
    assert "locations" in result
    
    # Legacy format should be converted to dict format
    if result["locations"]:
        first_location = result["locations"][0]
        assert isinstance(first_location, dict)
        assert "name" in first_location


def test_get_task_locations_no_data(session: Session):
    """Test handling of task with no location data in SLAYER_TASK_DATA."""
    # Create a monster not in SLAYER_TASK_DATA
    monster = Monster(
        id=3,
        name="Unknown Monster",
        combat_level=50,
        hitpoints=50,
        slayer_xp=50,
        defence_level=30,
        magic_level=1,
        ranged_level=1,
        defence_stab=10,
        defence_slash=10,
        defence_crush=10,
        defence_magic=10,
        defence_ranged=10,
        is_slayer_monster=True
    )
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.TURAEL,
        monster_id=monster.id,
        category="Unknown Category",
        quantity_min=10,
        quantity_max=20,
        weight=5,
        is_skippable=True,
        is_blockable=False
    )
    session.add(task)
    session.commit()
    
    service = SlayerService(session)
    result = service.get_task_locations(task.id)
    
    # Should return basic structure with empty lists
    assert "error" not in result
    assert result["task_id"] == task.id
    assert result["monster_name"] == "Unknown Monster"
    assert result["locations"] == []
    assert result["alternatives"] == []
    assert result["strategy"] == ""
    assert result["has_detailed_data"] is False


def test_get_task_locations_with_alternatives(session: Session):
    """Test that alternative monsters are included."""
    # Create a gargoyle task (has Grotesque Guardians alternative)
    monster = Monster(
        id=4,
        name="Gargoyle",
        combat_level=111,
        hitpoints=105,
        slayer_xp=105,
        defence_level=80,
        magic_level=1,
        ranged_level=1,
        defence_stab=50,
        defence_slash=50,
        defence_crush=50,
        defence_magic=50,
        defence_ranged=50,
        is_slayer_monster=True
    )
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=monster.id,
        category="Gargoyles",
        quantity_min=110,
        quantity_max=170,
        weight=7,
        is_skippable=True,
        is_blockable=True
    )
    session.add(task)
    session.commit()
    
    service = SlayerService(session)
    result = service.get_task_locations(task.id)
    
    # Gargoyles should have Grotesque Guardians alternative
    assert "alternatives" in result
    assert len(result["alternatives"]) > 0
    
    # Check alternative structure
    alternative = result["alternatives"][0]
    assert "name" in alternative
    assert "notes" in alternative
    assert "Grotesque Guardians" in alternative["name"]


def test_get_task_locations_items_needed(session: Session):
    """Test that required items are included."""
    # Create a gargoyle task (requires rock hammer)
    monster = Monster(
        id=5,
        name="Gargoyle",
        combat_level=111,
        hitpoints=105,
        slayer_xp=105,
        defence_level=80,
        magic_level=1,
        ranged_level=1,
        defence_stab=50,
        defence_slash=50,
        defence_crush=50,
        defence_magic=50,
        defence_ranged=50,
        is_slayer_monster=True
    )
    session.add(monster)
    session.commit()
    
    task = SlayerTask(
        master=SlayerMaster.DURADEL,
        monster_id=monster.id,
        category="Gargoyles",
        quantity_min=110,
        quantity_max=170,
        weight=7,
        is_skippable=True,
        is_blockable=True
    )
    session.add(task)
    session.commit()
    
    service = SlayerService(session)
    result = service.get_task_locations(task.id)
    
    assert "items_needed" in result
    assert "Rock hammer" in result["items_needed"]
