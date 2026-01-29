"""Unit tests for gear progression utilities."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch

from backend.services.gear.progression import (
    get_preset_loadout,
    get_progression_loadout,
    get_wiki_progression,
)
from backend.models import Item, PriceSnapshot


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
            slot="weapon",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_req=70,
            strength_req=70,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        ),
        Item(
            id=1163,
            name="Rune full helm",
            members=True,
            limit=70,
            value=20000,
            slot="head",
            attack_req=40,
            strength_req=1,
            defence_req=40,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        ),
    ]
    for item in items:
        test_session.add(item)
    test_session.commit()
    return items


class TestGetPresetLoadout:
    """Test get_preset_loadout function."""

    def test_get_preset_loadout_valid(self, test_session, sample_items):
        """Test get_preset_loadout with valid combat style and tier."""
        # Mock GEAR_PRESETS to return a simple preset
        mock_preset = {
            "weapon": ["Abyssal whip"],
            "head": ["Rune full helm"],
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            assert loadout["combat_style"] == "melee"
            assert loadout["tier"] == "low"
            assert "weapon" in loadout["slots"]
            assert loadout["slots"]["weapon"] is not None
            assert loadout["slots"]["weapon"]["id"] == 4151
            assert loadout["total_cost"] > 0

    def test_get_preset_loadout_invalid_combat_style(self, test_session):
        """Test get_preset_loadout raises ValueError for invalid combat style."""
        with pytest.raises(ValueError, match="Invalid combat style"):
            get_preset_loadout(test_session, "invalid_style", "low")

    def test_get_preset_loadout_invalid_tier(self, test_session):
        """Test get_preset_loadout raises ValueError for invalid tier."""
        with patch("backend.services.gear.progression.presets.GEAR_PRESETS", {"melee": {}}):
            with pytest.raises(ValueError, match="Invalid tier"):
                get_preset_loadout(test_session, "melee", "invalid_tier")

    def test_get_preset_loadout_empty_slot(self, test_session):
        """Test get_preset_loadout handles empty slots (e.g., shield for 2H)."""
        mock_preset = {
            "weapon": ["Abyssal whip"],
            "shield": [],  # Empty slot
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            assert loadout["slots"]["shield"] is None

    def test_get_preset_loadout_missing_item(self, test_session):
        """Test get_preset_loadout handles missing items."""
        mock_preset = {
            "weapon": ["Non-existent item"],
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            assert loadout["slots"]["weapon"] is None
            assert len(loadout["missing_items"]) > 0
            assert loadout["missing_items"][0]["slot"] == "weapon"

    def test_get_preset_loadout_multiple_item_options(self, test_session, sample_items):
        """Test get_preset_loadout tries multiple item names until one is found."""
        mock_preset = {
            "weapon": ["Non-existent item", "Abyssal whip"],  # Second one exists
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            assert loadout["slots"]["weapon"] is not None
            assert loadout["slots"]["weapon"]["id"] == 4151

    def test_get_preset_loadout_includes_item_details(self, test_session, sample_items):
        """Test get_preset_loadout includes all item details."""
        mock_preset = {
            "weapon": ["Abyssal whip"],
        }

        # Add price snapshot
        snapshot = PriceSnapshot(item_id=4151, high_price=1500000, low_price=1400000)
        test_session.add(snapshot)
        test_session.commit()

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            weapon_data = loadout["slots"]["weapon"]
            assert "requirements" in weapon_data
            assert "offensive_stats" in weapon_data
            assert "strength_bonuses" in weapon_data
            assert "defensive_stats" in weapon_data
            assert weapon_data["price"] == 1500000  # Uses snapshot high_price

    def test_get_preset_loadout_uses_item_value_when_no_snapshot(self, test_session, sample_items):
        """Test get_preset_loadout uses item.value when PriceSnapshot is missing."""
        mock_preset = {
            "weapon": ["Abyssal whip"],
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            weapon_data = loadout["slots"]["weapon"]
            # Should use item.value (2000000) since no snapshot
            assert weapon_data["price"] == 2000000

    def test_get_preset_loadout_uses_zero_when_no_value(self, test_session):
        """Test get_preset_loadout uses 0 when item.value is None."""
        # Create item with no value
        item = Item(
            id=9999,
            name="Test item",
            members=True,
            value=0,
            slot="weapon",
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

        mock_preset = {
            "weapon": ["Test item"],
        }

        with patch(
            "backend.services.gear.progression.presets.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            loadout = get_preset_loadout(test_session, "melee", "low")

            weapon_data = loadout["slots"]["weapon"]
            assert weapon_data["price"] == 0


class TestGetProgressionLoadout:
    """Test get_progression_loadout function."""

    def test_get_progression_loadout_valid(self, test_session, sample_items):
        """Test get_progression_loadout with valid style and tier."""
        mock_preset = {
            "weapon": ["Abyssal whip"],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            result = get_progression_loadout(test_session, "melee", "low")

            assert result["tier"] == "low"
            assert result["style"] == "melee"
            assert "loadout" in result
            assert "weapon" in result["loadout"]
            assert result["loadout"]["weapon"]["id"] == 4151

    def test_get_progression_loadout_invalid_style(self, test_session):
        """Test get_progression_loadout returns error for invalid style."""
        result = get_progression_loadout(test_session, "invalid_style", "low")
        assert "error" in result

    def test_get_progression_loadout_invalid_tier(self, test_session):
        """Test get_progression_loadout returns error for invalid tier."""
        with patch(
            "backend.services.gear.progression.wiki_progression.GEAR_PRESETS", {"melee": {}}
        ):
            result = get_progression_loadout(test_session, "melee", "invalid_tier")
            assert "error" in result

    def test_get_progression_loadout_empty_slot(self, test_session):
        """Test get_progression_loadout skips empty slots."""
        mock_preset = {
            "weapon": ["Abyssal whip"],
            "shield": [],  # Empty slot
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            result = get_progression_loadout(test_session, "melee", "low")

            assert "shield" not in result["loadout"]  # Empty slots are skipped

    def test_get_progression_loadout_missing_item(self, test_session):
        """Test get_progression_loadout handles missing items."""
        mock_preset = {
            "weapon": ["Non-existent item"],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.GEAR_PRESETS",
            {"melee": {"low": mock_preset}},
        ):
            result = get_progression_loadout(test_session, "melee", "low")

            assert "weapon" not in result["loadout"]  # Missing items are skipped


class TestGetWikiProgression:
    """Test get_wiki_progression function."""

    def test_get_wiki_progression_valid_style(self, test_session, sample_items):
        """Test get_wiki_progression with valid combat style."""
        mock_wiki_data = {
            "head": [
                {
                    "tier": "low",
                    "items": ["Rune full helm"],
                }
            ],
            "weapon": [
                {
                    "tier": "mid",
                    "items": ["Abyssal whip"],
                }
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            assert "head" in result
            assert "weapon" in result
            assert len(result["head"]) > 0
            assert result["head"][0]["tier"] == "low"
            assert len(result["head"][0]["items"]) > 0

    def test_get_wiki_progression_invalid_style(self, test_session):
        """Test get_wiki_progression returns empty dict for invalid style."""
        result = get_wiki_progression(test_session, "invalid_style")
        assert result == {}

    def test_get_wiki_progression_enriches_items(self, test_session, sample_items):
        """Test get_wiki_progression enriches items with price and stats."""
        # Add price snapshot
        snapshot = PriceSnapshot(item_id=4151, high_price=1500000, low_price=1400000)
        test_session.add(snapshot)
        test_session.commit()

        mock_wiki_data = {
            "weapon": [
                {
                    "tier": "mid",
                    "items": ["Abyssal whip"],
                }
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            item = result["weapon"][0]["items"][0]
            assert item["id"] == 4151
            assert item["price"] == 1500000
            assert "requirements" in item
            assert "stats" in item
            assert "wiki_url" in item

    def test_get_wiki_progression_handles_missing_items(self, test_session):
        """Test get_wiki_progression handles items not in database."""
        mock_wiki_data = {
            "weapon": [
                {
                    "tier": "mid",
                    "items": ["Non-existent item"],
                }
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            item = result["weapon"][0]["items"][0]
            assert item["id"] is None
            assert item["not_found"] is True
            assert item["price"] is None

    def test_get_wiki_progression_handles_invalid_tier_structure(self, test_session):
        """Test get_wiki_progression handles invalid tier structure gracefully."""
        mock_wiki_data = {
            "head": [
                "invalid",  # Not a dict
                {"tier": "low", "items": []},  # Valid
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            # Should handle invalid structure and process valid ones
            assert "head" in result
            # Only valid tier should be processed
            assert len(result["head"]) == 1

    def test_get_wiki_progression_handles_invalid_items_list(self, test_session):
        """Test get_wiki_progression handles invalid items list."""
        mock_wiki_data = {
            "head": [
                {
                    "tier": "low",
                    "items": "not a list",  # Invalid
                }
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            # Should handle gracefully
            assert "head" in result
            assert len(result["head"]) == 0  # Invalid items list skipped

    def test_get_wiki_progression_handles_non_string_item_names(self, test_session, sample_items):
        """Test get_wiki_progression handles non-string item names."""
        mock_wiki_data = {
            "head": [
                {
                    "tier": "low",
                    "items": [123, "Rune full helm"],  # First is not string
                }
            ],
        }

        with patch(
            "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
            {"melee": mock_wiki_data},
        ):
            result = get_wiki_progression(test_session, "melee")

            # Should skip non-string items and process valid ones
            assert "head" in result
            items = result["head"][0]["items"]
            # Should only have the valid string item
            assert len(items) == 1
            assert items[0]["name"] == "Rune full helm"

    def test_get_wiki_progression_determines_game_stage(self, test_session, sample_items):
        """Test get_wiki_progression determines game stage correctly."""
        from backend.services.gear.progression.wiki_progression import _determine_game_stage

        assert _determine_game_stage("torva") == "late_game"
        assert _determine_game_stage("barrows") == "mid_game"
        assert _determine_game_stage("rune") == "mid_game"
        assert _determine_game_stage("iron") == "early_game"

    def test_get_wiki_progression_determines_content_tags(self, test_session, sample_items):
        """Test get_wiki_progression determines content tags correctly."""
        from backend.services.gear.progression.wiki_progression import _determine_content_tags

        tags = _determine_content_tags("void", "head", "melee")
        assert "Pest Control" in tags

        tags = _determine_content_tags("masori", "body", "ranged")
        assert "ToA" in tags

        tags = _determine_content_tags("torva", "body", "melee")
        assert "GWD" in tags

        tags = _determine_content_tags("unknown", "weapon", "melee")
        assert "General" in tags
        assert "Questing" in tags  # For weapon slot

    def test_get_wiki_progression_handles_item_processing_errors(self, test_session):
        """Test get_wiki_progression handles item processing errors gracefully."""
        mock_wiki_data = {
            "weapon": [
                {
                    "tier": "mid",
                    "items": ["Abyssal whip"],
                }
            ],
        }

        with (
            patch(
                "backend.services.gear.progression.wiki_progression.WIKI_PROGRESSION",
                {"melee": mock_wiki_data},
            ),
            patch(
                "backend.services.gear.progression.wiki_progression.find_item_by_name",
                side_effect=Exception("Processing error"),
            ),
        ):
            result = get_wiki_progression(test_session, "melee")

            # Should handle error and add fallback entry
            assert "weapon" in result
            items = result["weapon"][0]["items"]
            assert len(items) == 1
            assert items[0]["not_found"] is True
            assert "error" in items[0]
