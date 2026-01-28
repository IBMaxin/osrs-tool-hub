"""Contract tests for gear API endpoints.

These tests verify that:
1. Response models match actual responses (golden path)
2. Error responses match ErrorResponse schema (validation failures)
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

from backend.api.v1.schemas import ErrorResponse


@pytest.mark.unit
class TestGearProgressionContract:
    """Contract tests for /api/v1/gear/progression/{combat_style} endpoint."""

    def test_get_progression_golden_path_response_schema(self, client: TestClient):
        """Test that GET /api/v1/gear/progression/{combat_style} returns valid schema."""
        # Mock the service to return valid data
        mock_progression_data = {
            "head": [
                {
                    "tier": "low",
                    "items": [
                        {
                            "id": 1139,
                            "name": "Iron full helm",
                            "icon_url": "https://example.com/icon.png",
                            "price": 1000,
                            "wiki_url": "https://oldschool.runescape.wiki/w/Iron_full_helm",
                        }
                    ],
                }
            ],
            "cape": [],
        }

        with patch("backend.api.v1.gear.routes.progression.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_wiki_progression.return_value = mock_progression_data

            response = client.get("/api/v1/gear/progression/melee")

            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "combat_style" in data
            assert "slots" in data
            assert data["combat_style"] == "melee"
            assert isinstance(data["slots"], dict)

    def test_get_progression_validation_error_schema(self, client: TestClient):
        """Test that invalid combat style returns ErrorResponse schema."""
        response = client.get("/api/v1/gear/progression/invalid_style")

        assert response.status_code == 400
        data = response.json()

        # Verify ErrorResponse schema
        try:
            ErrorResponse(**data)
        except ValidationError as e:
            pytest.fail(f"Error response does not match ErrorResponse schema: {e}")

        # Verify error structure
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert data["error"]["code"].startswith("HTTP_")
        assert (
            "invalid" in data["error"]["message"].lower()
            or "combat" in data["error"]["message"].lower()
        )

    def test_get_progression_service_error_schema(self, client: TestClient):
        """Test that service errors return ErrorResponse schema."""
        with patch("backend.api.v1.gear.routes.progression.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_wiki_progression.side_effect = Exception("Service error")

            response = client.get("/api/v1/gear/progression/melee")

            assert response.status_code == 500
            data = response.json()

            # Verify ErrorResponse schema
            try:
                ErrorResponse(**data)
            except ValidationError as e:
                pytest.fail(f"Error response does not match ErrorResponse schema: {e}")

            assert "error" in data
            assert data["error"]["code"] == "HTTP_500"
