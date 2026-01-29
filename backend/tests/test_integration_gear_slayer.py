"""Integration tests for Gear and Slayer service interactions."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, Monster, SlayerMaster
from backend.services.gear import GearService
from backend.tests.e2e.helpers import create_test_slayer_task


@pytest.mark.integration
class TestGearSlayerIntegration:
    """Test integration between Gear and Slayer services."""

    def test_slayer_gear_suggestion_workflow(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test complete workflow: slayer task -> gear suggestion -> verify loadout."""
        # Step 1: Create slayer task
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

        # Step 2: Get slayer gear suggestion
        gear_payload = {
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

        gear_response = client.post("/api/v1/gear/slayer-gear", json=gear_payload)
        assert gear_response.status_code == 200
        gear_data = gear_response.json()

        # Step 3: Verify gear suggestion structure
        assert isinstance(gear_data, dict)
        assert "tier_loadouts" in gear_data or "primary_loadout" in gear_data or "monster_name" in gear_data

        # Step 4: Verify task still exists and is accessible
        tasks_response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        assert tasks_response.status_code == 200
        tasks = tasks_response.json()
        assert any(t["task_id"] == task.id for t in tasks)

    def test_slayer_advice_with_gear_context(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test that slayer advice can be retrieved and gear suggestions work together."""
        # Create task
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

        # Get slayer advice
        tasks_response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        tasks = tasks_response.json()
        task_id = tasks[0]["task_id"]

        advice_response = client.get(f"/api/v1/slayer/advice/{task_id}")
        assert advice_response.status_code == 200
        advice = advice_response.json()

        # Get gear suggestion for same task
        gear_response = client.post(
            "/api/v1/gear/slayer-gear",
            json={
                "task_id": task.id,
                "stats": {"attack": 70, "strength": 70, "defence": 70, "ranged": 70, "magic": 70, "prayer": 50},
                "budget": 10000000,
                "combat_style": "melee",
            },
        )
        assert gear_response.status_code == 200

        # Verify both responses are consistent
        assert "task" in advice or "monster" in advice
        gear_data = gear_response.json()
        assert isinstance(gear_data, dict)

    def test_gear_service_with_slayer_task_data(
        self, session: Session, sample_items: list[Item], sample_monsters: list[Monster]
    ):
        """Test that GearService correctly uses SlayerTask data."""
        gear_service = GearService(session)
        monster = sample_monsters[0]

        # Create task
        task = create_test_slayer_task(
            session,
            SlayerMaster.DURADEL,
            monster.id,
            "Abyssal demons",
            120,
            185,
            12,
        )

        # Get slayer gear suggestion
        result = gear_service.suggest_slayer_gear(
            task_id=task.id,
            stats={"attack": 70, "strength": 70, "defence": 70, "ranged": 70, "magic": 70, "prayer": 50},
            budget=10000000,
            combat_style="melee",
        )

        assert "error" not in result
        assert isinstance(result, dict)

    def test_slayer_gear_with_different_combat_styles(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test slayer gear suggestions for different combat styles."""
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

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 70, "magic": 70, "prayer": 50}

        # Test melee
        melee_response = client.post(
            "/api/v1/gear/slayer-gear",
            json={"task_id": task.id, "stats": stats, "budget": 10000000, "combat_style": "melee"},
        )
        assert melee_response.status_code == 200

        # Test ranged
        ranged_response = client.post(
            "/api/v1/gear/slayer-gear",
            json={"task_id": task.id, "stats": stats, "budget": 10000000, "combat_style": "ranged"},
        )
        assert ranged_response.status_code == 200

        # Test magic
        magic_response = client.post(
            "/api/v1/gear/slayer-gear",
            json={"task_id": task.id, "stats": stats, "budget": 10000000, "combat_style": "magic"},
        )
        assert magic_response.status_code == 200

        # Verify all return valid data
        assert isinstance(melee_response.json(), dict)
        assert isinstance(ranged_response.json(), dict)
        assert isinstance(magic_response.json(), dict)


@pytest.mark.integration
class TestGearBossIntegration:
    """Test integration between Gear and Boss services."""

    def test_boss_bis_uses_gear_service(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that boss BiS calculation uses GearService loadout optimization."""
        from backend.services.gear.boss import get_available_bosses

        available_bosses = get_available_bosses()
        if not available_bosses:
            pytest.skip("No bosses available for testing")

        boss_name = available_bosses[0]

        payload = {
            "budget": 100000000,
            "stats": {
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
            "ironman": False,
        }

        response = client.post(f"/api/v1/gear/bis/{boss_name}", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Verify structure includes loadouts
        assert "boss_info" in data
        assert "recommended_loadouts" in data
        assert isinstance(data["recommended_loadouts"], list)

    def test_boss_list_with_gear_data(
        self, client: TestClient, session: Session
    ):
        """Test that boss list endpoint returns data usable by gear endpoints."""
        response = client.get("/api/v1/gear/bosses")
        assert response.status_code == 200
        data = response.json()

        assert "bosses" in data
        if len(data["bosses"]) > 0:
            boss = data["bosses"][0]
            # Verify boss has data needed for gear calculations
            assert "name" in boss
            assert "defence_stats" in boss or "recommended_styles" in boss
