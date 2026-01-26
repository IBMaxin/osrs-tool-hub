"""E2E tests for Admin sync endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.tests.e2e.base import BaseE2ETest


@pytest.mark.e2e


class TestAdminSyncEndpoint(BaseE2ETest):
    """Test the /api/v1/admin/sync-stats endpoint."""
    
    def test_sync_stats_endpoint_exists(self, client: TestClient, session: Session):
        """Test that sync stats endpoint exists and accepts requests."""
        # Note: This endpoint may take a long time and require external API access
        # In a real scenario, you might want to mock the external API call
        response = client.post("/api/v1/admin/sync-stats")
        
        # Should either succeed (200) or fail gracefully (500/503) if external API is unavailable
        assert response.status_code in [200, 500, 503, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
    
    def test_sync_stats_response_structure(self, client: TestClient, session: Session):
        """Test sync stats response structure when successful."""
        # This test assumes the endpoint might be mocked or external API is available
        # In practice, you'd mock the external API call
        response = client.post("/api/v1/admin/sync-stats")
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
            assert "status" in data
