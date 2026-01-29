"""Unit tests for account progression utilities."""

from unittest.mock import patch
from sqlmodel import Session

from backend.services.gear.progression.account_progression import get_global_upgrade_path


class TestGetGlobalUpgradePath:
    """Test get_global_upgrade_path function."""

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_single_style(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path with single style."""
        mock_get_upgrade_path.return_value = {
            "recommended_upgrades": [
                {"slot": "weapon", "cost": 1000000, "dps_per_gp": 0.5},
                {"slot": "head", "cost": 500000, "dps_per_gp": 0.3},
            ]
        }

        result = get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1, "head": 2}},
            bank_value=2000000,
            stats={"attack": 70, "strength": 70},
        )

        assert "recommended_upgrades" in result
        assert "upgrades_by_style" in result
        assert "total_cost" in result
        assert "bank_value" in result
        assert "remaining_budget" in result
        assert len(result["recommended_upgrades"]) == 2
        assert all("style" in u for u in result["recommended_upgrades"])

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_multiple_styles(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path with multiple styles."""
        def side_effect(session, current_loadout, combat_style, **kwargs):
            if combat_style == "melee":
                return {
                    "recommended_upgrades": [
                        {"slot": "weapon", "cost": 1000000, "dps_per_gp": 0.5}
                    ]
                }
            elif combat_style == "ranged":
                return {
                    "recommended_upgrades": [
                        {"slot": "weapon", "cost": 800000, "dps_per_gp": 0.6}
                    ]
                }
            return {"recommended_upgrades": []}

        mock_get_upgrade_path.side_effect = side_effect

        result = get_global_upgrade_path(
            session=session,
            current_gear={
                "melee": {"weapon": 1},
                "ranged": {"weapon": 2},
            },
            bank_value=2000000,
            stats={"attack": 70, "strength": 70, "ranged": 70},
        )

        assert len(result["recommended_upgrades"]) == 2
        # Should be sorted by dps_per_gp (ranged first with 0.6)
        assert result["recommended_upgrades"][0]["dps_per_gp"] == 0.6
        assert result["recommended_upgrades"][1]["dps_per_gp"] == 0.5

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_adds_global_priority(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path adds global priority numbers."""
        mock_get_upgrade_path.return_value = {
            "recommended_upgrades": [
                {"slot": "weapon", "cost": 1000000, "dps_per_gp": 0.5},
                {"slot": "head", "cost": 500000, "dps_per_gp": 0.3},
            ]
        }

        result = get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1, "head": 2}},
            bank_value=2000000,
            stats={"attack": 70, "strength": 70},
        )

        assert result["recommended_upgrades"][0]["global_priority"] == 1
        assert result["recommended_upgrades"][1]["global_priority"] == 2

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_respects_bank_value(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path respects bank value limit."""
        mock_get_upgrade_path.return_value = {
            "recommended_upgrades": [
                {"slot": "weapon", "cost": 1000000, "dps_per_gp": 0.5},
                {"slot": "head", "cost": 500000, "dps_per_gp": 0.3},
                {"slot": "body", "cost": 2000000, "dps_per_gp": 0.2},
            ]
        }

        result = get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1, "head": 2, "body": 3}},
            bank_value=1200000,  # Only enough for first upgrade (1M)
            stats={"attack": 70, "strength": 70},
        )

        # Only first upgrade (1M) fits in 1.2M budget
        assert len(result["recommended_upgrades"]) == 1
        assert result["total_cost"] == 1000000
        assert result["remaining_budget"] == 200000

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_passes_attack_type_for_melee(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path passes attack_type only for melee."""
        mock_get_upgrade_path.return_value = {"recommended_upgrades": []}

        get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1}, "ranged": {"weapon": 2}},
            bank_value=1000000,
            stats={"attack": 70, "strength": 70, "ranged": 70},
            attack_type="stab",
        )

        # Check melee call has attack_type
        melee_call = [c for c in mock_get_upgrade_path.call_args_list if c[1]["combat_style"] == "melee"][0]
        assert melee_call[1]["attack_type"] == "stab"

        # Check ranged call has no attack_type
        ranged_call = [c for c in mock_get_upgrade_path.call_args_list if c[1]["combat_style"] == "ranged"][0]
        assert ranged_call[1]["attack_type"] is None

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_passes_quests_and_achievements(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path passes quests and achievements."""
        mock_get_upgrade_path.return_value = {"recommended_upgrades": []}

        quests = {"Dragon Slayer"}
        achievements = {"Achievement 1"}

        get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1}},
            bank_value=1000000,
            stats={"attack": 70, "strength": 70},
            quests_completed=quests,
            achievements_completed=achievements,
        )

        call_kwargs = mock_get_upgrade_path.call_args[1]
        assert call_kwargs["quests_completed"] == quests
        assert call_kwargs["achievements_completed"] == achievements

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_handles_unlocked_content(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path handles unlocked_content parameter."""
        mock_get_upgrade_path.return_value = {"recommended_upgrades": []}

        get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1}},
            bank_value=1000000,
            stats={"attack": 70, "strength": 70},
            unlocked_content=["ToA", "GWD"],
        )

        # Function should handle unlocked_content (currently no-op but should not error)
        assert mock_get_upgrade_path.called

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_skips_empty_loadouts(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path skips styles with empty loadouts."""
        get_global_upgrade_path(
            session=session,
            current_gear={"melee": {}, "ranged": {"weapon": 1}},  # melee is empty
            bank_value=1000000,
            stats={"attack": 70, "strength": 70, "ranged": 70},
        )

        # Should only call get_upgrade_path for ranged (melee skipped)
        assert mock_get_upgrade_path.call_count == 1
        assert mock_get_upgrade_path.call_args[1]["combat_style"] == "ranged"

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_handles_exceptions(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path handles exceptions gracefully."""
        def side_effect(session, current_loadout, combat_style, **kwargs):
            if combat_style == "melee":
                raise ValueError("Test error")
            return {"recommended_upgrades": [{"slot": "weapon", "cost": 1000000, "dps_per_gp": 0.5}]}

        mock_get_upgrade_path.side_effect = side_effect

        result = get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1}, "ranged": {"weapon": 2}},
            bank_value=1000000,
            stats={"attack": 70, "strength": 70, "ranged": 70},
        )

        # Should continue with ranged despite melee error
        assert "ranged" in result["upgrades_by_style"]
        assert "melee" not in result["upgrades_by_style"]
        assert len(result["recommended_upgrades"]) == 1

    @patch("backend.services.gear.progression.account_progression.get_upgrade_path")
    def test_get_global_upgrade_path_no_upgrades(
        self, mock_get_upgrade_path, session: Session
    ):
        """Test get_global_upgrade_path with no upgrades."""
        mock_get_upgrade_path.return_value = {"recommended_upgrades": []}

        result = get_global_upgrade_path(
            session=session,
            current_gear={"melee": {"weapon": 1}},
            bank_value=1000000,
            stats={"attack": 70, "strength": 70},
        )

        assert len(result["recommended_upgrades"]) == 0
        assert result["total_cost"] == 0
        assert result["remaining_budget"] == 1000000
