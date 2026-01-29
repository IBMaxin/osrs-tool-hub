"""Unit tests for gear_calculations module."""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session

from backend.services.gear.gear_calculations import (
    suggest_gear_for_slot,
    calculate_dps_for_loadout,
    get_best_loadout_for_stats,
    get_upgrade_path_for_loadout,
    get_alternatives_for_slot,
    get_preset_loadout_for_tier,
    get_progression_loadout_for_tier,
    get_wiki_progression_for_style,
    suggest_slayer_gear_for_task,
)


class TestSuggestGearForSlot:
    """Test suggest_gear_for_slot function."""

    @patch("backend.services.gear.gear_calculations.suggest_gear")
    def test_suggest_gear_for_slot_delegates(self, mock_suggest_gear):
        """Test that suggest_gear_for_slot delegates to suggest_gear."""
        mock_session = MagicMock(spec=Session)
        mock_suggest_gear.return_value = [{"id": 1, "name": "Test"}]

        result = suggest_gear_for_slot(mock_session, "weapon", "melee", 1000000, 70)

        mock_suggest_gear.assert_called_once_with(mock_session, "weapon", "melee", 1000000, 70)
        assert result == [{"id": 1, "name": "Test"}]


class TestCalculateDpsForLoadout:
    """Test calculate_dps_for_loadout function."""

    @patch("backend.services.gear.gear_calculations.calculate_dps")
    def test_calculate_dps_for_loadout_delegates(self, mock_calculate_dps):
        """Test that calculate_dps_for_loadout delegates to calculate_dps."""
        mock_session = MagicMock(spec=Session)
        mock_items = {"weapon": MagicMock()}
        mock_calculate_dps.return_value = {"dps": 5.5}

        result = calculate_dps_for_loadout(mock_session, mock_items, "melee", "slash", {"attack": 70})

        mock_calculate_dps.assert_called_once_with(mock_items, "melee", "slash", {"attack": 70})
        assert result == {"dps": 5.5}


class TestGetBestLoadoutForStats:
    """Test get_best_loadout_for_stats function."""

    @patch("backend.services.gear.gear_calculations.get_best_loadout")
    def test_get_best_loadout_for_stats_delegates(self, mock_get_best_loadout):
        """Test that get_best_loadout_for_stats delegates to get_best_loadout."""
        mock_session = MagicMock(spec=Session)
        mock_get_best_loadout.return_value = {"total_cost": 1000000}

        result = get_best_loadout_for_stats(
            mock_session, "melee", 10000000, {"attack": 70}, "slash", None, None, None, False, None, None, False
        )

        mock_get_best_loadout.assert_called_once()
        assert result == {"total_cost": 1000000}


class TestGetUpgradePathForLoadout:
    """Test get_upgrade_path_for_loadout function."""

    @patch("backend.services.gear.gear_calculations.get_upgrade_path")
    def test_get_upgrade_path_for_loadout_delegates(self, mock_get_upgrade_path):
        """Test that get_upgrade_path_for_loadout delegates to get_upgrade_path."""
        mock_session = MagicMock(spec=Session)
        mock_get_upgrade_path.return_value = {"current_dps": 5.0}

        result = get_upgrade_path_for_loadout(
            mock_session, {"weapon": 4151}, "melee", 1000000, {"attack": 70}, "slash", None, None
        )

        mock_get_upgrade_path.assert_called_once()
        assert result == {"current_dps": 5.0}


class TestGetAlternativesForSlot:
    """Test get_alternatives_for_slot function."""

    @patch("backend.services.gear.gear_calculations.get_alternatives")
    def test_get_alternatives_for_slot_delegates(self, mock_get_alternatives):
        """Test that get_alternatives_for_slot delegates to get_alternatives."""
        mock_session = MagicMock(spec=Session)
        mock_get_alternatives.return_value = [{"id": 1, "name": "Alt"}]

        result = get_alternatives_for_slot(
            mock_session, "weapon", "melee", 1000000, {"attack": 70}, "slash", None, None, 10
        )

        mock_get_alternatives.assert_called_once()
        assert result == [{"id": 1, "name": "Alt"}]


class TestGetPresetLoadoutForTier:
    """Test get_preset_loadout_for_tier function."""

    @patch("backend.services.gear.gear_calculations.get_preset_loadout")
    def test_get_preset_loadout_for_tier_delegates(self, mock_get_preset_loadout):
        """Test that get_preset_loadout_for_tier delegates to get_preset_loadout."""
        mock_session = MagicMock(spec=Session)
        mock_get_preset_loadout.return_value = {"tier": "low"}

        result = get_preset_loadout_for_tier(mock_session, "melee", "low")

        mock_get_preset_loadout.assert_called_once_with(mock_session, "melee", "low")
        assert result == {"tier": "low"}


class TestGetProgressionLoadoutForTier:
    """Test get_progression_loadout_for_tier function."""

    @patch("backend.services.gear.gear_calculations.get_progression_loadout")
    def test_get_progression_loadout_for_tier_delegates(self, mock_get_progression_loadout):
        """Test that get_progression_loadout_for_tier delegates to get_progression_loadout."""
        mock_session = MagicMock(spec=Session)
        mock_get_progression_loadout.return_value = {"tier": "mid"}

        result = get_progression_loadout_for_tier(mock_session, "melee", "mid")

        mock_get_progression_loadout.assert_called_once_with(mock_session, "melee", "mid")
        assert result == {"tier": "mid"}


class TestGetWikiProgressionForStyle:
    """Test get_wiki_progression_for_style function."""

    @patch("backend.services.gear.gear_calculations.get_wiki_progression")
    def test_get_wiki_progression_for_style_delegates(self, mock_get_wiki_progression):
        """Test that get_wiki_progression_for_style delegates to get_wiki_progression."""
        mock_session = MagicMock(spec=Session)
        mock_get_wiki_progression.return_value = {"style": "melee"}

        result = get_wiki_progression_for_style(mock_session, "melee")

        mock_get_wiki_progression.assert_called_once_with(mock_session, "melee")
        assert result == {"style": "melee"}


class TestSuggestSlayerGearForTask:
    """Test suggest_slayer_gear_for_task function."""

    @patch("backend.services.gear.gear_calculations.suggest_slayer_gear")
    def test_suggest_slayer_gear_for_task_delegates(self, mock_suggest_slayer_gear):
        """Test that suggest_slayer_gear_for_task delegates to suggest_slayer_gear."""
        mock_session = MagicMock(spec=Session)
        mock_suggest_slayer_gear.return_value = {"task_id": 1}

        result = suggest_slayer_gear_for_task(
            mock_session, 1, {"attack": 70}, 10000000, "melee", None, None, False
        )

        mock_suggest_slayer_gear.assert_called_once()
        assert result == {"task_id": 1}
