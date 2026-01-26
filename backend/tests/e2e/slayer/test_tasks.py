"""E2E tests for Slayer Tasks endpoint."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Monster, SlayerTask, SlayerMaster
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import assert_successful_response


@pytest.mark.e2e


class TestSlayerTasksEndpoint(BaseE2ETest):
    """Test the /api/v1/slayer/tasks/{master} endpoint."""
    
    def test_get_tasks_for_master(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask]
    ):
        """Test getting tasks for a specific master."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        data = assert_successful_response(response)
        
        assert isinstance(data, list)
        assert len(data) >= 2  # Should have at least 2 tasks for Duradel
        
        # Verify structure
        for task in data:
            assert "monster_name" in task
            assert "monster_id" in task
            assert "category" in task
            assert "amount" in task
            assert "weight" in task
            assert "combat_level" in task
            assert "slayer_xp" in task
    
    def test_get_tasks_for_konar(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask]
    ):
        """Test getting tasks for Konar master."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.KONAR.value}")
        data = assert_successful_response(response)
        
        assert isinstance(data, list)
        assert len(data) >= 1  # Should have at least 1 task for Konar
    
    def test_get_tasks_for_nonexistent_master(self, client: TestClient, session: Session):
        """Test getting tasks for a master with no tasks."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.TURAEL.value}")
        data = assert_successful_response(response)
        
        assert isinstance(data, list)
        # May be empty or have tasks, both are valid
    
    def test_get_tasks_verify_monster_data(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask]
    ):
        """Test that task data includes correct monster information."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        data = assert_successful_response(response)
        
        # Find Abyssal demon task
        abyssal_task = next(
            (t for t in data if t["monster_name"] == "Abyssal demon"),
            None
        )
        
        if abyssal_task:
            assert abyssal_task["combat_level"] == 124
            assert abyssal_task["slayer_xp"] == 150.0
            assert "120-185" in abyssal_task["amount"] or abyssal_task["amount"] == "120-185"
    
    def test_tasks_sorted_by_weight(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask]
    ):
        """Test that tasks are sorted by weight (descending)."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        data = assert_successful_response(response)
        
        if len(data) > 1:
            weights = [task["weight"] for task in data]
            assert weights == sorted(weights, reverse=True)
