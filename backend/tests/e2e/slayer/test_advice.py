"""E2E tests for Slayer Advice endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Monster, SlayerTask, SlayerMaster
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import (
    assert_successful_response,
    assert_error_response,
    get_task_id_from_response,
)


@pytest.mark.e2e
class TestSlayerAdviceEndpoint(BaseE2ETest):
    """Test the /api/v1/slayer/advice/{task_id} endpoint."""

    def test_get_task_advice(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test getting advice for a task."""
        task_id = get_task_id_from_response(client, SlayerMaster.DURADEL)

        if task_id:
            response = client.get(f"/api/v1/slayer/advice/{task_id}")
            data = assert_successful_response(response)

            assert "recommendation" in data
            assert data["recommendation"] in ["DO", "SKIP", "BLOCK"]
            assert "task" in data
            assert "reason" in data

    def test_get_advice_for_nonexistent_task(self, client: TestClient, session: Session):
        """Test getting advice for a task that doesn't exist."""
        response = client.get("/api/v1/slayer/advice/99999")
        assert_error_response(response, 404)

    def test_get_advice_returns_valid_recommendation(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test that advice returns a valid recommendation."""
        task_id = get_task_id_from_response(client, SlayerMaster.DURADEL)

        if task_id:
            response = client.get(f"/api/v1/slayer/advice/{task_id}")
            data = assert_successful_response(response)

            # Recommendation should be one of the valid options
            valid_recommendations = ["DO", "SKIP", "BLOCK"]
            assert data["recommendation"] in valid_recommendations

    def test_advice_includes_task_details(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test that advice response includes task details."""
        task_id = get_task_id_from_response(client, SlayerMaster.DURADEL)

        if task_id:
            response = client.get(f"/api/v1/slayer/advice/{task_id}")
            data = assert_successful_response(response)

            assert "task" in data
            task_info = data["task"]
            # Task can be a string or dict
            if isinstance(task_info, dict):
                assert "monster_name" in task_info or "name" in task_info
            else:
                assert isinstance(task_info, str)
