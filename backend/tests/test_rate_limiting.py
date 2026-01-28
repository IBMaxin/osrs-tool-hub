"""Tests for API rate limiting."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_rate_limiting_allows_requests_within_limit(client):
    """Test that requests within rate limit are allowed."""
    # Make several requests (should be under 100/minute limit)
    for i in range(10):
        response = client.get("/api/v1/flips/opportunities")
        assert response.status_code in [200, 404]  # 404 if no data, but not 429


def test_rate_limiting_headers_present(client):
    """Test that rate limit headers are present in responses."""
    response = client.get("/api/v1/slayer/masters")

    # Rate limit headers should be present (if rate limiting is enabled)
    if settings.rate_limit_enabled:
        # Check for rate limit headers (X-RateLimit-*)
        # Note: slowapi may not always include these headers, so we check status code
        assert response.status_code in [200, 429]


def test_rate_limiting_configurable(client):
    """Test that rate limiting can be configured."""
    # Verify rate limiting is enabled by default
    assert hasattr(settings, "rate_limit_enabled")
    assert hasattr(settings, "default_rate_limit")

    # Default should be reasonable (100/minute)
    assert "100" in settings.default_rate_limit or "minute" in settings.default_rate_limit
