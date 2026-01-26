"""E2E tests for Slayer Masters endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.tests.e2e.base import BaseE2ETest


@pytest.mark.e2e


class TestSlayerMastersEndpoint(BaseE2ETest):
    """Test the /api/v1/slayer/masters endpoint."""
    
    def test_get_slayer_masters(self, client: TestClient, session: Session):
        """Test getting list of slayer masters."""
        response = client.get("/api/v1/slayer/masters")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check that expected masters are present
        master_names = [m.get("name") or m for m in data]
        assert any("Duradel" in str(m) or "Konar" in str(m) for m in master_names)
    
    def test_masters_response_structure(self, client: TestClient, session: Session):
        """Test that masters response has correct structure."""
        response = client.get("/api/v1/slayer/masters")
        
        assert response.status_code == 200
        data = response.json()
        
        # Each master should have identifiable fields
        for master in data:
            assert master is not None
            # Master can be a dict with name or just a string
            if isinstance(master, dict):
                assert "name" in master or "value" in master
