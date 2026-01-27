"""End-to-end tests for gear endpoints."""
import pytest
import json
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, GearSet, PriceSnapshot


class TestGearSetEndpoints:
    """Test gear set CRUD endpoints."""
    
    def test_create_gear_set(self, client: TestClient, session: Session,
                             sample_items: list[Item]):
        """Test creating a new gear set."""
        payload = {
            "name": "Test Melee Set",
            "description": "A test melee gear set",
            "items": {
                4151: 1,  # Abyssal whip
                11802: 1,  # Saradomin godsword
            }
        }
        
        response = client.post("/api/v1/gear", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Melee Set"
        assert data["description"] == "A test melee gear set"
        # JSON serialization converts dict keys to strings, so convert back for comparison
        response_items = {int(k): int(v) for k, v in data["items"].items()}
        assert response_items == payload["items"]
        assert "id" in data
        assert "total_cost" in data
        assert data["total_cost"] > 0
    
    def test_get_all_gear_sets(self, client: TestClient, session: Session,
                                sample_items: list[Item]):
        """Test getting all gear sets."""
        # Create a gear set first
        payload = {
            "name": "Test Set 1",
            "items": {4151: 1}
        }
        client.post("/api/v1/gear", json=payload)
        
        # Create another
        payload2 = {
            "name": "Test Set 2",
            "items": {11802: 1}
        }
        client.post("/api/v1/gear", json=payload2)
        
        # Get all
        response = client.get("/api/v1/gear")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        
        # Verify structure
        for gear_set in data:
            assert "id" in gear_set
            assert "name" in gear_set
            assert "items" in gear_set
            assert "total_cost" in gear_set
    
    def test_get_gear_set_by_id(self, client: TestClient, session: Session,
                                sample_items: list[Item]):
        """Test getting a specific gear set by ID."""
        # Create a gear set
        payload = {
            "name": "Test Set",
            "items": {4151: 1}
        }
        create_response = client.post("/api/v1/gear", json=payload)
        assert create_response.status_code == 201
        gear_set_id = create_response.json()["id"]
        
        # Get by ID
        response = client.get(f"/api/v1/gear/{gear_set_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == gear_set_id
        assert data["name"] == "Test Set"
    
    def test_get_nonexistent_gear_set(self, client: TestClient, session: Session):
        """Test getting a gear set that doesn't exist."""
        response = client.get("/api/v1/gear/99999")
        
        assert response.status_code == 404
    
    def test_delete_gear_set(self, client: TestClient, session: Session,
                             sample_items: list[Item]):
        """Test deleting a gear set."""
        # Create a gear set
        payload = {
            "name": "Test Set to Delete",
            "items": {4151: 1}
        }
        create_response = client.post("/api/v1/gear", json=payload)
        gear_set_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/api/v1/gear/{gear_set_id}")
        
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/api/v1/gear/{gear_set_id}")
        assert get_response.status_code == 404
    
    def test_gear_set_total_cost_calculation(self, client: TestClient, session: Session,
                                            sample_items: list[Item],
                                            sample_price_snapshots: list[PriceSnapshot]):
        """Test that gear set total cost is calculated correctly."""
        payload = {
            "name": "Cost Test Set",
            "items": {
                4151: 1,  # Abyssal whip: 1,400,000
                11802: 1,  # SGS: 50,000,000
            }
        }
        
        response = client.post("/api/v1/gear", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        
        # Total should be sum of item prices
        expected_cost = 1_400_000 + 50_000_000
        assert data["total_cost"] == expected_cost


class TestGearSuggestionsEndpoint:
    """Test gear suggestion endpoints."""
    
    def test_get_gear_suggestions(self, client: TestClient, session: Session,
                                  sample_items: list[Item]):
        """Test getting gear suggestions for a slot."""
        response = client.get(
            "/api/v1/gear/suggestions?"
            "slot=weapon&"
            "style=melee&"
            "defence_level=99"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_gear_suggestions_with_budget(self, client: TestClient, session: Session,
                                              sample_items: list[Item],
                                              sample_price_snapshots: list[PriceSnapshot]):
        """Test gear suggestions with budget filter."""
        response = client.get(
            "/api/v1/gear/suggestions?"
            "slot=weapon&"
            "style=melee&"
            "defence_level=99&"
            "budget=10000000"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All suggestions should be within budget
        for suggestion in data:
            if "price" in suggestion:
                assert suggestion["price"] <= 10000000


class TestGearProgressionEndpoints:
    """Test gear progression endpoints."""
    
    def test_get_progression_melee(self, client: TestClient, session: Session):
        """Test getting melee gear progression."""
        response = client.get("/api/v1/gear/progression/melee")
        
        assert response.status_code == 200
        data = response.json()
        assert "combat_style" in data
        assert data["combat_style"] == "melee"
        assert "slots" in data
    
    def test_get_progression_ranged(self, client: TestClient, session: Session):
        """Test getting ranged gear progression."""
        response = client.get("/api/v1/gear/progression/ranged")
        
        assert response.status_code == 200
        data = response.json()
        assert data["combat_style"] == "ranged"
    
    def test_get_progression_magic(self, client: TestClient, session: Session):
        """Test getting magic gear progression."""
        response = client.get("/api/v1/gear/progression/magic")
        
        assert response.status_code == 200
        data = response.json()
        assert data["combat_style"] == "magic"
    
    def test_get_progression_invalid_style(self, client: TestClient, session: Session):
        """Test getting progression with invalid combat style."""
        response = client.get("/api/v1/gear/progression/invalid")
        
        assert response.status_code == 400
    
    def test_get_slot_progression(self, client: TestClient, session: Session):
        """Test getting progression for a specific slot."""
        response = client.get("/api/v1/gear/progression/melee/head")
        
        assert response.status_code == 200
        data = response.json()
        assert "combat_style" in data
        assert "slot" in data
        assert data["slot"] == "head"
        assert "tiers" in data


class TestGearWikiProgressionEndpoint:
    """Test wiki-style gear progression endpoint."""
    
    def test_get_wiki_progression_melee(self, client: TestClient, session: Session):
        """Test getting wiki-style melee progression."""
        response = client.get("/api/v1/gear/wiki-progression/melee")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_wiki_progression_invalid_style(self, client: TestClient, session: Session):
        """Test wiki progression with invalid style."""
        response = client.get("/api/v1/gear/wiki-progression/invalid")
        
        assert response.status_code == 400
