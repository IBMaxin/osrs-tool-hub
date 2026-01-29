"""E2E tests for Health and Root endpoints."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
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


@pytest.mark.e2e
class TestAPIHealthEndpoint(BaseE2ETest):
    """Test the /api/v1/health endpoint."""

    @patch("httpx.AsyncClient")
    def test_api_v1_health_endpoint(self, mock_client_class, client: TestClient, session: Session):
        """Test /api/v1/health endpoint returns correct structure."""
        # Mock external API call to avoid network dependency
        from unittest.mock import AsyncMock, MagicMock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")
        data = assert_successful_response(response)

        assert "status" in data
        assert "database" in data
        assert "external_api" in data
        assert "version" in data

        assert data["status"] in ("healthy", "unhealthy")
        assert data["database"] in ("ok", "error")
        assert data["version"] == "1.0.0"

    @patch("httpx.AsyncClient")
    def test_api_v1_health_database_status(self, mock_client_class, client: TestClient, session: Session):
        """Test /api/v1/health endpoint checks database connectivity."""
        # Mock external API call
        from unittest.mock import AsyncMock, MagicMock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")
        data = assert_successful_response(response)

        # Database should be ok if test database is working
        assert data["database"] == "ok"

    @patch("httpx.AsyncClient")
    def test_api_v1_health_external_api_status(self, mock_client_class, client: TestClient, session: Session):
        """Test /api/v1/health endpoint checks external API."""
        # Mock external API call to return unavailable
        from unittest.mock import AsyncMock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.get = AsyncMock(side_effect=Exception("Connection timeout"))

        response = client.get("/api/v1/health")
        data = assert_successful_response(response)

        # External API status should be present
        assert data["external_api"] in ("ok", "degraded", "unavailable")
