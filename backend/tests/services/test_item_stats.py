"""Tests for item stats importer."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from backend.services.item_stats import import_item_stats
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


class TestImportItemStats:
    """Test import_item_stats function."""

    @pytest.mark.asyncio
    async def test_import_item_stats_updates_equipable_items(self, test_session):
        """Test that import_item_stats updates equipable items with stats."""
        # Create item in DB
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "4151": {
                "equipable_by_player": True,
                "equipment": {
                    "slot": "weapon",
                    "attack_stab": 82,
                    "attack_slash": 82,
                    "attack_crush": 0,
                    "attack_magic": 0,
                    "attack_ranged": 0,
                    "melee_strength": 82,
                    "ranged_strength": 0,
                    "magic_damage": 0,
                    "prayer": 0,
                    "defence_stab": 0,
                    "defence_slash": 0,
                    "defence_crush": 0,
                    "defence_magic": 0,
                    "defence_ranged": 0,
                },
                "requirements": {
                    "attack": 70,
                    "strength": 70,
                    "defence": 1,
                    "ranged": 1,
                    "magic": 1,
                    "prayer": 1,
                    "slayer": 0,
                },
                "weapon": {
                    "weapon_type": "whip",
                    "weapon_speed": 4,
                },
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            # Verify item was updated
            updated_item = test_session.get(Item, 4151)
            assert updated_item.slot == "weapon"
            assert updated_item.attack_req == 70
            assert updated_item.strength_req == 70
            assert updated_item.attack_stab == 82
            assert updated_item.attack_slash == 82
            assert updated_item.melee_strength == 82
            assert updated_item.attack_speed == 4
            assert updated_item.is_2h is False

    @pytest.mark.asyncio
    async def test_import_item_stats_skips_non_equipable(self, test_session):
        """Test that import_item_stats skips non-equipable items."""
        # Create item in DB
        item = Item(
            id=314,
            name="Feather",
            members=False,
            limit=13000,
            value=2,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "314": {
                "equipable_by_player": False,  # Not equipable
                "equipment": {},
                "requirements": {},
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            # Verify item was not updated (still has default values)
            updated_item = test_session.get(Item, 314)
            assert updated_item.name == "Feather"
            # Stats should remain at defaults (1s)
            assert updated_item.attack_req == 1

    @pytest.mark.asyncio
    async def test_import_item_stats_handles_missing_item_in_data(self, test_session):
        """Test that import_item_stats handles items not in OSRSBox data."""
        # Create item in DB that's not in OSRSBox data
        item = Item(
            id=99999,
            name="Unknown item",
            members=True,
            limit=1,
            value=1,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "4151": {
                "equipable_by_player": True,
                "equipment": {"slot": "weapon"},
                "requirements": {},
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            # Item 99999 should not be updated (not in OSRSBox data)
            unchanged_item = test_session.get(Item, 99999)
            assert unchanged_item.name == "Unknown item"
            assert unchanged_item.attack_req == 1  # Still default

    @pytest.mark.asyncio
    async def test_import_item_stats_sets_2h_flag(self, test_session):
        """Test that import_item_stats correctly sets is_2h flag."""
        item = Item(
            id=7158,
            name="Dragon mace",
            members=True,
            limit=8,
            value=50000,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "7158": {
                "equipable_by_player": True,
                "equipment": {"slot": "weapon"},
                "requirements": {},
                "weapon": {
                    "weapon_type": "2h_sword",  # 2-handed weapon
                    "weapon_speed": 4,
                },
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            updated_item = test_session.get(Item, 7158)
            assert updated_item.is_2h is True

    @pytest.mark.asyncio
    async def test_import_item_stats_sets_quest_requirement(self, test_session):
        """Test that import_item_stats sets quest requirement."""
        item = Item(
            id=11694,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "11694": {
                "equipable_by_player": True,
                "equipment": {"slot": "weapon"},
                "requirements": {},
                "weapon": {"weapon_type": "whip", "weapon_speed": 4},
                "quest": "Monkey Madness II",  # Quest requirement
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            updated_item = test_session.get(Item, 11694)
            assert updated_item.quest_req == "Monkey Madness II"

    @pytest.mark.asyncio
    async def test_import_item_stats_handles_http_error(self, test_session):
        """Test that import_item_stats handles HTTP errors gracefully."""
        import httpx

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_error = httpx.HTTPStatusError(
                "500 Server Error", request=MagicMock(), response=MagicMock()
            )
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=mock_error)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            # Should not raise, but return early
            await import_item_stats(test_session)

            # No items should be updated
            items = test_session.exec(select(Item)).all()
            assert len(items) == 0

    @pytest.mark.asyncio
    async def test_import_item_stats_handles_network_error(self, test_session):
        """Test that import_item_stats handles network errors gracefully."""
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=Exception("Network timeout"))
            mock_client_class.return_value.__aenter__.return_value = mock_client

            # Should not raise, but return early
            await import_item_stats(test_session)

            # No items should be updated
            items = test_session.exec(select(Item)).all()
            assert len(items) == 0

    @pytest.mark.asyncio
    async def test_import_item_stats_updates_all_stat_fields(self, test_session):
        """Test that import_item_stats updates all stat fields correctly."""
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        mock_osrsbox_data = {
            "4151": {
                "equipable_by_player": True,
                "equipment": {
                    "slot": "weapon",
                    "attack_stab": 82,
                    "attack_slash": 82,
                    "attack_crush": 0,
                    "attack_magic": 5,
                    "attack_ranged": -10,
                    "melee_strength": 82,
                    "ranged_strength": 0,
                    "magic_damage": 0,
                    "prayer": 0,
                    "defence_stab": 0,
                    "defence_slash": 0,
                    "defence_crush": 0,
                    "defence_magic": 0,
                    "defence_ranged": 0,
                },
                "requirements": {
                    "attack": 70,
                    "strength": 70,
                    "defence": 1,
                    "ranged": 1,
                    "magic": 1,
                    "prayer": 1,
                    "slayer": 0,
                },
                "weapon": {
                    "weapon_type": "whip",
                    "weapon_speed": 4,
                },
            }
        }

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_osrsbox_data
            mock_response.raise_for_status = MagicMock()
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_class.return_value.__aenter__.return_value = mock_client

            await import_item_stats(test_session)

            updated_item = test_session.get(Item, 4151)
            # Verify all offensive stats
            assert updated_item.attack_stab == 82
            assert updated_item.attack_slash == 82
            assert updated_item.attack_crush == 0
            assert updated_item.attack_magic == 5
            assert updated_item.attack_ranged == -10
            # Verify strength bonuses
            assert updated_item.melee_strength == 82
            assert updated_item.ranged_strength == 0
            assert updated_item.magic_damage == 0
            assert updated_item.prayer_bonus == 0
            # Verify defensive stats
            assert updated_item.defence_stab == 0
            assert updated_item.defence_slash == 0
            assert updated_item.defence_crush == 0
            assert updated_item.defence_magic == 0
            assert updated_item.defence_ranged == 0
