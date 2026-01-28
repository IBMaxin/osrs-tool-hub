"""Unit tests for gear utility functions."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.services.gear.utils import find_item_by_name
from backend.models import Item


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
def sample_items(test_session):
    """Create sample items for testing."""
    items = [
        Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
        ),
        Item(
            id=1163,
            name="Rune full helm",
            members=True,
            limit=70,
            value=20000,
        ),
        Item(
            id=12954,
            name="Dragon scimitar",
            members=True,
            limit=70,
            value=60000,
        ),
    ]
    for item in items:
        test_session.add(item)
    test_session.commit()
    return items


class TestFindItemByName:
    """Test find_item_by_name function."""

    def test_find_item_by_name_exact_match(self, test_session, sample_items):
        """Test find_item_by_name with exact match."""
        result = find_item_by_name(test_session, "Abyssal whip")
        assert result is not None
        assert result.id == 4151
        assert result.name == "Abyssal whip"

    def test_find_item_by_name_case_insensitive(self, test_session, sample_items):
        """Test find_item_by_name is case-insensitive."""
        result = find_item_by_name(test_session, "ABYSSAL WHIP")
        assert result is not None
        assert result.id == 4151

        result = find_item_by_name(test_session, "abyssal whip")
        assert result is not None
        assert result.id == 4151

    def test_find_item_by_name_partial_match(self, test_session, sample_items):
        """Test find_item_by_name with partial match."""
        result = find_item_by_name(test_session, "whip")
        assert result is not None
        assert result.id == 4151

        result = find_item_by_name(test_session, "Rune")
        assert result is not None
        assert "Rune" in result.name

    def test_find_item_by_name_partial_match_prefers_shorter(self, test_session):
        """Test find_item_by_name prefers shorter names for partial matches."""
        # Create items with similar names
        item1 = Item(id=1, name="Rune", members=True, value=1000)
        item2 = Item(id=2, name="Rune full helm", members=True, value=20000)
        test_session.add(item1)
        test_session.add(item2)
        test_session.commit()

        result = find_item_by_name(test_session, "Rune")
        # Should prefer shorter name (exact match)
        assert result is not None
        assert result.id == 1

    def test_find_item_by_name_not_found(self, test_session):
        """Test find_item_by_name returns None for non-existent items."""
        result = find_item_by_name(test_session, "Non-existent item")
        assert result is None

    def test_find_item_by_name_empty_string(self, test_session):
        """Test find_item_by_name handles empty string."""
        result = find_item_by_name(test_session, "")
        assert result is None

    def test_find_item_by_name_multiple_partial_matches(self, test_session):
        """Test find_item_by_name handles multiple partial matches."""
        # Create multiple items with similar names
        item1 = Item(id=100, name="Dragon scimitar", members=True, value=60000)
        item2 = Item(id=101, name="Dragon longsword", members=True, value=60000)
        item3 = Item(id=102, name="Dragon dagger", members=True, value=30000)
        test_session.add(item1)
        test_session.add(item2)
        test_session.add(item3)
        test_session.commit()

        result = find_item_by_name(test_session, "Dragon")
        # Should return one of them (prefers shorter)
        assert result is not None
        assert "Dragon" in result.name
