"""Tests for gear API schemas and validators."""

import pytest
from pydantic import ValidationError

from backend.api.v1.gear.schemas import (
    GearSetCreate,
    BestLoadoutRequest,
    UpgradePathRequest,
    DPSRequest,
    DPSComparisonRequest,
    LoadoutInput,
    SlayerGearRequest,
)


class TestGearSetCreate:
    """Test GearSetCreate schema."""

    def test_gear_set_create_valid(self):
        """Test GearSetCreate with valid data."""
        data = GearSetCreate(
            name="Test Set",
            items={4151: 1, 314: 100},
            description="Test description",
        )
        assert data.name == "Test Set"
        assert data.items == {4151: 1, 314: 100}

    def test_gear_set_create_empty_name(self):
        """Test GearSetCreate with empty name."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="", items={4151: 1})

    def test_gear_set_create_whitespace_name(self):
        """Test GearSetCreate with whitespace-only name."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="   ", items={4151: 1})

    def test_gear_set_create_empty_items(self):
        """Test GearSetCreate with empty items dict."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items={})

    def test_gear_set_create_too_many_items(self):
        """Test GearSetCreate with too many items."""
        items = {i: 1 for i in range(51)}  # 51 items
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items=items)

    def test_gear_set_create_negative_item_id(self):
        """Test GearSetCreate with negative item ID."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items={-1: 1})

    def test_gear_set_create_zero_quantity(self):
        """Test GearSetCreate with zero quantity."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items={4151: 0})

    def test_gear_set_create_negative_quantity(self):
        """Test GearSetCreate with negative quantity."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items={4151: -1})

    def test_gear_set_create_excessive_quantity(self):
        """Test GearSetCreate with quantity exceeding maximum."""
        with pytest.raises(ValidationError):
            GearSetCreate(name="Test", items={4151: 10001})

    def test_gear_set_create_strips_name_whitespace(self):
        """Test GearSetCreate strips whitespace from name."""
        data = GearSetCreate(name="  Test Set  ", items={4151: 1})
        assert data.name == "Test Set"


class TestBestLoadoutRequest:
    """Test BestLoadoutRequest schema."""

    def test_best_loadout_request_valid(self):
        """Test BestLoadoutRequest with valid data."""
        data = BestLoadoutRequest(
            combat_style="melee",
            budget=1000000,
            stats={"attack": 70, "strength": 70, "defence": 70},
        )
        assert data.combat_style == "melee"

    def test_best_loadout_request_invalid_combat_style(self):
        """Test BestLoadoutRequest with invalid combat style."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="invalid",
                budget=1000000,
                stats={"attack": 70},
            )

    def test_best_loadout_request_case_insensitive_combat_style(self):
        """Test BestLoadoutRequest normalizes combat style case."""
        data = BestLoadoutRequest(
            combat_style="MELEE",
            budget=1000000,
            stats={"attack": 70},
        )
        assert data.combat_style == "melee"

    def test_best_loadout_request_invalid_stat_name(self):
        """Test BestLoadoutRequest with invalid stat name."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="melee",
                budget=1000000,
                stats={"invalid_stat": 70},
            )

    def test_best_loadout_request_stat_below_minimum(self):
        """Test BestLoadoutRequest with stat below 1."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="melee",
                budget=1000000,
                stats={"attack": 0},
            )

    def test_best_loadout_request_stat_above_maximum(self):
        """Test BestLoadoutRequest with stat above 99."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="melee",
                budget=1000000,
                stats={"attack": 100},
            )

    def test_best_loadout_request_invalid_attack_type(self):
        """Test BestLoadoutRequest with invalid attack type."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="melee",
                budget=1000000,
                stats={"attack": 70},
                attack_type="invalid",
            )

    def test_best_loadout_request_valid_attack_types(self):
        """Test BestLoadoutRequest with valid attack types."""
        for attack_type in ["stab", "slash", "crush"]:
            data = BestLoadoutRequest(
                combat_style="melee",
                budget=1000000,
                stats={"attack": 70},
                attack_type=attack_type,
            )
            assert data.attack_type == attack_type

    def test_best_loadout_request_negative_budget(self):
        """Test BestLoadoutRequest with negative budget."""
        with pytest.raises(ValidationError):
            BestLoadoutRequest(
                combat_style="melee",
                budget=-1,
                stats={"attack": 70},
            )


class TestSlayerGearRequest:
    """Test SlayerGearRequest schema."""

    def test_slayer_gear_request_valid(self):
        """Test SlayerGearRequest with valid data."""
        data = SlayerGearRequest(
            task_id=1,
            stats={"attack": 70, "strength": 70, "defence": 70},
            budget=10000000,
        )
        assert data.task_id == 1
        assert data.budget == 10000000

    def test_slayer_gear_request_default_budget(self):
        """Test SlayerGearRequest uses default budget."""
        data = SlayerGearRequest(
            task_id=1,
            stats={"attack": 70},
        )
        assert data.budget == 100_000_000

    def test_slayer_gear_request_invalid_combat_style(self):
        """Test SlayerGearRequest with invalid combat style."""
        with pytest.raises(ValidationError):
            SlayerGearRequest(
                task_id=1,
                stats={"attack": 70},
                combat_style="invalid",
            )

    def test_slayer_gear_request_none_combat_style(self):
        """Test SlayerGearRequest with None combat style."""
        data = SlayerGearRequest(
            task_id=1,
            stats={"attack": 70},
            combat_style=None,
        )
        assert data.combat_style is None

    def test_slayer_gear_request_invalid_stat(self):
        """Test SlayerGearRequest with invalid stat."""
        with pytest.raises(ValidationError):
            SlayerGearRequest(
                task_id=1,
                stats={"invalid": 70},
            )

    def test_slayer_gear_request_stat_out_of_range(self):
        """Test SlayerGearRequest with stat out of range."""
        with pytest.raises(ValidationError):
            SlayerGearRequest(
                task_id=1,
                stats={"attack": 100},
            )


class TestDPSComparisonRequest:
    """Test DPSComparisonRequest schema."""

    def test_dps_comparison_request_valid(self):
        """Test DPSComparisonRequest with valid data."""
        data = DPSComparisonRequest(
            loadouts=[
                LoadoutInput(name="Loadout 1", loadout={"weapon": 4151}),
            ],
            combat_style="melee",
        )
        assert len(data.loadouts) == 1

    def test_dps_comparison_request_empty_loadouts(self):
        """Test DPSComparisonRequest with empty loadouts."""
        with pytest.raises(ValidationError):
            DPSComparisonRequest(
                loadouts=[],
                combat_style="melee",
            )

    def test_dps_comparison_request_too_many_loadouts(self):
        """Test DPSComparisonRequest with too many loadouts."""
        loadouts = [
            LoadoutInput(name=f"Loadout {i}", loadout={"weapon": 4151})
            for i in range(11)
        ]
        with pytest.raises(ValidationError):
            DPSComparisonRequest(
                loadouts=loadouts,
                combat_style="melee",
            )

    def test_dps_comparison_request_invalid_combat_style(self):
        """Test DPSComparisonRequest with invalid combat style."""
        with pytest.raises(ValidationError):
            DPSComparisonRequest(
                loadouts=[LoadoutInput(name="Test", loadout={"weapon": 4151})],
                combat_style="invalid",
            )
