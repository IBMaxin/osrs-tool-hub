"""Unit tests for gear set CRUD endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock, AsyncMock

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


class TestCreateGearSet:
    """Test POST /api/v1/gear endpoint."""

    def test_create_gear_set_success(self):
        """Test creating a gear set successfully."""
        payload = {
            "name": "Test Melee Set",
            "description": "A test melee gear set",
            "items": {4151: 1, 11802: 1},
        }

        # Mock the service to return a gear set
        mock_gear_set = MagicMock()
        mock_gear_set.id = 1
        mock_gear_set.name = "Test Melee Set"
        mock_gear_set.description = "A test melee gear set"
        mock_gear_set.items = '{"4151": 1, "11802": 1}'  # JSON string as stored in DB
        mock_gear_set.total_cost = 1000000
        from datetime import datetime

        mock_gear_set.created_at = datetime(2024, 1, 1)
        mock_gear_set.updated_at = datetime(2024, 1, 1)

        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.create_gear_set = AsyncMock(return_value=mock_gear_set)

            response = client.post("/api/v1/gear", json=payload)

            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test Melee Set"
            assert data["description"] == "A test melee gear set"

    def test_create_gear_set_validation_error(self):
        """Test creating a gear set with invalid data."""
        payload = {
            "name": "",  # Empty name
            "items": {},
        }

        response = client.post("/api/v1/gear", json=payload)

        assert response.status_code == 422  # Validation error

    def test_create_gear_set_service_error(self):
        """Test creating a gear set when service raises error."""
        payload = {
            "name": "Test Set",
            "items": {4151: 1},
        }

        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.create_gear_set = AsyncMock(side_effect=Exception("Service error"))

            # Exception will propagate (no global handler for generic Exception)
            # This tests that unhandled exceptions are not silently swallowed
            with pytest.raises(Exception, match="Service error"):
                client.post("/api/v1/gear", json=payload)


class TestGetGearSets:
    """Test GET /api/v1/gear endpoint."""

    def test_get_all_gear_sets_success(self):
        """Test getting all gear sets successfully."""
        from datetime import datetime

        mock_gear_set1 = MagicMock()
        mock_gear_set1.id = 1
        mock_gear_set1.name = "Set 1"
        mock_gear_set1.description = None
        mock_gear_set1.items = '{"4151": 1}'  # JSON string
        mock_gear_set1.total_cost = 1000000
        mock_gear_set1.created_at = datetime(2024, 1, 1)
        mock_gear_set1.updated_at = datetime(2024, 1, 1)

        mock_gear_set2 = MagicMock()
        mock_gear_set2.id = 2
        mock_gear_set2.name = "Set 2"
        mock_gear_set2.description = None
        mock_gear_set2.items = '{"11802": 1}'  # JSON string
        mock_gear_set2.total_cost = 2000000
        mock_gear_set2.created_at = datetime(2024, 1, 1)
        mock_gear_set2.updated_at = datetime(2024, 1, 1)

        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_all_gear_sets.return_value = [mock_gear_set1, mock_gear_set2]

            response = client.get("/api/v1/gear")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2

    def test_get_all_gear_sets_empty(self):
        """Test getting all gear sets when none exist."""
        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_all_gear_sets.return_value = []

            response = client.get("/api/v1/gear")

            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 0


class TestGetGearSetById:
    """Test GET /api/v1/gear/{gear_set_id} endpoint."""

    def test_get_gear_set_by_id_success(self):
        """Test getting a gear set by ID successfully."""
        from datetime import datetime

        mock_gear_set = MagicMock()
        mock_gear_set.id = 1
        mock_gear_set.name = "Test Set"
        mock_gear_set.description = None
        mock_gear_set.items = '{"4151": 1}'  # JSON string
        mock_gear_set.total_cost = 1000000
        mock_gear_set.created_at = datetime(2024, 1, 1)
        mock_gear_set.updated_at = datetime(2024, 1, 1)

        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_gear_set_by_id.return_value = mock_gear_set

            response = client.get("/api/v1/gear/1")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "Test Set"

    def test_get_gear_set_by_id_not_found(self):
        """Test getting a gear set that doesn't exist."""
        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.get_gear_set_by_id.return_value = None

            response = client.get("/api/v1/gear/99999")

            assert response.status_code == 404
            data = response.json()
            # Check for error detail in either 'detail' or 'error.message'
            error_msg = data.get("detail", data.get("error", {}).get("message", ""))
            assert "not found" in str(error_msg).lower()


class TestDeleteGearSet:
    """Test DELETE /api/v1/gear/{gear_set_id} endpoint."""

    def test_delete_gear_set_success(self):
        """Test deleting a gear set successfully."""
        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.delete_gear_set.return_value = True

            response = client.delete("/api/v1/gear/1")

            assert response.status_code == 204

    def test_delete_gear_set_not_found(self):
        """Test deleting a gear set that doesn't exist."""
        with patch("backend.api.v1.gear.routes.gear_sets.GearService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.delete_gear_set.return_value = False

            response = client.delete("/api/v1/gear/99999")

            assert response.status_code == 404
            data = response.json()
            # Check for error detail in either 'detail' or 'error.message'
            error_msg = data.get("detail", data.get("error", {}).get("message", ""))
            assert "not found" in str(error_msg).lower()
