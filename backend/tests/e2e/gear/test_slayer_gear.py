"""E2E tests for Slayer Gear endpoint."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, Monster, SlayerMaster
from backend.tests.e2e.base import BaseE2ETest
from backend.tests.e2e.helpers import (
    assert_successful_response,
    assert_error_response,
    create_test_slayer_task,
)


@pytest.mark.e2e
class TestSlayerGearEndpoint(BaseE2ETest):
    """Test POST /api/v1/gear/slayer-gear endpoint."""

    def test_suggest_slayer_gear_basic(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test getting slayer gear suggestions."""
        # Create a slayer task
        monster = sample_monsters[0]
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        payload = {
            "task_id": task.id,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70,
                "ranged": 70,
                "magic": 70,
                "prayer": 50,
            },
            "budget": 10000000,
            "combat_style": "melee",
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        data = assert_successful_response(response)

        assert isinstance(data, dict)

    def test_suggest_slayer_gear_with_quests(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test getting slayer gear suggestions with quests completed."""
        monster = sample_monsters[0]
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        payload = {
            "task_id": task.id,
            "stats": {
                "attack": 80,
                "strength": 80,
                "defence": 80,
                "ranged": 80,
                "magic": 80,
                "prayer": 60,
            },
            "budget": 50000000,
            "combat_style": "melee",
            "quests_completed": ["Dragon Slayer", "Monkey Madness"],
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        data = assert_successful_response(response)

        assert isinstance(data, dict)

    def test_suggest_slayer_gear_ironman(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test getting slayer gear suggestions for ironman."""
        monster = sample_monsters[0]
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        payload = {
            "task_id": task.id,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70,
                "ranged": 70,
                "magic": 70,
                "prayer": 50,
            },
            "budget": 10000000,
            "combat_style": "melee",
            "ironman": True,
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        data = assert_successful_response(response)

        assert isinstance(data, dict)

    def test_suggest_slayer_gear_nonexistent_task(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
    ):
        """Test getting slayer gear for non-existent task."""
        payload = {
            "task_id": 999999,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70,
                "ranged": 70,
                "magic": 70,
                "prayer": 50,
            },
            "budget": 10000000,
            "combat_style": "melee",
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        assert_error_response(response, 404)

    def test_suggest_slayer_gear_invalid_combat_style(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test getting slayer gear with invalid combat style."""
        monster = sample_monsters[0]
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        payload = {
            "task_id": task.id,
            "stats": {
                "attack": 70,
                "strength": 70,
                "defence": 70,
                "ranged": 70,
                "magic": 70,
                "prayer": 50,
            },
            "budget": 10000000,
            "combat_style": "invalid_style",
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        # May return 400 or 422 depending on validation
        assert response.status_code in (400, 422)

    def test_suggest_slayer_gear_missing_stats(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test getting slayer gear with missing stats."""
        monster = sample_monsters[0]
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        payload = {
            "task_id": task.id,
            "budget": 10000000,
            "combat_style": "melee",
            # Missing stats
        }

        response = client.post("/api/v1/gear/slayer-gear", json=payload)
        assert_error_response(response, 422)  # Validation error
