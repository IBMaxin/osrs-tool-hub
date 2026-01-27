"""Tests for seed_slayer script."""
import pytest
from unittest.mock import patch
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from backend.scripts.seed_slayer import seed_slayer_data
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


def test_seed_slayer_data_creates_monsters(test_engine):
    """Test that seed_slayer_data creates monsters."""
    with patch('backend.scripts.seed_slayer.engine', test_engine):
        seed_slayer_data()
        
        with Session(test_engine) as session:
            monsters = session.exec(select(Monster)).all()
            assert len(monsters) > 0
            
            # Check specific monster exists
            abyssal = session.get(Monster, 415)
            assert abyssal is not None
            assert abyssal.name == "Abyssal demon"
            assert abyssal.combat_level == 124
            assert abyssal.is_demon is True


def test_seed_slayer_data_creates_tasks(test_engine):
    """Test that seed_slayer_data creates slayer tasks."""
    with patch('backend.scripts.seed_slayer.engine', test_engine):
        seed_slayer_data()
        
        with Session(test_engine) as session:
            tasks = session.exec(select(SlayerTask)).all()
            assert len(tasks) > 0
            
            # Check task for Duradel exists
            duradel_tasks = session.exec(
                select(SlayerTask).where(SlayerTask.master == SlayerMaster.DURADEL)
            ).all()
            assert len(duradel_tasks) > 0


def test_seed_slayer_data_idempotent(test_engine):
    """Test that running seed_slayer_data multiple times doesn't create duplicates."""
    with patch('backend.scripts.seed_slayer.engine', test_engine):
        # Run twice
        seed_slayer_data()
        
        with Session(test_engine) as session:
            first_run_monsters = session.exec(select(Monster)).all()
            first_run_tasks = session.exec(select(SlayerTask)).all()
        
        seed_slayer_data()
        
        with Session(test_engine) as session:
            second_run_monsters = session.exec(select(Monster)).all()
            second_run_tasks = session.exec(select(SlayerTask)).all()
            
            # Should have same count (no duplicates)
            assert len(first_run_monsters) == len(second_run_monsters)
            assert len(first_run_tasks) == len(second_run_tasks)


def test_seed_slayer_data_monster_task_relationship(test_engine):
    """Test that tasks are properly linked to monsters."""
    with patch('backend.scripts.seed_slayer.engine', test_engine):
        seed_slayer_data()
        
        with Session(test_engine) as session:
            # Get a task
            task = session.exec(
                select(SlayerTask).where(SlayerTask.master == SlayerMaster.DURADEL)
            ).first()
            
            assert task is not None
            
            # Verify monster exists and is linked
            monster = session.get(Monster, task.monster_id)
            assert monster is not None
            assert task.monster_id == monster.id
