"""E2E tests for Gear Progression endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


@pytest.mark.e2e


class TestGearProgressionEndpoints(BaseE2ETest):
    """Test gear progression endpoints."""
    
    def test_get_progression_melee(self, client: TestClient, session: Session):
        """Test getting melee gear progression."""
        response = client.get("/api/v1/gear/progression/melee")
        data = assert_successful_response(response)
        
        assert "combat_style" in data
        assert data["combat_style"] == "melee"
        assert "slots" in data
    
    def test_get_progression_ranged(self, client: TestClient, session: Session):
        """Test getting ranged gear progression."""
        response = client.get("/api/v1/gear/progression/ranged")
        data = assert_successful_response(response)
        
        assert data["combat_style"] == "ranged"
        assert "slots" in data
    
    def test_get_progression_magic(self, client: TestClient, session: Session):
        """Test getting magic gear progression."""
        response = client.get("/api/v1/gear/progression/magic")
        data = assert_successful_response(response)
        
        assert data["combat_style"] == "magic"
        assert "slots" in data
    
    def test_get_progression_invalid_style(self, client: TestClient, session: Session):
        """Test getting progression with invalid combat style."""
        response = client.get("/api/v1/gear/progression/invalid")
        assert_error_response(response, 400)
    
    def test_get_slot_progression(self, client: TestClient, session: Session):
        """Test getting progression for a specific slot."""
        response = client.get("/api/v1/gear/progression/melee/head")
        data = assert_successful_response(response)
        
        assert "combat_style" in data
        assert "slot" in data
        assert data["slot"] == "head"
        assert "tiers" in data
    
    def test_get_slot_progression_ranged(self, client: TestClient, session: Session):
        """Test getting ranged slot progression."""
        response = client.get("/api/v1/gear/progression/ranged/weapon")
        data = assert_successful_response(response)
        
        assert data["combat_style"] == "ranged"
        assert data["slot"] == "weapon"
        assert "tiers" in data


class TestGearWikiProgressionEndpoint(BaseE2ETest):
    """Test wiki-style gear progression endpoint."""
    
    def test_get_wiki_progression_melee(self, client: TestClient, session: Session):
        """Test getting wiki-style melee progression."""
        response = client.get("/api/v1/gear/wiki-progression/melee")
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
    
    def test_get_wiki_progression_ranged(self, client: TestClient, session: Session):
        """Test getting wiki-style ranged progression."""
        response = client.get("/api/v1/gear/wiki-progression/ranged")
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
    
    def test_get_wiki_progression_magic(self, client: TestClient, session: Session):
        """Test getting wiki-style magic progression."""
        response = client.get("/api/v1/gear/wiki-progression/magic")
        data = assert_successful_response(response)
        
        assert isinstance(data, dict)
    
    def test_get_wiki_progression_invalid_style(self, client: TestClient, session: Session):
        """Test wiki progression with invalid style."""
        response = client.get("/api/v1/gear/wiki-progression/invalid")
        assert_error_response(response, 400)
