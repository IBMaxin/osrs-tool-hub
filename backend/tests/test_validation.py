"""Tests for input validation."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.api.v1.validators import (
    validate_budget,
    validate_roi,
    validate_volume,
    validate_level,
    validate_item_id,
    validate_string_length,
    validate_slot
)

client = TestClient(app)


def test_validate_budget_valid():
    """Test budget validation with valid values."""
    assert validate_budget(None) is None
    assert validate_budget(0) == 0
    assert validate_budget(1000000) == 1000000
    assert validate_budget(2_147_483_647) == 2_147_483_647


def test_validate_budget_invalid():
    """Test budget validation with invalid values."""
    with pytest.raises(Exception):  # HTTPException
        validate_budget(-1)
    
    with pytest.raises(Exception):  # HTTPException
        validate_budget(2_147_483_648)


def test_validate_roi_valid():
    """Test ROI validation with valid values."""
    assert validate_roi(0.0) == 0.0
    assert validate_roi(5.5) == 5.5
    assert validate_roi(10000.0) == 10000.0


def test_validate_roi_invalid():
    """Test ROI validation with invalid values."""
    with pytest.raises(Exception):  # HTTPException
        validate_roi(-1.0)
    
    with pytest.raises(Exception):  # HTTPException
        validate_roi(10001.0)


def test_validate_volume_valid():
    """Test volume validation with valid values."""
    assert validate_volume(0) == 0
    assert validate_volume(1000) == 1000


def test_validate_volume_invalid():
    """Test volume validation with invalid values."""
    with pytest.raises(Exception):  # HTTPException
        validate_volume(-1)


def test_validate_level_valid():
    """Test level validation with valid values."""
    assert validate_level(1) == 1
    assert validate_level(50) == 50
    assert validate_level(99) == 99


def test_validate_level_invalid():
    """Test level validation with invalid values."""
    with pytest.raises(Exception):  # HTTPException
        validate_level(0)
    
    with pytest.raises(Exception):  # HTTPException
        validate_level(100)


def test_validate_slot_valid():
    """Test slot validation with valid values."""
    assert validate_slot("head") == "head"
    assert validate_slot("WEAPON") == "weapon"  # Should lowercase
    assert validate_slot("Two_Handed") == "two_handed"


def test_validate_slot_invalid():
    """Test slot validation with invalid values."""
    with pytest.raises(Exception):  # HTTPException
        validate_slot("invalid_slot")


def test_flip_endpoint_validates_budget():
    """Test that flip endpoint validates budget parameter."""
    # Valid request
    response = client.get("/api/v1/flips/opportunities?max_budget=1000000")
    assert response.status_code in [200, 404]  # 404 if no data
    
    # Invalid budget (negative)
    response = client.get("/api/v1/flips/opportunities?max_budget=-1")
    assert response.status_code == 422  # FastAPI validation error


def test_flip_endpoint_validates_roi():
    """Test that flip endpoint validates ROI parameter."""
    # Invalid ROI (negative)
    response = client.get("/api/v1/flips/opportunities?min_roi=-1")
    assert response.status_code == 422  # FastAPI validation error
    
    # Valid ROI
    response = client.get("/api/v1/flips/opportunities?min_roi=5.0")
    assert response.status_code in [200, 404]


def test_gear_set_creation_validates_name():
    """Test that gear set creation validates name."""
    # Empty name should fail
    response = client.post(
        "/api/v1/gear",
        json={
            "name": "",
            "items": {4151: 1}
        }
    )
    assert response.status_code == 422  # Validation error
    
    # Name too long should fail
    response = client.post(
        "/api/v1/gear",
        json={
            "name": "a" * 201,  # Exceeds max_length=200
            "items": {4151: 1}
        }
    )
    assert response.status_code == 422  # Validation error


def test_gear_set_creation_validates_items():
    """Test that gear set creation validates items."""
    # Empty items should fail
    response = client.post(
        "/api/v1/gear",
        json={
            "name": "Test Set",
            "items": {}
        }
    )
    assert response.status_code == 422  # Validation error
    
    # Invalid quantity should fail
    response = client.post(
        "/api/v1/gear",
        json={
            "name": "Test Set",
            "items": {4151: 0}  # Quantity must be at least 1
        }
    )
    assert response.status_code == 422  # Validation error
