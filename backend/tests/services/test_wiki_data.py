"""Unit tests for wiki_data module."""

import pytest
from unittest.mock import patch, mock_open
import json

from backend.services.wiki_data import (
    get_progression_data,
    get_slot_progression,
    get_all_slots,
    WIKI_PROGRESSION,
)


class TestGetProgressionData:
    """Test get_progression_data function."""

    def test_get_progression_data_valid_style(self):
        """Test get_progression_data with valid combat style."""
        result = get_progression_data("melee")
        assert isinstance(result, dict)

    def test_get_progression_data_invalid_style(self):
        """Test get_progression_data with invalid combat style."""
        result = get_progression_data("invalid_style")
        assert result == {}

    def test_get_progression_data_all_styles(self):
        """Test get_progression_data for all combat styles."""
        for style in ["melee", "ranged", "magic"]:
            result = get_progression_data(style)
            assert isinstance(result, dict)


class TestGetSlotProgression:
    """Test get_slot_progression function."""

    def test_get_slot_progression_valid(self):
        """Test get_slot_progression with valid style and slot."""
        result = get_slot_progression("melee", "head")
        assert isinstance(result, list)

    def test_get_slot_progression_invalid_style(self):
        """Test get_slot_progression with invalid style."""
        result = get_slot_progression("invalid_style", "head")
        assert result == []

    def test_get_slot_progression_invalid_slot(self):
        """Test get_slot_progression with invalid slot."""
        result = get_slot_progression("melee", "invalid_slot")
        assert result == []


class TestGetAllSlots:
    """Test get_all_slots function."""

    def test_get_all_slots_valid_style(self):
        """Test get_all_slots with valid combat style."""
        result = get_all_slots("melee")
        assert isinstance(result, list)
        assert all(isinstance(slot, str) for slot in result)

    def test_get_all_slots_invalid_style(self):
        """Test get_all_slots with invalid style."""
        result = get_all_slots("invalid_style")
        assert result == []

    def test_get_all_slots_all_styles(self):
        """Test get_all_slots for all combat styles."""
        for style in ["melee", "ranged", "magic"]:
            result = get_all_slots(style)
            assert isinstance(result, list)


class TestWikiProgressionData:
    """Test WIKI_PROGRESSION data structure."""

    def test_wiki_progression_is_dict(self):
        """Test that WIKI_PROGRESSION is a dictionary."""
        assert isinstance(WIKI_PROGRESSION, dict)

    def test_wiki_progression_has_combat_styles(self):
        """Test that WIKI_PROGRESSION has expected combat styles."""
        expected_styles = ["melee", "ranged", "magic"]
        for style in expected_styles:
            assert style in WIKI_PROGRESSION

    def test_wiki_progression_structure(self):
        """Test that WIKI_PROGRESSION has correct structure."""
        for style_data in WIKI_PROGRESSION.values():
            assert isinstance(style_data, dict)
            # Each style should have slots as keys
            for slot, tiers in style_data.items():
                assert isinstance(slot, str)
                assert isinstance(tiers, list)
