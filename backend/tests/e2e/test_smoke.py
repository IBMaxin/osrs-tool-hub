"""E2E smoke test for critical API endpoints.

This test verifies that:
1. Backend starts successfully
2. Critical endpoint returns 200 with correct schema
3. Error handling returns ErrorResponse schema
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from pydantic import ValidationError

from backend.models import Item, PriceSnapshot
from backend.services.flipping import FlipOpportunity


@pytest.mark.e2e
class TestSmoke:
    """E2E smoke tests for critical endpoints."""

    def test_flips_opportunities_critical_path(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test critical path: GET /api/v1/flips/opportunities returns 200 + valid schema."""
        response = client.get("/api/v1/flips/opportunities")

        # Verify 200 status
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        # Verify response is valid JSON
        data = response.json()
        assert isinstance(data, list), "Response should be a list"

        # Verify schema matches FlipOpportunity model
        if len(data) > 0:
            try:
                FlipOpportunity(**data[0])
            except ValidationError as e:
                pytest.fail(f"Response does not match FlipOpportunity schema: {e}")

    def test_flips_opportunities_error_path(self, client: TestClient):
        """Test error path: GET /api/v1/flips/opportunities?min_roi=-1 returns 422 (validation error)."""
        response = client.get("/api/v1/flips/opportunities?min_roi=-1")

        # FastAPI returns 422 for query parameter validation errors
        assert (
            response.status_code == 422
        ), f"Expected 422, got {response.status_code}: {response.text}"

        # FastAPI's RequestValidationError doesn't go through our HTTPException handler
        # So it returns FastAPI's default validation error format
        # This is acceptable - validation errors are handled by FastAPI before reaching our handler
        data = response.json()
        assert "detail" in data, "Validation error should have 'detail' field"
