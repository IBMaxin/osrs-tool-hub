"""Full flow integration tests - testing complete user workflows."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot, Monster, SlayerTask, SlayerMaster


class TestFullFlippingWorkflow:
    """Test complete flipping workflow from data setup to API response."""
    
    def test_complete_flip_scanner_workflow(self, client: TestClient, session: Session):
        """Test complete workflow: create items -> sync prices -> query scanner."""
        # Step 1: Create items with price data
        items = [
            Item(
                id=4151,
                name="Abyssal whip",
                members=True,
                limit=70,
                high_price=1500000,
                low_price=1400000,
                high_time=1700000000,
                low_time=1700000000,
                buy_limit=70,
            ),
            Item(
                id=11802,
                name="Saradomin godsword",
                members=True,
                limit=8,
                high_price=52_000_000,
                low_price=50_000_000,
                high_time=1700000000,
                low_time=1700000000,
                buy_limit=8,
            ),
        ]
        for item in items:
            session.add(item)
        
        # Step 2: Create price snapshots for volume data
        snapshots = [
            PriceSnapshot(
                item_id=4151,
                high_price=1500000,
                low_price=1400000,
                high_volume=5000,
                low_volume=4000,
            ),
            PriceSnapshot(
                item_id=11802,
                high_price=52_000_000,
                low_price=50_000_000,
                high_volume=200,
                low_volume=150,
            ),
        ]
        for snapshot in snapshots:
            session.add(snapshot)
        
        session.commit()
        
        # Step 3: Query the scanner endpoint
        response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=100000000&"
            "min_roi=0.5&"
            "min_volume=100"
        )
        
        # Step 4: Verify results
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        
        # Verify both items are in results
        item_names = [r["name"] for r in data]
        assert "Abyssal whip" in item_names
        assert "Saradomin godsword" in item_names
        
        # Verify calculations are correct
        whip_result = next(r for r in data if r["name"] == "Abyssal whip")
        assert whip_result["buy_price"] == 1400000
        assert whip_result["sell_price"] == 1500000
        assert whip_result["roi"] > 0


class TestFullGearWorkflow:
    """Test complete gear workflow from items to gear sets."""
    
    def test_create_and_retrieve_gear_set_workflow(self, client: TestClient, session: Session):
        """Test complete workflow: create items -> create gear set -> retrieve it."""
        # Step 1: Create items with prices
        items = [
            Item(
                id=4151,
                name="Abyssal whip",
                members=True,
                limit=70,
                high_price=1500000,
                low_price=1400000,
            ),
            Item(
                id=11802,
                name="Saradomin godsword",
                members=True,
                limit=8,
                high_price=52_000_000,
                low_price=50_000_000,
            ),
        ]
        for item in items:
            session.add(item)
        session.commit()
        
        # Step 2: Create gear set via API
        payload = {
            "name": "My Melee Set",
            "description": "A complete melee setup",
            "items": {
                4151: 1,
                11802: 1,
            }
        }
        create_response = client.post("/api/v1/gear", json=payload)
        assert create_response.status_code == 201
        gear_set_id = create_response.json()["id"]
        
        # Step 3: Retrieve the gear set
        get_response = client.get(f"/api/v1/gear/{gear_set_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        
        # Step 4: Verify data
        assert data["name"] == "My Melee Set"
        assert data["description"] == "A complete melee setup"
        assert data["items"] == payload["items"]
        assert data["total_cost"] == 1_400_000 + 50_000_000
        
        # Step 5: List all gear sets
        list_response = client.get("/api/v1/gear")
        assert list_response.status_code == 200
        all_sets = list_response.json()
        assert len(all_sets) >= 1
        assert any(gs["id"] == gear_set_id for gs in all_sets)


class TestFullSlayerWorkflow:
    """Test complete slayer workflow from monsters to advice."""
    
    def test_complete_slayer_workflow(self, client: TestClient, session: Session):
        """Test complete workflow: create monster -> create task -> get advice."""
        # Step 1: Create monster
        monster = Monster(
            id=415,
            name="Abyssal demon",
            combat_level=124,
            hitpoints=150,
            slayer_xp=150.0,
            is_slayer_monster=True,
        )
        session.add(monster)
        session.commit()
        
        # Step 2: Create slayer task
        task = SlayerTask(
            master=SlayerMaster.DURADEL,
            monster_id=monster.id,
            category="Abyssal demons",
            quantity_min=120,
            quantity_max=185,
            weight=12,
            is_skippable=True,
            is_blockable=True,
        )
        session.add(task)
        session.commit()
        
        # Step 3: Get tasks for master
        tasks_response = client.get(f"/api/v1/slayer/tasks/{SlayerMaster.DURADEL.value}")
        assert tasks_response.status_code == 200
        tasks = tasks_response.json()
        assert len(tasks) >= 1
        
        # Step 4: Get advice for the task
        task_id = tasks[0]["task_id"]
        advice_response = client.get(f"/api/v1/slayer/advice/{task_id}")
        assert advice_response.status_code == 200
        advice = advice_response.json()
        
        # Step 5: Verify advice structure
        assert "recommendation" in advice
        assert advice["recommendation"] in ["DO", "SKIP", "BLOCK"]
        assert "task" in advice
        assert "reason" in advice


class TestCrossFeatureIntegration:
    """Test integration between different features."""
    
    def test_flipping_uses_gear_item_prices(self, client: TestClient, session: Session):
        """Test that flipping scanner can use items that are also used in gear sets."""
        # Create an item
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            high_price=1500000,
            low_price=1400000,
            buy_limit=70,
        )
        session.add(item)
        
        snapshot = PriceSnapshot(
            item_id=4151,
            high_price=1500000,
            low_price=1400000,
            high_volume=5000,
            low_volume=4000,
        )
        session.add(snapshot)
        session.commit()
        
        # Use item in gear set
        gear_payload = {
            "name": "Whip Set",
            "items": {4151: 1}
        }
        gear_response = client.post("/api/v1/gear", json=gear_payload)
        assert gear_response.status_code == 201
        
        # Use same item in flip scanner
        flip_response = client.get(
            "/api/v1/flipping/scanner?"
            "budget=10000000&"
            "min_roi=0.1&"
            "min_volume=10"
        )
        assert flip_response.status_code == 200
        flip_data = flip_response.json()
        
        # Item should appear in both
        assert gear_response.json()["items"] == {4151: 1}
        assert any(r["item_id"] == 4151 for r in flip_data)
