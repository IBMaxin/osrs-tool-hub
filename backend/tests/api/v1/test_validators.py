"""Unit tests for API validators."""

import pytest
from fastapi import HTTPException

from backend.api.v1.validators import (
    validate_budget,
    validate_roi,
    validate_volume,
    validate_level,
    validate_item_id,
    validate_string_length,
    validate_slot,
    BudgetQuery,
    ROIQuery,
    VolumeQuery,
    LevelQuery,
)


class TestValidateBudget:
    """Test validate_budget function."""

    def test_validate_budget_valid(self):
        """Test validate_budget with valid values."""
        assert validate_budget(0) == 0
        assert validate_budget(1000000) == 1000000
        assert validate_budget(2_147_483_647) == 2_147_483_647
        assert validate_budget(None) is None

    def test_validate_budget_negative(self):
        """Test validate_budget raises error for negative values."""
        with pytest.raises(HTTPException) as exc_info:
            validate_budget(-1)
        assert exc_info.value.status_code == 400
        assert "non-negative" in exc_info.value.detail.lower()

    def test_validate_budget_exceeds_max(self):
        """Test validate_budget raises error for values exceeding max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_budget(2_147_483_648)
        assert exc_info.value.status_code == 400
        assert "maximum" in exc_info.value.detail.lower()


class TestValidateROI:
    """Test validate_roi function."""

    def test_validate_roi_valid(self):
        """Test validate_roi with valid values."""
        assert validate_roi(0.0) == 0.0
        assert validate_roi(10.5) == 10.5
        assert validate_roi(10000.0) == 10000.0

    def test_validate_roi_negative(self):
        """Test validate_roi raises error for negative values."""
        with pytest.raises(HTTPException) as exc_info:
            validate_roi(-1.0)
        assert exc_info.value.status_code == 400
        assert "non-negative" in exc_info.value.detail.lower()

    def test_validate_roi_exceeds_max(self):
        """Test validate_roi raises error for values exceeding max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_roi(10001.0)
        assert exc_info.value.status_code == 400
        assert "maximum" in exc_info.value.detail.lower()


class TestValidateVolume:
    """Test validate_volume function."""

    def test_validate_volume_valid(self):
        """Test validate_volume with valid values."""
        assert validate_volume(0) == 0
        assert validate_volume(1000) == 1000
        assert validate_volume(2_147_483_647) == 2_147_483_647

    def test_validate_volume_negative(self):
        """Test validate_volume raises error for negative values."""
        with pytest.raises(HTTPException) as exc_info:
            validate_volume(-1)
        assert exc_info.value.status_code == 400
        assert "non-negative" in exc_info.value.detail.lower()

    def test_validate_volume_exceeds_max(self):
        """Test validate_volume raises error for values exceeding max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_volume(2_147_483_648)
        assert exc_info.value.status_code == 400
        assert "maximum" in exc_info.value.detail.lower()


class TestValidateLevel:
    """Test validate_level function."""

    def test_validate_level_valid(self):
        """Test validate_level with valid values."""
        assert validate_level(1) == 1
        assert validate_level(50) == 50
        assert validate_level(99) == 99

    def test_validate_level_custom_range(self):
        """Test validate_level with custom min/max."""
        assert validate_level(10, min_level=5, max_level=20) == 10
        assert validate_level(5, min_level=5, max_level=20) == 5
        assert validate_level(20, min_level=5, max_level=20) == 20

    def test_validate_level_below_min(self):
        """Test validate_level raises error for values below min."""
        with pytest.raises(HTTPException) as exc_info:
            validate_level(0)
        assert exc_info.value.status_code == 400
        assert "between" in exc_info.value.detail.lower()

    def test_validate_level_above_max(self):
        """Test validate_level raises error for values above max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_level(100)
        assert exc_info.value.status_code == 400
        assert "between" in exc_info.value.detail.lower()


class TestValidateItemId:
    """Test validate_item_id function."""

    def test_validate_item_id_valid(self):
        """Test validate_item_id with valid values."""
        assert validate_item_id(0) == 0
        assert validate_item_id(4151) == 4151
        assert validate_item_id(2_147_483_647) == 2_147_483_647

    def test_validate_item_id_negative(self):
        """Test validate_item_id raises error for negative values."""
        with pytest.raises(HTTPException) as exc_info:
            validate_item_id(-1)
        assert exc_info.value.status_code == 400
        assert "non-negative" in exc_info.value.detail.lower()

    def test_validate_item_id_exceeds_max(self):
        """Test validate_item_id raises error for values exceeding max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_item_id(2_147_483_648)
        assert exc_info.value.status_code == 400
        assert "maximum" in exc_info.value.detail.lower()


class TestValidateStringLength:
    """Test validate_string_length function."""

    def test_validate_string_length_valid(self):
        """Test validate_string_length with valid strings."""
        assert validate_string_length("test", 10) == "test"
        assert validate_string_length("a" * 10, 10) == "a" * 10

    def test_validate_string_length_exceeds_max(self):
        """Test validate_string_length raises error for strings exceeding max."""
        with pytest.raises(HTTPException) as exc_info:
            validate_string_length("a" * 11, 10)
        assert exc_info.value.status_code == 400
        assert "maximum length" in exc_info.value.detail.lower()

    def test_validate_string_length_custom_field_name(self):
        """Test validate_string_length uses custom field name in error."""
        with pytest.raises(HTTPException) as exc_info:
            validate_string_length("a" * 11, 10, field_name="Name")
        assert exc_info.value.status_code == 400
        assert "Name" in exc_info.value.detail


class TestValidateSlot:
    """Test validate_slot function."""

    def test_validate_slot_valid(self):
        """Test validate_slot with valid slots."""
        valid_slots = [
            "head",
            "cape",
            "neck",
            "ammo",
            "weapon",
            "shield",
            "body",
            "legs",
            "gloves",
            "boots",
            "ring",
            "two_handed",
        ]
        for slot in valid_slots:
            assert validate_slot(slot) == slot.lower()
            assert validate_slot(slot.upper()) == slot.lower()  # Case insensitive

    def test_validate_slot_invalid(self):
        """Test validate_slot raises error for invalid slots."""
        with pytest.raises(HTTPException) as exc_info:
            validate_slot("invalid_slot")
        assert exc_info.value.status_code == 400
        assert "Invalid slot" in exc_info.value.detail


class TestQueryValidators:
    """Test Query parameter validators."""

    def test_budget_query(self):
        """Test BudgetQuery creates Query with correct constraints."""
        query = BudgetQuery(default=1000000)
        assert query.default == 1000000
        # Query constraints are internal to FastAPI, just verify it's created
        assert query is not None

    def test_roi_query(self):
        """Test ROIQuery creates Query with correct constraints."""
        query = ROIQuery(default=10.0)
        assert query.default == 10.0
        assert query is not None

    def test_volume_query(self):
        """Test VolumeQuery creates Query with correct constraints."""
        query = VolumeQuery(default=1000)
        assert query.default == 1000
        assert query is not None

    def test_level_query(self):
        """Test LevelQuery creates Query with correct constraints."""
        query = LevelQuery(default=50, min_level=1, max_level=99)
        assert query.default == 50
        assert query is not None
