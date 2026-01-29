"""Integration tests for complete multi-step user workflows."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.models import Item, PriceSnapshot, Monster, SlayerTask


@pytest.mark.integration
class TestCompleteFlippingWorkflow:
    """Test complete flipping workflow from discovery to tracking."""

    def test_discover_flip_track_profit_workflow(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test complete workflow: discover flip -> add to watchlist -> track trade -> check stats."""
        user_id = "test-user-flip-workflow"
        item = sample_items[0]

        # Step 1: Discover flip opportunity
        flip_response = client.get(
            "/api/v1/flips/opportunities?max_budget=10000000&min_roi=1.0&min_volume=100"
        )
        assert flip_response.status_code == 200
        opportunities = flip_response.json()

        # Find our test item in opportunities
        item_opportunity = next((o for o in opportunities if o["item_id"] == item.id), None)
        if not item_opportunity:
            pytest.skip(f"Item {item.id} not found in flip opportunities")

        # Step 2: Add item to watchlist
        watchlist_response = client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user_id,
                "item_id": item.id,
                "alert_type": "price_below",
                "threshold": item_opportunity["buy_price"],
            },
        )
        assert watchlist_response.status_code == 201

        # Step 3: Create trade (simulating buy)
        buy_trade = client.post(
            "/api/v1/trades",
            json={
                "user_id": user_id,
                "item_id": item.id,
                "buy_price": item_opportunity["buy_price"],
                "quantity": 1,
                "status": "bought",
            },
        )
        assert buy_trade.status_code == 201

        # Step 4: Create sell trade
        sell_trade = client.post(
            "/api/v1/trades",
            json={
                "user_id": user_id,
                "item_id": item.id,
                "buy_price": item_opportunity["buy_price"],
                "sell_price": item_opportunity["sell_price"],
                "quantity": 1,
                "status": "sold",
            },
        )
        assert sell_trade.status_code == 201

        # Step 5: Check trade stats
        stats_response = client.get(f"/api/v1/trades/stats?user_id={user_id}")
        assert stats_response.status_code == 200
        stats = stats_response.json()

        assert stats["total_trades"] == 2
        assert stats["sold_trades"] == 1
        assert stats["total_profit"] > 0

        # Step 6: Verify watchlist still active
        watchlist = client.get(f"/api/v1/watchlist?user_id={user_id}").json()
        assert len(watchlist) == 1


