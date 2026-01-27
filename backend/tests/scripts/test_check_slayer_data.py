"""Tests for check_slayer_data script."""
import pytest
from unittest.mock import patch
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.scripts.check_slayer_data import check_slayer_data
from backend.models import Monster, SlayerTask, SlayerMaster


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


def test_check_slayer_data_empty_database(test_engine, capsys):
    """Test check_slayer_data with empty database."""
    with patch('backend.scripts.check_slayer_data.engine', test_engine):
        result = check_slayer_data()
        
        assert result is False
        
        captured = capsys.readouterr()
        assert "Slayer data is missing!" in captured.out
        assert "Run: python -m backend.scripts.seed_slayer" in captured.out


def test_check_slayer_data_with_data(test_engine, capsys):
    """Test check_slayer_data with existing data."""
    with patch('backend.scripts.check_slayer_data.engine', test_engine):
        # Seed some data
        with Session(test_engine) as session:
            monster = Monster(
                id=415,
                name="Abyssal demon",
                combat_level=124,
                hitpoints=150,
                slayer_xp=150.0,
                is_slayer_monster=True
            )
            session.add(monster)
            
            task = SlayerTask(
                master=SlayerMaster.DURADEL,
                monster_id=415,
                category="Abyssal demons",
                quantity_min=120,
                quantity_max=185,
                weight=12,
                is_skippable=True,
                is_blockable=True
            )
            session.add(task)
            session.commit()
        
        result = check_slayer_data()
        
        assert result is True
        
        captured = capsys.readouterr()
        assert "Slayer data exists!" in captured.out
        assert "Monsters: 1" in captured.out
        assert "Tasks: 1" in captured.out


def test_check_slayer_data_shows_master_breakdown(test_engine, capsys):
    """Test that check_slayer_data shows task breakdown by master."""
    with patch('backend.scripts.check_slayer_data.engine', test_engine):
        # Seed data for multiple masters
        with Session(test_engine) as session:
            monster1 = Monster(id=415, name="Abyssal demon", combat_level=124, hitpoints=150, slayer_xp=150.0, is_slayer_monster=True)
            monster2 = Monster(id=11, name="Aberrant spectre", combat_level=96, hitpoints=90, slayer_xp=90.0, is_slayer_monster=True)
            session.add(monster1)
            session.add(monster2)
            
            task1 = SlayerTask(master=SlayerMaster.DURADEL, monster_id=415, category="Abyssal demons", quantity_min=120, quantity_max=185, weight=12, is_skippable=True, is_blockable=True)
            task2 = SlayerTask(master=SlayerMaster.KONAR, monster_id=11, category="Aberrant spectres", quantity_min=120, quantity_max=200, weight=8, is_skippable=True, is_blockable=True)
            session.add(task1)
            session.add(task2)
            session.commit()
        
        check_slayer_data()
        
        captured = capsys.readouterr()
        assert "Duradel" in captured.out or "KONAR" in captured.out
