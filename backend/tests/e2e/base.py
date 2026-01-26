"""Base test classes for E2E tests."""
from typing import Dict, Any
from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest

from backend.tests.e2e.helpers import assert_successful_response, assert_error_response


class BaseE2ETest:
    """Base class for E2E tests with common utilities."""
    
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, session: Session):
        """Setup for each test."""
        self.client = client
        self.session = session
    
    def get(self, path: str, expected_status: int = 200) -> Dict[str, Any]:
        """Make GET request and assert success."""
        response = self.client.get(path)
        return assert_successful_response(response, expected_status)
    
    def post(self, path: str, json_data: Dict[str, Any], expected_status: int = 200) -> Dict[str, Any]:
        """Make POST request and assert success."""
        response = self.client.post(path, json=json_data)
        return assert_successful_response(response, expected_status)
    
    def delete(self, path: str, expected_status: int = 204) -> None:
        """Make DELETE request and assert success."""
        response = self.client.delete(path)
        assert response.status_code == expected_status
    
    def assert_error(self, path: str, method: str = "GET", expected_status: int = 404, **kwargs) -> Dict[str, Any]:
        """Make request and assert error response."""
        if method == "GET":
            response = self.client.get(path)
        elif method == "POST":
            response = self.client.post(path, **kwargs)
        elif method == "DELETE":
            response = self.client.delete(path)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return assert_error_response(response, expected_status)
