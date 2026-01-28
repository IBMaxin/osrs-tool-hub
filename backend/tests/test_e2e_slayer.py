"""End-to-end tests for slayer endpoints."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Monster, SlayerTask, SlayerMaster


class TestSlayerMastersEndpoint:
    """Test the /api/v1/slayer/masters endpoint."""

    def test_get_slayer_masters(self, client: TestClient, session: Session):
        """Test getting list of slayer masters."""
        response = client.get("/api/v1/slayer/masters")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Check that expected masters are present
        # Response is a list of strings (master names)
        master_names = [m if isinstance(m, str) else m.get("name", "") for m in data]
        assert "Duradel" in master_names or "Konar" in master_names


class TestSlayerTasksEndpoint:
    """Test the /api/v1/slayer/tasks/{master} endpoint."""

    def test_get_tasks_for_master(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test getting tasks for a specific master."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")

        assert response.status_code == 200
        data = response.json()
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
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test getting tasks for Konar master."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.KONAR.value}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Should have at least 1 task for Konar
        assert len(data) >= 1

    def test_get_tasks_for_nonexistent_master(self, client: TestClient, session: Session):
        """Test getting tasks for a master with no tasks."""
        # Use a master that doesn't have tasks in our test data
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.TURAEL.value}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_tasks_verify_monster_data(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test that task data includes correct monster information."""
        response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")

        assert response.status_code == 200
        data = response.json()

        # Find Abyssal demon task
        abyssal_task = next((t for t in data if t["monster_name"] == "Abyssal demon"), None)

        if abyssal_task:
            assert abyssal_task["combat_level"] == 124
            assert abyssal_task["slayer_xp"] == 150.0
            assert "120-185" in abyssal_task["amount"] or abyssal_task["amount"] == "120-185"


class TestSlayerAdviceEndpoint:
    """Test the /api/v1/slayer/advice/{task_id} endpoint."""

    def test_get_task_advice(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test getting advice for a task."""
        # Get a task ID from the tasks endpoint
        tasks_response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        assert tasks_response.status_code == 200
        tasks = tasks_response.json()

        if len(tasks) > 0:
            task_id = tasks[0]["task_id"]

            response = client.get(f"/api/v1/slayer/advice/{task_id}")

            assert response.status_code == 200
            data = response.json()
            assert "recommendation" in data
            assert data["recommendation"] in ["DO", "SKIP", "BLOCK"]
            assert "task" in data
            assert "reason" in data

    def test_get_advice_for_nonexistent_task(self, client: TestClient, session: Session):
        """Test getting advice for a task that doesn't exist."""
        response = client.get("/api/v1/slayer/advice/99999")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert (
            "error" in data["error"].get("message", "").lower()
            or "not found" in data["error"].get("message", "").lower()
        )

    def test_get_advice_returns_valid_recommendation(
        self,
        client: TestClient,
        session: Session,
        sample_monsters: list[Monster],
        sample_slayer_tasks: list[SlayerTask],
    ):
        """Test that advice returns a valid recommendation."""
        # Get tasks
        tasks_response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        tasks = tasks_response.json()

        if len(tasks) > 0:
            task_id = tasks[0]["task_id"]
            response = client.get(f"/api/v1/slayer/advice/{task_id}")

            assert response.status_code == 200
            data = response.json()

            # Recommendation should be one of the valid options
            valid_recommendations = ["DO", "SKIP", "BLOCK"]
            assert data["recommendation"] in valid_recommendations
