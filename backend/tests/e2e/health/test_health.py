"""E2E tests for Health and Root endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e


class TestRootEndpoint(BaseE2ETest):
    """Test the root endpoint."""
    
    def test_root_endpoint(self, client: TestClient, session: Session):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        data = assert_successful_response(response)
        
        assert "message" in data
        assert "OSRS" in data["message"] or "Tool Hub" in data["message"]


class TestHealthEndpoint(BaseE2ETest):
    """Test the health check endpoint."""
    
    def test_health_endpoint(self, client: TestClient, session: Session):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        data = assert_successful_response(response)
        
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_endpoint_always_available(self, client: TestClient, session: Session):
        """Test health endpoint is always available regardless of database state."""
        # Health should work even with empty database
        response = client.get("/health")
        data = assert_successful_response(response)
        
        assert data["status"] == "healthy"
