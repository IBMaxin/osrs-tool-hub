"""Tests for boss BiS API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.database import get_session

# Create test engine
test_engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


def get_test_session():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Set up test database before each test."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)
    test_engine.dispose()


class TestGetBossBiS:
    """Test GET /api/v1/gear/bis/{boss_name} endpoint."""

    def test_get_boss_bis_validation_error(self):
        """Test GET endpoint validation (stats dict can't be passed as query param)."""
        # The GET endpoint expects stats as dict which doesn't work well as query param
        # This test verifies validation error handling
        response = client.get(
            "/api/v1/gear/bis/vorkath",
            params={"budget": 10000000},
        )
        # Should return validation error since stats is required
        assert response.status_code == 422


class TestPostBossBiS:
    """Test POST /api/v1/gear/bis/{boss_name} endpoint."""

    def test_post_boss_bis_success(self):
        """Test calculating BiS with POST request."""
        with patch("backend.api.v1.gear.routes.boss.BossService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_bis_for_boss.return_value = {
                "boss_info": {"name": "Vorkath"},
                "recommended_loadouts": [{"style": "ranged"}],
                "notes": [],
            }

            payload = {
                "budget": 10000000,
                "stats": {"attack": 99, "strength": 99, "defence": 99, "ranged": 99, "magic": 99, "prayer": 99},
                "ironman": False,
            }

            response = client.post("/api/v1/gear/bis/vorkath", json=payload)

            assert response.status_code == 200
            data = response.json()
            assert "boss_info" in data

    def test_post_boss_bis_with_constraints(self):
        """Test calculating BiS with all constraints."""
        with patch("backend.api.v1.gear.routes.boss.BossService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_bis_for_boss.return_value = {
                "boss_info": {"name": "Vorkath"},
                "recommended_loadouts": [],
                "notes": [],
            }

            payload = {
                "budget": 10000000,
                "stats": {"attack": 99},
                "ironman": True,
                "exclude_items": ["Abyssal whip"],
                "max_tick_manipulation": True,
            }

            response = client.post("/api/v1/gear/bis/vorkath", json=payload)

            assert response.status_code == 200
            call_kwargs = mock_service.get_bis_for_boss.call_args[1]
            assert call_kwargs["ironman"] is True
            assert call_kwargs["exclude_items"] == ["Abyssal whip"]
            assert call_kwargs["max_tick_manipulation"] is True

    def test_post_boss_bis_boss_not_found(self):
        """Test POST with non-existent boss."""
        with patch("backend.api.v1.gear.routes.boss.BossService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_bis_for_boss.side_effect = ValueError("Boss not found")

            payload = {
                "budget": 10000000,
                "stats": {"attack": 99},
            }

            response = client.post("/api/v1/gear/bis/nonexistent", json=payload)

            assert response.status_code == 404

    def test_post_boss_bis_service_error(self):
        """Test handling service errors in POST."""
        with patch("backend.api.v1.gear.routes.boss.BossService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_bis_for_boss.side_effect = Exception("Service error")

            payload = {
                "budget": 10000000,
                "stats": {"attack": 99},
            }

            response = client.post("/api/v1/gear/bis/vorkath", json=payload)

            assert response.status_code == 400


class TestListBosses:
    """Test GET /api/v1/gear/bosses endpoint."""

    def test_list_bosses_success(self):
        """Test listing available bosses."""
        with patch("backend.api.v1.gear.routes.boss.get_available_bosses") as mock_get_bosses:
            mock_get_bosses.return_value = ["vorkath", "zulrah", "gwd"]

            response = client.get("/api/v1/gear/bosses")

            assert response.status_code == 200
            data = response.json()
            assert "bosses" in data
            assert isinstance(data["bosses"], list)
            assert len(data["bosses"]) == 3

    def test_list_bosses_empty(self):
        """Test listing bosses when none available."""
        with patch("backend.api.v1.gear.routes.boss.get_available_bosses") as mock_get_bosses:
            mock_get_bosses.return_value = []

            response = client.get("/api/v1/gear/bosses")

            assert response.status_code == 200
            data = response.json()
            assert data["bosses"] == []
