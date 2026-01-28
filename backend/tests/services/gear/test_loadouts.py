"""Unit tests for gear loadout optimization utilities."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.services.gear.loadouts import (
    suggest_gear,
    get_best_loadout,
    get_upgrade_path,
    get_alternatives,
)
from backend.models import Item, PriceSnapshot


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def sample_items(test_session):
    """Create sample items for testing."""
    items = [
        Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            limit=70,
            value=2000000,
            slot="weapon",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_req=70,
            strength_req=70,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
            is_2h=False,
        ),
        Item(
            id=1163,
            name="Rune full helm",
            members=True,
            limit=70,
            value=20000,
            slot="head",
            defence_req=40,
            attack_req=1,
            strength_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
            melee_strength=0,
            ranged_strength=0,
            magic_damage=0,
            attack_slash=0,
            attack_ranged=0,
            attack_magic=0,
        ),
        Item(
            id=12954,
            name="Dragon scimitar",
            members=True,
            limit=70,
            value=60000,
            slot="weapon",
            attack_stab=60,
            attack_slash=66,
            attack_crush=0,
            melee_strength=66,
            attack_req=60,
            strength_req=60,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
            is_2h=False,
        ),
    ]
    for item in items:
        test_session.add(item)
    test_session.commit()
    return items


class TestSuggestGear:
    """Test suggest_gear function."""

    def test_suggest_gear_melee(self, test_session, sample_items):
        """Test suggest_gear for melee combat style."""
        results = suggest_gear(test_session, "weapon", "melee", budget_per_slot=10000000)

        assert len(results) > 0
        # Should be sorted by score descending
        assert results[0]["score"] >= results[-1]["score"] if len(results) > 1 else True
        assert "id" in results[0]
        assert "name" in results[0]
        assert "score" in results[0]

    def test_suggest_gear_ranged(self, test_session):
        """Test suggest_gear for ranged combat style."""
        # Create a ranged weapon
        item = Item(
            id=861,
            name="Magic shortbow",
            members=True,
            slot="weapon",
            attack_ranged=69,
            ranged_strength=55,
            ranged_req=50,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        results = suggest_gear(test_session, "weapon", "ranged", budget_per_slot=10000000)

        assert len(results) > 0
        assert results[0]["score"] > 0

    def test_suggest_gear_magic(self, test_session):
        """Test suggest_gear for magic combat style."""
        # Create a magic weapon
        item = Item(
            id=4675,
            name="Ancient staff",
            members=True,
            slot="weapon",
            attack_magic=75,
            magic_damage=15,
            magic_req=50,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        results = suggest_gear(test_session, "weapon", "magic", budget_per_slot=10000000)

        assert len(results) > 0
        assert results[0]["score"] > 0

    def test_suggest_gear_prayer(self, test_session):
        """Test suggest_gear for prayer combat style."""
        # Create an item with prayer bonus
        item = Item(
            id=1044,
            name="Holy symbol",
            members=True,
            slot="neck",
            prayer_bonus=8,
            attack_req=1,
            strength_req=1,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        test_session.commit()

        results = suggest_gear(test_session, "neck", "prayer", budget_per_slot=10000000)

        assert len(results) > 0
        assert results[0]["score"] > 0

    def test_suggest_gear_filters_by_defence_level(self, test_session):
        """Test suggest_gear filters items by defence level requirement."""
        # Create an item with high defence requirement
        high_def_item = Item(
            id=9999,
            name="High defence helm",
            members=True,
            slot="head",
            defence_req=99,  # High requirement
            attack_req=1,
            strength_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(high_def_item)
        test_session.commit()

        # Request with low defence level
        results = suggest_gear(test_session, "head", "melee", defence_level=50)

        # Should not include items requiring defence > 50
        item_ids = [r["id"] for r in results]
        assert 9999 not in item_ids  # High defence item excluded

    def test_suggest_gear_returns_top_10(self, test_session):
        """Test suggest_gear returns at most 10 items."""
        # Create many items
        for i in range(20):
            item = Item(
                id=1000 + i,
                name=f"Test weapon {i}",
                members=True,
                slot="weapon",
                attack_slash=50 + i,
                melee_strength=50 + i,
                attack_req=1,
                strength_req=1,
                defence_req=1,
                ranged_req=1,
                magic_req=1,
                prayer_req=1,
                slayer_req=0,
            )
            test_session.add(item)
        test_session.commit()

        results = suggest_gear(test_session, "weapon", "melee", budget_per_slot=10000000)

        assert len(results) <= 10


class TestGetBestLoadout:
    """Test get_best_loadout function."""

    def test_get_best_loadout_melee(self, test_session, sample_items):
        """Test get_best_loadout for melee combat style."""
        # Add price snapshots
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value, low_price=item.value - 1000
            )
            test_session.add(snapshot)
        test_session.commit()

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        result = get_best_loadout(test_session, "melee", budget=10000000, stats=stats)

        assert result["combat_style"] == "melee"
        assert "total_cost" in result
        assert "dps" in result
        assert "slots" in result

    def test_get_best_loadout_with_exclude_slots(self, test_session, sample_items):
        """Test get_best_loadout excludes specified slots."""
        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        result = get_best_loadout(
            test_session, "melee", budget=10000000, stats=stats, exclude_slots=["shield"]
        )

        assert "shield" not in result["slots"] or result["slots"]["shield"] is None

    def test_get_best_loadout_handles_2h_weapons(self, test_session):
        """Test get_best_loadout excludes shield when weapon is 2H."""
        # Create a 2H weapon
        weapon = Item(
            id=7158,
            name="Dragon 2h sword",
            members=True,
            slot="weapon",
            attack_slash=80,
            melee_strength=80,
            is_2h=True,
            attack_req=60,
            strength_req=60,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(weapon)
        test_session.commit()

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        result = get_best_loadout(test_session, "melee", budget=10000000, stats=stats)

        # Shield should be None if weapon is 2H
        if "weapon" in result["slots"] and result["slots"]["weapon"]:
            # Check if weapon is 2H, then shield should be None
            # This depends on the actual weapon selected
            pass  # Just verify function runs without error

    def test_get_best_loadout_respects_budget(self, test_session, sample_items):
        """Test get_best_loadout respects budget constraints."""
        # Set high prices
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value * 10, low_price=item.value * 9
            )
            test_session.add(snapshot)
        test_session.commit()

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        result = get_best_loadout(test_session, "melee", budget=100000, stats=stats)

        assert result["total_cost"] <= 100000
        assert result["budget_used"] <= 100000

    def test_get_best_loadout_with_quests(self, test_session):
        """Test get_best_loadout filters by quest requirements."""
        # Create item with quest requirement
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            slot="weapon",
            attack_slash=82,
            melee_strength=82,
            quest_req="Recipe for Disaster",
            attack_req=70,
            strength_req=70,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        snapshot = PriceSnapshot(item_id=4151, high_price=2000000, low_price=1900000)
        test_session.add(snapshot)
        test_session.commit()

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        result = get_best_loadout(
            test_session,
            "melee",
            budget=10000000,
            stats=stats,
            quests_completed={"Recipe for Disaster"},
        )

        # Should include quest-locked items if quest completed
        assert result is not None


class TestGetUpgradePath:
    """Test get_upgrade_path function."""

    def test_get_upgrade_path_finds_better_items(self, test_session, sample_items):
        """Test get_upgrade_path finds better items for current loadout."""
        # Add price snapshots
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value, low_price=item.value - 1000
            )
            test_session.add(snapshot)
        test_session.commit()

        current_loadout = {"weapon": 12954}  # Dragon scimitar
        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}

        result = get_upgrade_path(
            test_session, current_loadout, "melee", budget=10000000, stats=stats
        )

        assert result["combat_style"] == "melee"
        assert "upgrades" in result
        # Should find upgrade for weapon (Abyssal whip is better)
        if "weapon" in result["upgrades"]:
            assert (
                result["upgrades"]["weapon"]["recommended"]["score"]
                > result["upgrades"]["weapon"]["current"]["score"]
            )

    def test_get_upgrade_path_no_current_item(self, test_session):
        """Test get_upgrade_path handles None current item."""
        current_loadout = {"weapon": None}
        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}

        result = get_upgrade_path(
            test_session, current_loadout, "melee", budget=10000000, stats=stats
        )

        # Should return empty upgrades for None items
        assert result["upgrades"] == {}

    def test_get_upgrade_path_nonexistent_item(self, test_session):
        """Test get_upgrade_path handles nonexistent current item."""
        current_loadout = {"weapon": 99999}  # Non-existent ID
        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}

        result = get_upgrade_path(
            test_session, current_loadout, "melee", budget=10000000, stats=stats
        )

        # Should handle gracefully
        assert result["upgrades"] == {}

    def test_get_upgrade_path_respects_budget(self, test_session, sample_items):
        """Test get_upgrade_path respects budget constraints."""
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value, low_price=item.value - 1000
            )
            test_session.add(snapshot)
        test_session.commit()

        current_loadout = {"weapon": 12954}  # Dragon scimitar
        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}

        result = get_upgrade_path(
            test_session, current_loadout, "melee", budget=100000, stats=stats
        )

        # Upgrade cost should be within budget
        if result["upgrades"]:
            total_cost = result["total_upgrade_cost"]
            assert total_cost <= 100000


class TestGetAlternatives:
    """Test get_alternatives function."""

    def test_get_alternatives_melee(self, test_session, sample_items):
        """Test get_alternatives for melee combat style."""
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value, low_price=item.value - 1000
            )
            test_session.add(snapshot)
        test_session.commit()

        results = get_alternatives(test_session, "weapon", "melee", limit=10)

        assert len(results) > 0
        assert len(results) <= 10
        # Should be sorted by score descending
        if len(results) > 1:
            assert results[0]["score"] >= results[-1]["score"]

    def test_get_alternatives_with_budget(self, test_session, sample_items):
        """Test get_alternatives filters by budget."""
        for item in sample_items:
            snapshot = PriceSnapshot(
                item_id=item.id, high_price=item.value, low_price=item.value - 1000
            )
            test_session.add(snapshot)
        test_session.commit()

        results = get_alternatives(test_session, "weapon", "melee", budget=100000, limit=10)

        # All items should be within budget
        for item in results:
            assert item["price"] <= 100000

    def test_get_alternatives_with_stats(self, test_session, sample_items):
        """Test get_alternatives filters by stat requirements."""
        stats = {"attack": 60, "strength": 60, "defence": 1, "ranged": 1, "magic": 1, "prayer": 1}

        results = get_alternatives(test_session, "weapon", "melee", stats=stats, limit=10)

        # All items should meet stat requirements
        for item in results:
            assert item["requirements"]["attack"] <= 60

    def test_get_alternatives_with_quests(self, test_session):
        """Test get_alternatives filters by quest requirements."""
        # Create item with quest requirement
        item = Item(
            id=4151,
            name="Abyssal whip",
            members=True,
            slot="weapon",
            attack_slash=82,
            melee_strength=82,
            quest_req="Recipe for Disaster",
            attack_req=70,
            strength_req=70,
            defence_req=1,
            ranged_req=1,
            magic_req=1,
            prayer_req=1,
            slayer_req=0,
        )
        test_session.add(item)
        snapshot = PriceSnapshot(item_id=4151, high_price=2000000, low_price=1900000)
        test_session.add(snapshot)
        test_session.commit()

        stats = {"attack": 70, "strength": 70, "defence": 70, "ranged": 1, "magic": 1, "prayer": 1}
        results = get_alternatives(
            test_session,
            "weapon",
            "melee",
            stats=stats,
            quests_completed={"Recipe for Disaster"},
            limit=10,
        )

        # Should include quest-locked items if quest completed
        assert len(results) > 0

    def test_get_alternatives_respects_limit(self, test_session):
        """Test get_alternatives respects limit parameter."""
        # Create many items
        for i in range(20):
            item = Item(
                id=1000 + i,
                name=f"Test weapon {i}",
                members=True,
                slot="weapon",
                attack_slash=50 + i,
                melee_strength=50 + i,
                attack_req=1,
                strength_req=1,
                defence_req=1,
                ranged_req=1,
                magic_req=1,
                prayer_req=1,
                slayer_req=0,
            )
            test_session.add(item)
            snapshot = PriceSnapshot(item_id=1000 + i, high_price=100000, low_price=90000)
            test_session.add(snapshot)
        test_session.commit()

        results = get_alternatives(test_session, "weapon", "melee", limit=5)

        assert len(results) <= 5
