"""Unit tests for slayer gear integration."""

import pytest
from unittest.mock import patch, MagicMock
from sqlmodel import Session

from backend.services.gear.slayer_integration import suggest_slayer_gear, _parse_attack_style
from backend.models import Monster, SlayerTask, SlayerMaster


class TestSuggestSlayerGear:
    """Test suggest_slayer_gear function."""

    def test_suggest_slayer_gear_task_not_found(self, session: Session):
        """Test suggest_slayer_gear returns error when task not found."""
        result = suggest_slayer_gear(session, task_id=99999, stats={"attack": 70, "strength": 70})
        assert "error" in result
        assert result["error"] == "Task not found"

    def test_suggest_slayer_gear_monster_not_found(
        self, session: Session, sample_slayer_tasks
    ):
        """Test suggest_slayer_gear returns error when monster not found."""
        task = sample_slayer_tasks[0]
        # Delete the monster
        monster = session.get(Monster, task.monster_id)
        if monster:
            session.delete(monster)
            session.commit()

        result = suggest_slayer_gear(session, task_id=task.id, stats={"attack": 70, "strength": 70})
        assert "error" in result
        assert result["error"] == "Monster not found"

    def test_suggest_slayer_gear_invalid_combat_style(
        self, session: Session, sample_slayer_tasks, sample_monsters
    ):
        """Test suggest_slayer_gear returns error for invalid combat style."""
        task = sample_slayer_tasks[0]
        result = suggest_slayer_gear(
            session,
            task_id=task.id,
            stats={"attack": 70, "strength": 70},
            combat_style="invalid",
        )
        assert "error" in result
        assert "Invalid combat style" in result["error"]

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_with_combat_style_override(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear with combat style override."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": ["Slash"], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        result = suggest_slayer_gear(
            session,
            task_id=task.id,
            stats={"attack": 70, "strength": 70, "ranged": 70},
            combat_style="ranged",
        )

        assert "error" not in result
        assert result["combat_style"] == "ranged"
        assert result["task_id"] == task.id

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_melee_with_stab_weakness(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear determines stab attack type from weakness."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": ["Stab"], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        result = suggest_slayer_gear(
            session,
            task_id=task.id,
            stats={"attack": 70, "strength": 70},
            combat_style="melee",
        )

        assert result["attack_type"] == "stab"
        mock_get_best_loadout.assert_called()
        call_kwargs = mock_get_best_loadout.call_args[1]
        assert call_kwargs["attack_type"] == "stab"

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_parses_combat_style_from_task_data(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear parses combat style from task data."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {
            "weakness": [],
            "attack_style": "Magic (Burst/Barrage)",
        }
        mock_get_best_loadout.return_value = {"loadout": "test"}

        result = suggest_slayer_gear(
            session, task_id=task.id, stats={"magic": 70, "attack": 70}
        )

        assert result["combat_style"] == "magic"

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_tier_budgets_based_on_level(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear creates tier budgets based on level."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": [], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        # Test with level 85
        result = suggest_slayer_gear(
            session, task_id=task.id, stats={"attack": 85, "strength": 85}
        )

        assert len(result["tier_loadouts"]) >= 3  # Should have 70+, 75+, 80+, 85+ tiers
        assert any(t["tier"] == "85+" for t in result["tier_loadouts"])

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_low_level_uses_current_tier(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear uses Current tier for low levels."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": [], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        result = suggest_slayer_gear(
            session, task_id=task.id, stats={"attack": 50, "strength": 50}, budget=1_000_000
        )

        assert len(result["tier_loadouts"]) == 1
        assert result["tier_loadouts"][0]["tier"] == "Current"

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_includes_quests_and_achievements(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear passes quests and achievements to get_best_loadout."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": [], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        quests = {"Dragon Slayer", "Monkey Madness"}
        achievements = {"Achievement 1"}

        suggest_slayer_gear(
            session,
            task_id=task.id,
            stats={"attack": 70, "strength": 70},
            quests_completed=quests,
            achievements_completed=achievements,
        )

        call_kwargs = mock_get_best_loadout.call_args[1]
        assert call_kwargs["quests_completed"] == quests
        assert call_kwargs["achievements_completed"] == achievements

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_ironman_mode(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear passes ironman flag."""
        task = sample_slayer_tasks[0]
        mock_task_data.get.return_value = {"weakness": [], "attack_style": "Melee"}
        mock_get_best_loadout.return_value = {"loadout": "test"}

        suggest_slayer_gear(
            session, task_id=task.id, stats={"attack": 70, "strength": 70}, ironman=True
        )

        call_kwargs = mock_get_best_loadout.call_args[1]
        assert call_kwargs["ironman"] is True

    @patch("backend.services.gear.slayer_integration.get_best_loadout")
    @patch("backend.services.gear.slayer_integration.SLAYER_TASK_DATA")
    def test_suggest_slayer_gear_returns_complete_response(
        self,
        mock_task_data,
        mock_get_best_loadout,
        session: Session,
        sample_slayer_tasks,
        sample_monsters,
    ):
        """Test suggest_slayer_gear returns complete response structure."""
        task = sample_slayer_tasks[0]
        monster = sample_monsters[0]
        mock_task_data.get.return_value = {
            "weakness": ["Slash"],
            "attack_style": "Melee (Slash)",
        }
        mock_get_best_loadout.return_value = {"loadout": "test"}

        result = suggest_slayer_gear(
            session, task_id=task.id, stats={"attack": 70, "strength": 70}
        )

        assert "task_id" in result
        assert "monster_name" in result
        assert "category" in result
        assert "combat_style" in result
        assert "attack_type" in result
        assert "weakness" in result
        assert "attack_style_recommendation" in result
        assert "tier_loadouts" in result
        assert "primary_loadout" in result
        assert result["monster_name"] == monster.name
        assert result["category"] == task.category


class TestParseAttackStyle:
    """Test _parse_attack_style function."""

    def test_parse_attack_style_magic_keywords(self):
        """Test _parse_attack_style detects magic from keywords."""
        combat_style, attack_type = _parse_attack_style("Magic (Burst/Barrage)", [])
        assert combat_style == "magic"
        assert attack_type is None

    def test_parse_attack_style_ranged_keywords(self):
        """Test _parse_attack_style detects ranged from keywords."""
        combat_style, attack_type = _parse_attack_style("Ranged (Blowpipe)", [])
        assert combat_style == "ranged"
        assert attack_type is None

    def test_parse_attack_style_melee_default(self):
        """Test _parse_attack_style defaults to melee."""
        combat_style, attack_type = _parse_attack_style("Melee", [])
        assert combat_style == "melee"

    def test_parse_attack_style_melee_stab_from_weakness(self):
        """Test _parse_attack_style determines stab from weakness."""
        combat_style, attack_type = _parse_attack_style("Melee", ["Stab"])
        assert combat_style == "melee"
        assert attack_type == "stab"

    def test_parse_attack_style_melee_slash_from_weakness(self):
        """Test _parse_attack_style determines slash from weakness."""
        combat_style, attack_type = _parse_attack_style("Melee", ["Slash"])
        assert combat_style == "melee"
        assert attack_type == "slash"

    def test_parse_attack_style_melee_crush_from_weakness(self):
        """Test _parse_attack_style determines crush from weakness."""
        combat_style, attack_type = _parse_attack_style("Melee", ["Crush"])
        assert combat_style == "melee"
        assert attack_type == "crush"

    def test_parse_attack_style_melee_stab_from_string(self):
        """Test _parse_attack_style determines stab from attack style string."""
        combat_style, attack_type = _parse_attack_style("Melee (Stab)", [])
        assert combat_style == "melee"
        assert attack_type == "stab"

    def test_parse_attack_style_melee_slash_from_string(self):
        """Test _parse_attack_style determines slash from attack style string."""
        combat_style, attack_type = _parse_attack_style("Melee (Slash)", [])
        assert combat_style == "melee"
        assert attack_type == "slash"

    def test_parse_attack_style_melee_crush_from_string(self):
        """Test _parse_attack_style determines crush from attack style string."""
        combat_style, attack_type = _parse_attack_style("Melee (Crush)", [])
        assert combat_style == "melee"
        assert attack_type == "crush"

    def test_parse_attack_style_weakness_priority_over_string(self):
        """Test _parse_attack_style prioritizes weakness over string."""
        combat_style, attack_type = _parse_attack_style("Melee (Crush)", ["Stab"])
        assert combat_style == "melee"
        assert attack_type == "stab"  # Weakness takes priority

    def test_parse_attack_style_case_insensitive_weakness(self):
        """Test _parse_attack_style handles case-insensitive weakness."""
        combat_style, attack_type = _parse_attack_style("Melee", ["STAB", "Slash"])
        assert combat_style == "melee"
        assert attack_type == "stab"  # First match wins
