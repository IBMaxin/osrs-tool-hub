"""Unit tests for wiki_guide_verification module."""

import pytest

from backend.services.wiki_guide_verification import (
    WIKI_GUIDE_SLOT_ORDER,
    WIKI_GUIDE_STYLES,
    validate_guide,
    validate_slot_order,
    validate_guide_root,
    validate_tier,
    validate_game_stage,
    validate_bonus_row,
    WikiGuideValidationError,
)


class TestValidateSlotOrder:
    """Tests for validate_slot_order function."""

    def test_valid_slot_order(self) -> None:
        """Test that canonical slot order passes validation."""
        validate_slot_order(WIKI_GUIDE_SLOT_ORDER)  # Should not raise

    def test_invalid_wrong_order(self) -> None:
        """Test that wrong order raises error."""
        wrong_order = ["head", "cape", "weapon", "neck", "ammo", "body", "shield", "legs", "hands", "feet", "ring"]
        with pytest.raises(WikiGuideValidationError):
            validate_slot_order(wrong_order)

    def test_invalid_wrong_length(self) -> None:
        """Test that wrong length raises error."""
        short_order = ["head", "cape", "neck"]
        with pytest.raises(WikiGuideValidationError):
            validate_slot_order(short_order)

    def test_invalid_not_list(self) -> None:
        """Test that non-list input raises error."""
        with pytest.raises(WikiGuideValidationError):
            validate_slot_order("head,cape,neck")  # type: ignore[arg-type]


