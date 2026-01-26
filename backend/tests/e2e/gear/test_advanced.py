"""E2E tests for advanced Gear endpoints (DPS, loadouts, etc.)."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e


class TestGearPresetEndpoint(BaseE2ETest):
    """Test gear preset loadout endpoint."""
    
    def test_get_preset_loadout(self, client: TestClient, session: Session):
        """Test getting preset loadout for a combat style and tier."""
        response = client.get("/api/v1/gear/preset?combat_style=melee&tier=mid")
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
        # Should have items or loadout information
    
    def test_preset_invalid_style(self, client: TestClient, session: Session):
        """Test preset with invalid combat style."""
        response = client.get("/api/v1/gear/preset?combat_style=invalid&tier=mid")
        assert_error_response(response, 400)


class TestGearBestLoadoutEndpoint(BaseE2ETest):
    """Test best loadout endpoint."""
    
    def test_get_best_loadout(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item]
    ):
        """Test getting best loadout based on budget and stats."""
        payload = {
            "combat_style": "melee",
            "budget": 10000000,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70
            },
            "attack_type": "slash"
        }
        
        response = client.post("/api/v1/gear/best-loadout", json=payload)
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
        # Should have loadout information


class TestGearUpgradePathEndpoint(BaseE2ETest):
    """Test upgrade path endpoint."""
    
    def test_get_upgrade_path(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item]
    ):
        """Test getting upgrade path recommendations."""
        payload = {
            "current_loadout": {"weapon": 4151},  # Abyssal whip
            "combat_style": "melee",
            "budget": 50000000,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70
            },
            "attack_type": "slash"
        }
        
        response = client.post("/api/v1/gear/upgrade-path", json=payload)
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
        # Should have upgrade recommendations


class TestGearDPSEndpoint(BaseE2ETest):
    """Test DPS calculation endpoint."""
    
    def test_calculate_dps(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item]
    ):
        """Test calculating DPS for a loadout."""
        payload = {
            "loadout": {"weapon": 4151},  # Abyssal whip
            "combat_style": "melee",
            "attack_type": "slash",
            "player_stats": {
                "attack": 70,
                "strength": 70
            }
        }
        
        response = client.post("/api/v1/gear/dps", json=payload)
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
        # Should have DPS information
