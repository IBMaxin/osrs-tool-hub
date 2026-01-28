"""Unit tests for DPS calculation service."""

from backend.services.gear.dps import calculate_dps
from backend.models import Item


class TestCalculateDPS:
    """Test calculate_dps function."""

    def test_no_weapon_returns_zero_dps(self):
        """Test that DPS is 0 when no weapon is equipped."""
        items = {"head": None, "body": None}
        result = calculate_dps(items, "melee")

        assert result["dps"] == 0.0
        assert result["max_hit"] == 0
        assert result["attack_speed"] == 0

    def test_melee_dps_with_basic_weapon(self):
        """Test melee DPS calculation with basic weapon."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["dps"] > 0
        assert result["max_hit"] > 0
        assert result["attack_speed"] == 4
        assert result["total_attack_bonus"] == 82
        assert result["total_strength_bonus"] == 82
        assert result["details"]["combat_style"] == "melee"
        assert result["details"]["attack_type"] == "slash"

    def test_melee_dps_with_full_gear(self):
        """Test melee DPS with multiple gear pieces."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )
        helm = Item(
            id=1163,
            name="Rune full helm",
            attack_stab=0,
            attack_slash=0,
            attack_crush=0,
            melee_strength=0,
            attack_speed=4,
        )
        body = Item(
            id=1127,
            name="Rune platebody",
            attack_stab=0,
            attack_slash=0,
            attack_crush=0,
            melee_strength=0,
            attack_speed=4,
        )

        items = {"weapon": weapon, "head": helm, "body": body}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["dps"] > 0
        assert result["total_attack_bonus"] == 82
        assert result["total_strength_bonus"] == 82

    def test_melee_dps_attack_type_stab(self):
        """Test melee DPS with stab attack type."""
        weapon = Item(
            id=12904,
            name="Abyssal dagger",
            attack_stab=75,
            attack_slash=75,
            attack_crush=-4,
            melee_strength=75,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="stab")

        assert result["total_attack_bonus"] == 75
        assert result["details"]["attack_type"] == "stab"

    def test_melee_dps_attack_type_crush(self):
        """Test melee DPS with crush attack type."""
        weapon = Item(
            id=7158,
            name="Dragon mace",
            attack_stab=0,
            attack_slash=0,
            attack_crush=67,
            melee_strength=66,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="crush")

        assert result["total_attack_bonus"] == 67
        assert result["details"]["attack_type"] == "crush"

    def test_melee_dps_no_attack_type_uses_max(self):
        """Test melee DPS without attack type uses max of stab/slash/crush."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type=None)

        assert result["total_attack_bonus"] == 82  # Max of 82, 82, 0
        assert result["details"]["attack_type"] is None

    def test_ranged_dps_basic(self):
        """Test ranged DPS calculation."""
        weapon = Item(
            id=861,
            name="Magic shortbow",
            attack_ranged=69,
            ranged_strength=0,
            attack_speed=3,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "ranged")

        assert result["dps"] > 0
        assert result["max_hit"] > 0
        assert result["total_attack_bonus"] == 69
        assert result["total_strength_bonus"] == 0
        assert result["details"]["combat_style"] == "ranged"

    def test_ranged_dps_with_armor(self):
        """Test ranged DPS with armor bonuses."""
        weapon = Item(
            id=861,
            name="Magic shortbow",
            attack_ranged=69,
            ranged_strength=0,
            attack_speed=3,
        )
        helm = Item(
            id=1169,
            name="Leather cowl",
            attack_ranged=2,
            ranged_strength=0,
            attack_speed=3,
        )

        items = {"weapon": weapon, "head": helm}
        result = calculate_dps(items, "ranged")

        assert result["total_attack_bonus"] == 71  # 69 + 2
        assert result["total_strength_bonus"] == 0

    def test_magic_dps_basic(self):
        """Test magic DPS calculation."""
        weapon = Item(
            id=1379,
            name="Staff of fire",
            attack_magic=10,
            magic_damage=0,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "magic")

        assert result["dps"] > 0
        assert result["max_hit"] == 30  # Placeholder value
        assert result["total_attack_bonus"] == 10
        assert result["details"]["combat_style"] == "magic"

    def test_magic_dps_with_damage_bonus(self):
        """Test magic DPS with magic damage bonus."""
        weapon = Item(
            id=1379,
            name="Staff of fire",
            attack_magic=10,
            magic_damage=0,
            attack_speed=4,
        )
        amulet = Item(
            id=12002,
            name="Occult necklace",
            attack_magic=12,
            magic_damage=10,
            attack_speed=4,
        )

        items = {"weapon": weapon, "neck": amulet}
        result = calculate_dps(items, "magic")

        assert result["total_attack_bonus"] == 22  # 10 + 12
        # For magic, total_strength_bonus uses total_ranged_strength (which is 0 for magic)
        # The code doesn't expose total_magic_damage in total_strength_bonus field
        assert result["total_strength_bonus"] == 0

    def test_custom_player_stats(self):
        """Test DPS calculation with custom player stats."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        player_stats = {"attack": 70, "strength": 70, "ranged": 1, "magic": 1}
        result = calculate_dps(items, "melee", attack_type="slash", player_stats=player_stats)

        assert result["dps"] > 0
        assert result["details"]["player_stats"] == player_stats

    def test_default_player_stats(self):
        """Test that default player stats (99) are used when not provided."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["details"]["player_stats"]["attack"] == 99
        assert result["details"]["player_stats"]["strength"] == 99

    def test_attack_speed_conversion(self):
        """Test that attack speed is converted from ticks to seconds."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["attack_speed"] == 4  # ticks
        assert result["attack_speed_seconds"] == 2.4  # 4 * 0.6

    def test_attack_speed_default(self):
        """Test that default attack speed (4 ticks) is used when not set."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=None,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["attack_speed"] == 4  # Default
        assert result["attack_speed_seconds"] == 2.4

    def test_accuracy_calculation(self):
        """Test that accuracy is calculated and returned as percentage."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert 0 <= result["accuracy"] <= 100
        assert isinstance(result["accuracy"], (int, float))

    def test_none_items_ignored(self):
        """Test that None items in loadout are ignored."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon, "head": None, "body": None, "legs": None}
        result = calculate_dps(items, "melee", attack_type="slash")

        assert result["dps"] > 0
        assert result["total_attack_bonus"] == 82  # Only weapon counted

    def test_invalid_combat_style(self):
        """Test that invalid combat style returns zero DPS."""
        weapon = Item(
            id=4151,
            name="Abyssal whip",
            attack_stab=82,
            attack_slash=82,
            attack_crush=0,
            melee_strength=82,
            attack_speed=4,
        )

        items = {"weapon": weapon}
        result = calculate_dps(items, "invalid_style")

        assert result["dps"] == 0.0
        assert result["max_hit"] == 0
        assert result["accuracy"] == 0.0