class TestValidateGuideRoot:
    """Tests for validate_guide_root function."""

    def test_valid_root(self) -> None:
        """Test that valid root structure passes."""
        data = {
            "style": "magic",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        validate_guide_root(data)  # Should not raise

    def test_missing_style(self) -> None:
        """Test that missing style raises error."""
        data = {
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key: style"):
            validate_guide_root(data)

    def test_missing_slot_order(self) -> None:
        """Test that missing slot_order raises error."""
        data = {
            "style": "magic",
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key: slot_order"):
            validate_guide_root(data)

    def test_invalid_style(self) -> None:
        """Test that invalid style raises error."""
        data = {
            "style": "invalid_style",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        with pytest.raises(WikiGuideValidationError, match="Invalid style"):
            validate_guide_root(data)

    def test_invalid_slot_order(self) -> None:
        """Test that invalid slot_order raises error."""
        data = {
            "style": "magic",
            "slot_order": ["head", "cape"],
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        with pytest.raises(WikiGuideValidationError):
            validate_guide_root(data)


class TestValidateTier:
    """Tests for validate_tier function."""

    def test_valid_tier(self) -> None:
        """Test that valid tier passes."""
        tier = {
            "label": "Level 1",
            "total_cost": 1000,
            "slots": {slot: None for slot in WIKI_GUIDE_SLOT_ORDER},
        }
        validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)  # Should not raise

    def test_tier_with_icons(self) -> None:
        """Test tier with icon_override values."""
        tier = {
            "label": "Level 50",
            "total_cost": 50000,
            "slots": {
                "head": {"name": "Helm of neitiznot", "icon_override": "Helm_of_neitiznot"},
                "cape": {"name": "Fire cape"},
                "neck": None,
                "ammo": None,
                "weapon": {"name": "Abyssal whip"},
                "body": {"name": "Rune platebody"},
                "shield": {"name": "Rune defender"},
                "legs": {"name": "Rune platelegs"},
                "hands": {"name": "Rune gloves"},
                "feet": {"name": "Rune boots"},
                "ring": None,
            },
        }
        validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)  # Should not raise

    def test_missing_label(self) -> None:
        """Test that missing label raises error."""
        tier = {
            "total_cost": 1000,
            "slots": {slot: None for slot in WIKI_GUIDE_SLOT_ORDER},
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key in tier: label"):
            validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)

    def test_missing_slots(self) -> None:
        """Test that missing slots raises error."""
        tier = {
            "label": "Level 1",
            "total_cost": 1000,
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key in tier: slots"):
            validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)

    def test_missing_slot_in_tier(self) -> None:
        """Test that missing slot in tier raises error."""
        slots = {slot: None for slot in WIKI_GUIDE_SLOT_ORDER[:-1]}  # Missing 'ring'
        tier = {
            "label": "Level 1",
            "total_cost": 1000,
            "slots": slots,
        }
        with pytest.raises(WikiGuideValidationError, match="Tier missing slot 'ring'"):
            validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)

    def test_invalid_slot_value(self) -> None:
        """Test that invalid slot value raises error."""
        slots = {slot: None for slot in WIKI_GUIDE_SLOT_ORDER}
        slots["head"] = "Not a dict"  # Invalid
        tier = {
            "label": "Level 1",
            "total_cost": 1000,
            "slots": slots,
        }
        with pytest.raises(WikiGuideValidationError, match="Slot value must be null or dict"):
            validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)

    def test_slot_missing_name(self) -> None:
        """Test that slot missing 'name' raises error."""
        slots = {slot: None for slot in WIKI_GUIDE_SLOT_ORDER}
        slots["head"] = {"icon_override": "Some item"}  # Missing 'name'
        tier = {
            "label": "Level 1",
            "total_cost": 1000,
            "slots": slots,
        }
        with pytest.raises(WikiGuideValidationError, match="Slot value missing required 'name' key"):
            validate_tier(tier, WIKI_GUIDE_SLOT_ORDER)


class TestValidateGameStage:
    """Tests for validate_game_stage function."""

    def test_valid_stage(self) -> None:
        """Test that valid stage passes."""
        stage = {
            "id": "early_game",
            "title": "Early Game",
            "tiers": [
                {
                    "label": "Level 1",
                    "total_cost": 1000,
                    "slots": {slot: None for slot in WIKI_GUIDE_SLOT_ORDER},
                }
            ],
            "content_specific": [],
        }
        validate_game_stage(stage, WIKI_GUIDE_SLOT_ORDER)  # Should not raise

    def test_missing_id(self) -> None:
        """Test that missing id raises error."""
        stage = {
            "title": "Early Game",
            "tiers": [],
            "content_specific": [],
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key in stage: id"):
            validate_game_stage(stage, WIKI_GUIDE_SLOT_ORDER)

    def test_empty_tiers_allowed(self) -> None:
        """Test that empty tiers list is valid."""
        stage = {
            "id": "empty_stage",
            "title": "Empty Stage",
            "tiers": [],
            "content_specific": [],
        }
        validate_game_stage(stage, WIKI_GUIDE_SLOT_ORDER)  # Should not raise

    def test_invalid_tier_in_stage(self) -> None:
        """Test that invalid tier in stage raises error."""
        stage = {
            "id": "early_game",
            "title": "Early Game",
            "tiers": [
                {
                    "label": "Level 1",
                    # Missing total_cost and slots
                }
            ],
            "content_specific": [],
        }
        with pytest.raises(WikiGuideValidationError):
            validate_game_stage(stage, WIKI_GUIDE_SLOT_ORDER)


class TestValidateBonusRow:
    """Tests for validate_bonus_row function."""

    def test_valid_row(self) -> None:
        """Test that valid bonus row passes."""
        row = {
            "item": "Abyssal whip",
            "bonus": "+15 Slash",
            "cost": 120000,
            "delta": "+5",
            "cost_per_delta": "24000",
        }
        validate_bonus_row(row)  # Should not raise

    def test_minimal_row(self) -> None:
        """Test that minimal valid row passes."""
        row = {
            "item": "Some item",
            "bonus": "+10",
        }
        validate_bonus_row(row)  # Should not raise

    def test_missing_item(self) -> None:
        """Test that missing item raises error."""
        row = {
            "bonus": "+10",
        }
        with pytest.raises(WikiGuideValidationError, match="Bonus row missing required 'item' key"):
            validate_bonus_row(row)

    def test_missing_bonus(self) -> None:
        """Test that missing bonus raises error."""
        row = {
            "item": "Some item",
        }
        with pytest.raises(WikiGuideValidationError, match="Bonus row missing required 'bonus' key"):
            validate_bonus_row(row)

    def test_invalid_cost(self) -> None:
        """Test that invalid cost raises error."""
        row = {
            "item": "Some item",
            "bonus": "+10",
            "cost": "not a number",
        }
        with pytest.raises(WikiGuideValidationError, match="bonus row 'cost' must be a number"):
            validate_bonus_row(row)


class TestValidateGuide:
    """Tests for validate_guide function."""

    def test_valid_minimal_guide(self) -> None:
        """Test that minimal valid guide passes."""
        guide = {
            "style": "magic",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            "bonus_table": [],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        validate_guide(guide)  # Should not raise

    def test_valid_full_guide(self) -> None:
        """Test that full valid guide passes."""
        guide = {
            "style": "magic",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [
                {
                    "id": "early_game",
                    "title": "Early Game",
                    "tiers": [
                        {
                            "label": "Level 1",
                            "total_cost": 9135,
                            "slots": {
                                "head": {"name": "Blue wizard hat"},
                                "cape": {"name": "Black cape"},
                                "neck": {"name": "Amulet of magic"},
                                "ammo": None,
                                "weapon": {"name": "Staff of air"},
                                "body": {"name": "Blue wizard robe"},
                                "shield": None,
                                "legs": {"name": "Zamorak monk bottom"},
                                "hands": {"name": "Leather gloves"},
                                "feet": {"name": "Leather boots"},
                                "ring": None,
                            },
                        }
                    ],
                    "content_specific": [],
                }
            ],
            "bonus_table": [
                {"item": "Staff of fire", "bonus": "+5 Magic dmg", "cost": 300},
            ],
            "cost_per_hour_label": "Cost (Runes, 1 Hour)",
        }
        validate_guide(guide)  # Should not raise

    def test_missing_top_level_key(self) -> None:
        """Test that missing top-level key raises error."""
        guide = {
            "style": "magic",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            # Missing bonus_table and cost_per_hour_label
        }
        with pytest.raises(WikiGuideValidationError, match="Missing required key"):
            validate_guide(guide)

    def test_invalid_bonus_table_row(self) -> None:
        """Test that invalid bonus table row raises error."""
        guide = {
            "style": "magic",
            "slot_order": WIKI_GUIDE_SLOT_ORDER,
            "game_stages": [],
            "bonus_table": [
                {"bonus": "+10"},  # Missing 'item'
            ],
            "cost_per_hour_label": "Cost (1 Hour)",
        }
        with pytest.raises(WikiGuideValidationError, match="Bonus row missing required 'item' key"):
            validate_guide(guide)


class TestConstants:
    """Tests for module constants."""

    def test_slot_order_length(self) -> None:
        """Test that slot order has expected length."""
        assert len(WIKI_GUIDE_SLOT_ORDER) == 11

    def test_slot_order_values(self) -> None:
        """Test that slot order has expected values."""
        assert WIKI_GUIDE_SLOT_ORDER == [
            "head", "cape", "neck", "ammo", "weapon",
            "body", "shield", "legs", "hands", "feet", "ring"
        ]

    def test_styles_values(self) -> None:
        """Test that styles has expected values."""
        assert WIKI_GUIDE_STYLES == ["magic", "melee", "ranged"]
