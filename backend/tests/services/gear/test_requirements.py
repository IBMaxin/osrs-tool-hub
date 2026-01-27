"""Tests for gear requirements checking."""
import pytest
from backend.models import Item
from backend.services.gear.requirements import meets_requirements


def test_meets_requirements_all_stats_pass():
    """Test that item meets requirements when all stats are sufficient."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=70,
        strength_req=70,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1
    )
    
    stats = {
        "attack": 70,
        "strength": 70,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is True


def test_meets_requirements_attack_too_low():
    """Test that item fails when attack requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=70,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1
    )
    
    stats = {
        "attack": 69,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_strength_too_low():
    """Test that item fails when strength requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=70,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1
    )
    
    stats = {
        "attack": 1,
        "strength": 69,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_defence_too_low():
    """Test that item fails when defence requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=70,
        ranged_req=1,
        magic_req=1,
        prayer_req=1
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 69,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_ranged_too_low():
    """Test that item fails when ranged requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=70,
        magic_req=1,
        prayer_req=1
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 69,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_magic_too_low():
    """Test that item fails when magic requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=70,
        prayer_req=1
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 69,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_prayer_too_low():
    """Test that item fails when prayer requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=70
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 69
    }
    
    assert meets_requirements(item, stats) is False


def test_meets_requirements_missing_stat_defaults_to_1():
    """Test that missing stats default to 1."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1
    )
    
    # Missing some stats - should default to 1
    stats = {
        "attack": 1,
        "strength": 1
    }
    
    assert meets_requirements(item, stats) is True


def test_meets_requirements_quest_required_and_completed():
    """Test that item passes when quest requirement is met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        quest_req="Recipe for Disaster"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    quests_completed = {"Recipe for Disaster"}
    
    assert meets_requirements(item, stats, quests_completed=quests_completed) is True


def test_meets_requirements_quest_required_but_not_completed():
    """Test that item fails when quest requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        quest_req="Recipe for Disaster"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    quests_completed = set()  # Empty set
    
    assert meets_requirements(item, stats, quests_completed=quests_completed) is False


def test_meets_requirements_quest_required_but_quests_none():
    """Test that item fails when quest is required but quests_completed is None."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        quest_req="Recipe for Disaster"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats, quests_completed=None) is False


def test_meets_requirements_achievement_required_and_completed():
    """Test that item passes when achievement requirement is met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        achievement_req="Fight Caves"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    achievements_completed = {"Fight Caves"}
    
    assert meets_requirements(item, stats, achievements_completed=achievements_completed) is True


def test_meets_requirements_achievement_required_but_not_completed():
    """Test that item fails when achievement requirement is not met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        achievement_req="Fight Caves"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    achievements_completed = set()  # Empty set
    
    assert meets_requirements(item, stats, achievements_completed=achievements_completed) is False


def test_meets_requirements_achievement_required_but_achievements_none():
    """Test that item fails when achievement is required but achievements_completed is None."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=1,
        strength_req=1,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        achievement_req="Fight Caves"
    )
    
    stats = {
        "attack": 1,
        "strength": 1,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    assert meets_requirements(item, stats, achievements_completed=None) is False


def test_meets_requirements_all_requirements_met():
    """Test that item passes when all requirements (stats, quest, achievement) are met."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_req=70,
        strength_req=70,
        defence_req=1,
        ranged_req=1,
        magic_req=1,
        prayer_req=1,
        quest_req="Recipe for Disaster",
        achievement_req="Fight Caves"
    )
    
    stats = {
        "attack": 70,
        "strength": 70,
        "defence": 1,
        "ranged": 1,
        "magic": 1,
        "prayer": 1
    }
    
    quests_completed = {"Recipe for Disaster"}
    achievements_completed = {"Fight Caves"}
    
    assert meets_requirements(item, stats, quests_completed=quests_completed, achievements_completed=achievements_completed) is True
