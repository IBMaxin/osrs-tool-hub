"""Tests for slayer gear suggestion endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session

from backend.models import Monster, SlayerTask, SlayerMaster


class TestSlayerGearEndpoint:
    """Test slayer gear suggestion endpoint."""

    def test_suggest_slayer_gear_success(
        self, client: TestClient, session: Session, sample_slayer_tasks, sample_monsters
    ):
        """Test successful slayer gear suggestion."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {
                "task_id": task.id,
                "monster_name": "Abyssal demon",
                "combat_style": "melee",
                "tier_loadouts": [{"tier": "70+", "loadout": {}}],
            }

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"attack": 70, "strength": 70, "defence": 70},
                    "budget": 10000000,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert "task_id" in data
            assert "monster_name" in data

    def test_suggest_slayer_gear_task_not_found(
        self, client: TestClient, session: Session
    ):
        """Test slayer gear suggestion with non-existent task."""
        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {"error": "Task not found"}

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": 99999,
                    "stats": {"attack": 70, "strength": 70},
                    "budget": 10000000,
                },
            )

            assert response.status_code == 404
            # Check error detail (FastAPI error format)
            error_data = response.json()
            assert "detail" in error_data or "error" in error_data
            error_msg = error_data.get("detail", error_data.get("error", {}).get("message", ""))
            assert "task not found" in str(error_msg).lower()

    def test_suggest_slayer_gear_with_combat_style(
        self, client: TestClient, session: Session, sample_slayer_tasks
    ):
        """Test slayer gear suggestion with combat style override."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {
                "task_id": task.id,
                "combat_style": "ranged",
                "tier_loadouts": [],
            }

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"ranged": 70, "attack": 70},
                    "combat_style": "ranged",
                    "budget": 10000000,
                },
            )

            assert response.status_code == 200
            call_kwargs = mock_service.suggest_slayer_gear.call_args[1]
            assert call_kwargs["combat_style"] == "ranged"

    def test_suggest_slayer_gear_with_quests_and_achievements(
        self, client: TestClient, session: Session, sample_slayer_tasks
    ):
        """Test slayer gear suggestion with quests and achievements."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {
                "task_id": task.id,
                "tier_loadouts": [],
            }

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"attack": 70, "strength": 70},
                    "quests_completed": ["Dragon Slayer"],
                    "achievements_completed": ["Achievement 1"],
                    "budget": 10000000,
                },
            )

            assert response.status_code == 200
            call_kwargs = mock_service.suggest_slayer_gear.call_args[1]
            assert call_kwargs["quests_completed"] == {"Dragon Slayer"}
            assert call_kwargs["achievements_completed"] == {"Achievement 1"}

    def test_suggest_slayer_gear_ironman_mode(
        self, client: TestClient, session: Session, sample_slayer_tasks
    ):
        """Test slayer gear suggestion with ironman mode."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {
                "task_id": task.id,
                "tier_loadouts": [],
            }

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"attack": 70, "strength": 70},
                    "ironman": True,
                    "budget": 10000000,
                },
            )

            assert response.status_code == 200
            call_kwargs = mock_service.suggest_slayer_gear.call_args[1]
            assert call_kwargs["ironman"] is True

    def test_suggest_slayer_gear_handles_service_errors(
        self, client: TestClient, session: Session, sample_slayer_tasks
    ):
        """Test slayer gear suggestion handles service errors."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.side_effect = Exception("Service error")

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"attack": 70, "strength": 70},
                    "budget": 10000000,
                },
            )

            assert response.status_code == 400
            assert "error" in response.json()["error"]["message"].lower()

    def test_suggest_slayer_gear_validation_error(self, client: TestClient):
        """Test slayer gear suggestion with invalid request."""
        response = client.post(
            "/api/v1/gear/slayer-gear",
            json={
                "task_id": 1,
                "stats": {"invalid": 70},  # Invalid stat name
                "budget": 10000000,
            },
        )

        assert response.status_code == 422  # Validation error

    def test_suggest_slayer_gear_invalid_combat_style(self, client: TestClient):
        """Test slayer gear suggestion with invalid combat style."""
        response = client.post(
            "/api/v1/gear/slayer-gear",
            json={
                "task_id": 1,
                "stats": {"attack": 70, "strength": 70},
                "combat_style": "invalid",
                "budget": 10000000,
            },
        )

        assert response.status_code == 422  # Validation error

    def test_suggest_slayer_gear_empty_quests_list(
        self, client: TestClient, session: Session, sample_slayer_tasks
    ):
        """Test slayer gear suggestion with empty quests list."""
        task = sample_slayer_tasks[0]

        with patch("backend.api.v1.gear.routes.slayer.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.suggest_slayer_gear.return_value = {
                "task_id": task.id,
                "tier_loadouts": [],
            }

            response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
                    "task_id": task.id,
                    "stats": {"attack": 70, "strength": 70},
                    "quests_completed": [],
                    "budget": 10000000,
                },
            )

            assert response.status_code == 200
            call_kwargs = mock_service.suggest_slayer_gear.call_args[1]
            assert call_kwargs["quests_completed"] is None
