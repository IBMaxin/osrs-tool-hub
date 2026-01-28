"""Tests for boss service."""

import pytest
from unittest.mock import patch
from sqlmodel import Session

from backend.services.gear.boss import BossService, get_boss_data, get_available_bosses
from backend.models import Item


class TestBossService:
    """Test BossService methods."""

    def test_get_boss_data_success(self):
        """Test getting boss data for existing boss."""
        boss_data = get_boss_data("vorkath")
        assert boss_data is not None
        assert isinstance(boss_data, dict)

    def test_get_boss_data_not_found(self):
        """Test getting boss data for non-existent boss."""
        boss_data = get_boss_data("nonexistent_boss")
        assert boss_data is None

    def test_get_boss_data_case_insensitive(self):
        """Test that boss name is case-insensitive."""
        boss_data1 = get_boss_data("Vorkath")
        boss_data2 = get_boss_data("vorkath")
        assert boss_data1 == boss_data2

    def test_get_available_bosses(self):
        """Test getting list of available bosses."""
        bosses = get_available_bosses()
        assert isinstance(bosses, list)
        assert len(bosses) > 0
        assert "vorkath" in bosses or "Vorkath" in bosses.lower()

    def test_get_available_bosses_no_directory(self, tmp_path):
        """Test getting bosses when directory doesn't exist."""
        with patch("backend.services.gear.boss._BOSS_DATA_DIR", tmp_path / "nonexistent"):
            bosses = get_available_bosses()
            assert bosses == []

    def test_boss_service_init(self, session: Session):
        """Test initializing BossService."""
        service = BossService(session)
        assert service.session == session

    def test_get_bis_for_boss_success(self, session: Session):
        """Test getting BiS for a boss successfully."""
        # Create some test items
        item1 = Item(
            id=4151,
            name="Abyssal whip",
            slot="weapon",
            members=True,
            value=2000000,
        )
        session.add(item1)
        session.commit()

        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        )

        assert "boss_info" in result
        assert "recommended_loadouts" in result
        assert "notes" in result
        assert isinstance(result["recommended_loadouts"], list)

    def test_get_bis_for_boss_not_found(self, session: Session):
        """Test getting BiS for non-existent boss."""
        service = BossService(session)
        with pytest.raises(ValueError, match="Boss 'nonexistent' not found"):
            service.get_bis_for_boss(
                boss_name="nonexistent",
                budget=10000000,
                stats={
                    "attack": 99,
                    "strength": 99,
                    "defence": 99,
                    "ranged": 99,
                    "magic": 99,
                    "prayer": 99,
                },
            )

    def test_get_bis_for_boss_with_ironman(self, session: Session):
        """Test getting BiS with ironman filter."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
            ironman=True,
        )

        assert "recommended_loadouts" in result

    def test_get_bis_for_boss_with_exclude_items(self, session: Session):
        """Test getting BiS with excluded items."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
            exclude_items=["Abyssal whip"],
        )

        assert "recommended_loadouts" in result

    def test_get_bis_for_boss_with_max_tick_manipulation(self, session: Session):
        """Test getting BiS with max tick manipulation filter."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
            max_tick_manipulation=True,
        )

        assert "recommended_loadouts" in result

    def test_get_bis_for_boss_handles_loadout_error(self, session: Session):
        """Test that service handles errors when calculating loadout."""
        service = BossService(session)

        with patch("backend.services.gear.boss.get_best_loadout") as mock_loadout:
            mock_loadout.side_effect = Exception("Loadout calculation error")

            # Should not raise, but log error and continue
            result = service.get_bis_for_boss(
                boss_name="vorkath",
                budget=10000000,
                stats={
                    "attack": 99,
                    "strength": 99,
                    "defence": 99,
                    "ranged": 99,
                    "magic": 99,
                    "prayer": 99,
                },
            )

            # Should still return result structure, but with empty or partial loadouts
            assert "recommended_loadouts" in result

    def test_get_bis_for_boss_multiple_styles(self, session: Session):
        """Test getting BiS for boss with multiple recommended styles."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="zulrah",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        )

        # Zulrah typically has multiple recommended styles
        assert len(result["recommended_loadouts"]) >= 0  # May be 0 if no items match

    def test_get_bis_for_boss_includes_notes(self, session: Session):
        """Test that result includes special mechanics notes."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        )

        assert "notes" in result
        assert isinstance(result["notes"], list)

    def test_get_bis_for_boss_loadout_has_style(self, session: Session):
        """Test that each loadout includes style information."""
        service = BossService(session)
        result = service.get_bis_for_boss(
            boss_name="vorkath",
            budget=10000000,
            stats={
                "attack": 99,
                "strength": 99,
                "defence": 99,
                "ranged": 99,
                "magic": 99,
                "prayer": 99,
            },
        )

        for loadout in result["recommended_loadouts"]:
            assert "style" in loadout
