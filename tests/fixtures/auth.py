"""
Authentication fixtures for integration tests
"""
import pytest
from typing import Dict
import httpx
from fastapi.testclient import TestClient


class AuthenticatedClient:
    """HTTP client with authentication capabilities"""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.client = httpx.Client(base_url=base_url)

    def login(self, email: str, password: str = "ooo", auth_type: str = "candidate") -> "AuthenticatedClient":
        """Login and store authentication token"""
        login_data = {
            "username": email,  # FastAPI OAuth2 uses 'username' field
            "password": password
        }

        # Use appropriate auth endpoint based on auth_type
        endpoint = f"/{auth_type}/auth/login"
        response = self.client.post(endpoint, data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")
            # Set Authorization header for future requests
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
        else:
            raise Exception(f"Login failed: {response.text}")

        return self

    def get(self, url: str, **kwargs) -> httpx.Response:
        """HTTP GET with authentication"""
        return self.client.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        """HTTP POST with authentication"""
        return self.client.post(url, **kwargs)

    def put(self, url: str, **kwargs) -> httpx.Response:
        """HTTP PUT with authentication"""
        return self.client.put(url, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        """HTTP DELETE with authentication"""
        return self.client.delete(url, **kwargs)

    def close(self):
        """Close the HTTP client"""
        self.client.close()


@pytest.fixture
def authenticated_client():
    """Provide an authenticated HTTP client"""
    client = AuthenticatedClient()
    yield client
    client.close()


class TestAuthMixin:
    """Mixin to provide authentication helpers to test classes"""

    def as_admin(self, email: str = "admin@test.com") -> AuthenticatedClient:
        """Create authenticated client as admin user"""
        client = AuthenticatedClient()
        return client.login(email, auth_type="admin")

    def as_candidate(self, email: str = "ooo@ooo.es") -> AuthenticatedClient:
        """Create authenticated client as candidate user"""
        client = AuthenticatedClient()
        return client.login(email, auth_type="candidate")

    def as_user(self, email: str = "ooo@ooo.es") -> AuthenticatedClient:
        """Create authenticated client as regular user (alias for as_candidate)"""
        return self.as_candidate(email)