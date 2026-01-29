"""Unit tests for gear_sets module."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.services.gear.gear_sets import (
    create_gear_set,
    get_all_gear_sets,
    get_gear_set_by_id,
    delete_gear_set,
)
from backend.models import GearSet, Item
from backend.services.gear.pricing import get_item_price


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def sample_item(test_session):
    """Create a sample item for testing."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        members=True,
        limit=70,
        value=2000000,
        slot="weapon",
        attack_stab=82,
        attack_slash=82,
        melee_strength=82,
        attack_req=70,
    )
    test_session.add(item)
    test_session.commit()
    test_session.refresh(item)
    return item


class TestCreateGearSet:
    """Test create_gear_set function."""

    def test_create_gear_set_success(self, test_session, sample_item):
        """Test creating a gear set successfully."""
        items = {sample_item.id: 1}
        gear_set = create_gear_set(test_session, "Test Set", items, "Test description")

        assert gear_set.name == "Test Set"
        assert gear_set.description == "Test description"
        assert gear_set.id is not None
        assert gear_set.total_cost > 0

    def test_create_gear_set_with_multiple_items(self, test_session, sample_item):
        """Test creating a gear set with multiple items."""
        # Create another item
        item2 = Item(
            id=4152,
            name="Test item 2",
            members=True,
            limit=1,
            value=1000,
            slot="head",
        )
        test_session.add(item2)
        test_session.commit()

        items = {sample_item.id: 1, item2.id: 2}
        gear_set = create_gear_set(test_session, "Multi Item Set", items)

        assert gear_set.name == "Multi Item Set"
        assert gear_set.total_cost > 0

    def test_create_gear_set_without_description(self, test_session, sample_item):
        """Test creating a gear set without description."""
        items = {sample_item.id: 1}
        gear_set = create_gear_set(test_session, "No Desc Set", items)

        assert gear_set.name == "No Desc Set"
        assert gear_set.description is None


class TestGetAllGearSets:
    """Test get_all_gear_sets function."""

    def test_get_all_gear_sets_empty(self, test_session):
        """Test getting all gear sets when none exist."""
        gear_sets = get_all_gear_sets(test_session)
        assert gear_sets == []

    def test_get_all_gear_sets_multiple(self, test_session, sample_item):
        """Test getting all gear sets."""
        items = {sample_item.id: 1}
        gear_set1 = create_gear_set(test_session, "Set 1", items)
        gear_set2 = create_gear_set(test_session, "Set 2", items)

        gear_sets = get_all_gear_sets(test_session)
        assert len(gear_sets) == 2
        # Should be ordered by created_at desc (newest first)
        assert gear_sets[0].name in ("Set 1", "Set 2")
        assert gear_sets[1].name in ("Set 1", "Set 2")


class TestGetGearSetById:
    """Test get_gear_set_by_id function."""

    def test_get_gear_set_by_id_exists(self, test_session, sample_item):
        """Test getting a gear set by ID when it exists."""
        items = {sample_item.id: 1}
        gear_set = create_gear_set(test_session, "Test Set", items)

        retrieved = get_gear_set_by_id(test_session, gear_set.id)
        assert retrieved is not None
        assert retrieved.id == gear_set.id
        assert retrieved.name == "Test Set"

    def test_get_gear_set_by_id_not_exists(self, test_session):
        """Test getting a gear set by ID when it doesn't exist."""
        retrieved = get_gear_set_by_id(test_session, 99999)
        assert retrieved is None


class TestDeleteGearSet:
    """Test delete_gear_set function."""

    def test_delete_gear_set_exists(self, test_session, sample_item):
        """Test deleting a gear set that exists."""
        items = {sample_item.id: 1}
        gear_set = create_gear_set(test_session, "To Delete", items)

        result = delete_gear_set(test_session, gear_set.id)
        assert result is True

        # Verify it's deleted
        retrieved = get_gear_set_by_id(test_session, gear_set.id)
        assert retrieved is None

    def test_delete_gear_set_not_exists(self, test_session):
        """Test deleting a gear set that doesn't exist."""
        result = delete_gear_set(test_session, 99999)
        assert result is False
