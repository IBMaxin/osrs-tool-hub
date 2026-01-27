"""Tests for gear scoring utilities."""
import pytest
from backend.models import Item
from backend.services.gear.scoring import score_item_for_style


def test_score_item_for_style_melee_stab():
    """Test scoring melee item with stab attack type."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_stab=82,
        attack_slash=82,
        attack_crush=0,
        melee_strength=82
    )
    
    score = score_item_for_style(item, "melee", attack_type="stab")
    assert score == 82 * 4 + 82  # melee_strength * 4 + attack_stab


def test_score_item_for_style_melee_slash():
    """Test scoring melee item with slash attack type."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_stab=0,
        attack_slash=82,
        attack_crush=0,
        melee_strength=82
    )
    
    score = score_item_for_style(item, "melee", attack_type="slash")
    assert score == 82 * 4 + 82  # melee_strength * 4 + attack_slash


def test_score_item_for_style_melee_crush():
    """Test scoring melee item with crush attack type."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_stab=0,
        attack_slash=0,
        attack_crush=82,
        melee_strength=82
    )
    
    score = score_item_for_style(item, "melee", attack_type="crush")
    assert score == 82 * 4 + 82  # melee_strength * 4 + attack_crush


def test_score_item_for_style_melee_no_attack_type():
    """Test scoring melee item without attack type (uses best attack bonus)."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_stab=70,
        attack_slash=82,
        attack_crush=60,
        melee_strength=82
    )
    
    score = score_item_for_style(item, "melee", attack_type=None)
    # Should use max(70, 82, 60) = 82
    assert score == 82 * 4 + 82  # melee_strength * 4 + max(attack bonuses)


def test_score_item_for_style_melee_best_attack_bonus():
    """Test that melee scoring uses the best attack bonus when no attack type specified."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        attack_stab=100,
        attack_slash=50,
        attack_crush=75,
        melee_strength=82
    )
    
    score = score_item_for_style(item, "melee")
    # Should use max(100, 50, 75) = 100
    assert score == 82 * 4 + 100


def test_score_item_for_style_ranged():
    """Test scoring ranged item."""
    item = Item(
        id=861,
        name="Magic shortbow",
        attack_ranged=69,
        ranged_strength=55
    )
    
    score = score_item_for_style(item, "ranged")
    assert score == 55 * 4 + 69  # ranged_strength * 4 + attack_ranged


def test_score_item_for_style_magic():
    """Test scoring magic item."""
    item = Item(
        id=1409,
        name="Mystic fire staff",
        attack_magic=10,
        magic_damage=15
    )
    
    score = score_item_for_style(item, "magic")
    assert score == 15 * 10 + 10  # magic_damage * 10 + attack_magic


def test_score_item_for_style_prayer():
    """Test scoring prayer item."""
    item = Item(
        id=1042,
        name="Holy symbol",
        prayer_bonus=8
    )
    
    score = score_item_for_style(item, "prayer")
    assert score == 8 * 10  # prayer_bonus * 10


def test_score_item_for_style_unknown_style():
    """Test scoring item with unknown combat style returns 0."""
    item = Item(
        id=4151,
        name="Abyssal whip",
        melee_strength=82
    )
    
    score = score_item_for_style(item, "unknown_style")
    assert score == 0.0


def test_score_item_for_style_zero_stats():
    """Test scoring item with zero stats."""
    item = Item(
        id=1,
        name="Item with no stats",
        attack_stab=0,
        attack_slash=0,
        attack_crush=0,
        melee_strength=0,
        attack_ranged=0,
        ranged_strength=0,
        attack_magic=0,
        magic_damage=0,
        prayer_bonus=0
    )
    
    assert score_item_for_style(item, "melee") == 0.0
    assert score_item_for_style(item, "ranged") == 0.0
    assert score_item_for_style(item, "magic") == 0.0
    assert score_item_for_style(item, "prayer") == 0.0
