"""Unit and integration tests for health check endpoint."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlmodel import Session
from fastapi import HTTPException

from backend.main import app
from backend.api.v1.health import health_check, HealthCheckResponse


client = TestClient(app)


@pytest.mark.unit
class TestHealthCheckUnit:
    """Unit tests for health_check function."""

    @pytest.mark.asyncio
    async def test_health_check_database_ok(self):
        """Test health check when database is healthy."""
        mock_session = MagicMock(spec=Session)
        mock_session.exec.return_value.one.return_value = 1

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_client.get = AsyncMock(return_value=mock_response)

            result = await health_check(mock_session)

            assert isinstance(result, HealthCheckResponse)
            assert result.status == "healthy"
            assert result.database == "ok"
            assert result.external_api == "ok"
            assert result.version == "1.0.0"

    @pytest.mark.asyncio
    async def test_health_check_database_error(self):
        """Test health check when database connection fails."""
        mock_session = MagicMock(spec=Session)
        mock_session.exec.side_effect = Exception("Database connection failed")

        with pytest.raises(HTTPException) as exc_info:
            await health_check(mock_session)

        assert exc_info.value.status_code == 503
        assert "Database connection failed" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_health_check_external_api_unavailable(self):
        """Test health check when external API is unavailable."""
        mock_session = MagicMock(spec=Session)
        mock_session.exec.return_value.one.return_value = 1

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            mock_client.get = AsyncMock(side_effect=Exception("Connection timeout"))

            result = await health_check(mock_session)

            assert result.status == "healthy"  # Still healthy, external API is non-critical
            assert result.database == "ok"
            assert result.external_api == "unavailable"

    @pytest.mark.asyncio
    async def test_health_check_external_api_degraded(self):
        """Test health check when external API returns non-200 status."""
        mock_session = MagicMock(spec=Session)
        mock_session.exec.return_value.one.return_value = 1

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_client.get = AsyncMock(return_value=mock_response)

            result = await health_check(mock_session)

            assert result.status == "healthy"
            assert result.database == "ok"
            assert result.external_api == "degraded"


@pytest.mark.integration
class TestHealthCheckIntegration:
    """Integration tests for health check endpoint."""

    @patch("httpx.AsyncClient")
    def test_health_endpoint_success(self, mock_client_class, client: TestClient, session: Session):
        """Test /api/v1/health endpoint returns correct structure."""
        # Mock external API call to avoid network dependency in tests
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "database" in data
        assert "external_api" in data
        assert "version" in data

        assert data["status"] in ("healthy", "unhealthy")
        assert data["database"] in ("ok", "error")
        assert data["version"] == "1.0.0"

    @patch("httpx.AsyncClient")
    def test_health_endpoint_database_check(self, mock_client_class, client: TestClient, session: Session):
        """Test health endpoint checks database connectivity."""
        # Mock external API call
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Database should be ok if test database is working
        assert data["database"] == "ok"

    @patch("httpx.AsyncClient")
    def test_health_endpoint_external_api_check(self, mock_client_class, client: TestClient, session: Session):
        """Test health endpoint checks external API availability."""
        # Mock external API call to return unavailable
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.get = AsyncMock(side_effect=Exception("Connection timeout"))

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # External API status should be present (ok, degraded, or unavailable)
        assert data["external_api"] in ("ok", "degraded", "unavailable")


@pytest.mark.e2e
class TestHealthCheckE2E:
    """E2E tests for health check endpoint."""

    @patch("httpx.AsyncClient")
    def test_api_v1_health_endpoint(self, mock_client_class, client: TestClient, session: Session):
        """Test /api/v1/health endpoint returns correct response."""
        # Mock external API call to prevent hangs/timeouts
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Verify response structure matches HealthCheckResponse schema
        assert "status" in data
        assert "database" in data
        assert "external_api" in data
        assert "version" in data

        # Verify response values
        assert isinstance(data["status"], str)
        assert isinstance(data["database"], str)
        assert isinstance(data["version"], str)
        assert data["version"] == "1.0.0"

    @patch("httpx.AsyncClient")
    def test_health_endpoint_monitoring_ready(self, mock_client_class, client: TestClient, session: Session):
        """Test health endpoint is suitable for monitoring/load balancers."""
        # Mock external API call to prevent hangs/timeouts
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)

        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Monitoring systems can check database status
        assert "database" in data
        assert data["database"] in ("ok", "error")

        # If database is error, should return 503 (tested in unit tests)