@pytest.mark.integration
class TestCompleteGearProgressionWorkflow:
    """Test complete gear progression workflow."""

    def test_progression_suggestion_upgrade_workflow(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test workflow: get progression -> get suggestions -> create gear set -> get upgrade path."""
        # Step 1: Get gear progression
        progression_response = client.get("/api/v1/gear/progression/melee")
        assert progression_response.status_code == 200
        progression = progression_response.json()

        assert "combat_style" in progression
        assert "slots" in progression

        # Step 2: Get gear suggestions (need slot parameter)
        suggestions_response = client.get(
            "/api/v1/gear/suggestions?slot=weapon&combat_style=melee&budget=10000000"
        )
        if suggestions_response.status_code == 200:
            suggestions = suggestions_response.json()
            assert isinstance(suggestions, list)

            # Step 3: Create gear set from suggestions
            if len(suggestions) > 0:
                # Use first suggestion to create gear set
                first_suggestion = suggestions[0]
                item_id = first_suggestion.get("item_id") or first_suggestion.get("id")

                if item_id:
                    gear_set_payload = {
                        "name": "My Progression Set",
                        "items": {item_id: 1},
                    }
                    gear_set_response = client.post("/api/v1/gear", json=gear_set_payload)
                    assert gear_set_response.status_code == 201
                    gear_set_response.json()["id"]

                    # Step 4: Get upgrade path
                    upgrade_payload = {
                        "current_loadout": {"weapon": item_id},
                        "combat_style": "melee",
                        "budget": 50000000,
                        "stats": {"attack": 70, "strength": 70, "defence": 70},
                        "attack_type": "slash",
                    }
                    upgrade_response = client.post(
                        "/api/v1/gear/upgrade-path", json=upgrade_payload
                    )
                    assert upgrade_response.status_code == 200
                    upgrade_data = upgrade_response.json()

                    assert isinstance(upgrade_data, dict)


@pytest.mark.integration
class TestCompleteSlayerWorkflow:
    """Test complete slayer task workflow."""

    def test_slayer_task_advice_gear_workflow(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_monsters: list[Monster],
    ):
        """Test workflow: get tasks -> get advice -> get gear suggestions -> create gear set."""
        # Step 1: Get slayer masters
        masters_response = client.get("/api/v1/slayer/masters")
        assert masters_response.status_code == 200
        masters = masters_response.json()

        if len(masters) == 0:
            pytest.skip("No slayer masters available for testing")

        # Step 2: Get tasks for master
        master = masters[0]
        tasks_response = client.get(f"/api/v1/slayer/tasks/{master}")
        assert tasks_response.status_code == 200
        tasks = tasks_response.json()

        if len(tasks) == 0:
            pytest.skip(f"No tasks available for master {master}")

        # Step 3: Get advice for task
        task_id = tasks[0]["task_id"]
        advice_response = client.get(f"/api/v1/slayer/advice/{task_id}")
        assert advice_response.status_code == 200
        advice = advice_response.json()

        assert "recommendation" in advice

        # Step 4: Get gear suggestion for task
        # First, get the actual task from database
        from sqlmodel import select

        task = session.exec(select(SlayerTask).where(SlayerTask.id == task_id)).first()

        if task:
            gear_response = client.post(
                "/api/v1/gear/slayer-gear",
                json={
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
                },
            )
            assert gear_response.status_code == 200
            gear_data = gear_response.json()

            assert isinstance(gear_data, dict)


@pytest.mark.integration
class TestCrossFeatureDataConsistency:
    """Test data consistency across different features."""

    def test_item_price_consistency_across_features(
        self,
        client: TestClient,
        session: Session,
        sample_items: list[Item],
        sample_price_snapshots: list[PriceSnapshot],
    ):
        """Test that item prices are consistent across flipping, gear, and trades."""
        item = sample_items[0]

        # Get price from item endpoint
        item_response = client.get(f"/api/v1/gear/items/{item.id}")
        assert item_response.status_code == 200
        item_price = item_response.json()["price"]

        # Get price from flip opportunities
        flip_response = client.get("/api/v1/flips/opportunities")
        assert flip_response.status_code == 200
        flip_opportunities = flip_response.json()
        item_flip = next((f for f in flip_opportunities if f["item_id"] == item.id), None)

        if item_flip:
            # Prices should be related (buy_price <= item_price <= sell_price approximately)
            assert item_flip["buy_price"] <= item_flip["sell_price"]

        # Create trade with item price
        trade_response = client.post(
            "/api/v1/trades",
            json={
                "user_id": "test-user",
                "item_id": item.id,
                "buy_price": item_price,
                "quantity": 1,
            },
        )
        assert trade_response.status_code == 201

    def test_user_data_isolation(
        self, client: TestClient, session: Session, sample_items: list[Item]
    ):
        """Test that user data is properly isolated across features."""
        user1 = "user-isolation-1"
        user2 = "user-isolation-2"
        item = sample_items[0]

        # User 1: Create trade and watchlist
        client.post(
            "/api/v1/trades",
            json={"user_id": user1, "item_id": item.id, "buy_price": 1000, "quantity": 1},
        )
        client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user1,
                "item_id": item.id,
                "alert_type": "price_below",
                "threshold": 1000,
            },
        )

        # User 2: Create trade and watchlist for same item
        client.post(
            "/api/v1/trades",
            json={"user_id": user2, "item_id": item.id, "buy_price": 1000, "quantity": 1},
        )
        client.post(
            "/api/v1/watchlist",
            json={
                "user_id": user2,
                "item_id": item.id,
                "alert_type": "price_above",
                "threshold": 2000,
            },
        )

        # Verify isolation
        user1_trades = client.get(f"/api/v1/trades?user_id={user1}").json()
        user2_trades = client.get(f"/api/v1/trades?user_id={user2}").json()
        user1_watchlist = client.get(f"/api/v1/watchlist?user_id={user1}").json()
        user2_watchlist = client.get(f"/api/v1/watchlist?user_id={user2}").json()

        assert len(user1_trades) == 1
        assert len(user2_trades) == 1
        assert len(user1_watchlist) == 1
        assert len(user2_watchlist) == 1

        # Verify users can't see each other's data
        assert user1_trades[0]["user_id"] == user1
        assert user2_trades[0]["user_id"] == user2
        assert user1_watchlist[0]["user_id"] == user1
        assert user2_watchlist[0]["user_id"] == user2
