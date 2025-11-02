"""
Integration tests for Company User Management endpoints
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime

from adapters.http.company.routers.company_user_router import router as company_user_router
from adapters.http.company.schemas.company_user_response import CompanyUserResponse
from adapters.http.company.schemas.company_user_invitation_request import AssignRoleRequest
from core.container import Container


class TestCompanyUserManagementEndpoints:
    """Tests for company user management endpoints"""

    @pytest.fixture
    def mock_controller(self):
        """Mock controller for company user operations"""
        return Mock()

    @pytest.fixture
    def app(self, mock_controller):
        """Create FastAPI app with mocked controller"""
        from dependency_injector import providers
        
        app = FastAPI()
        app.include_router(company_user_router)
        
        # Override container provider with mock
        container = Container()
        container.company_user_controller.override(
            providers.Singleton(lambda: mock_controller)
        )
        
        # Wire the container to the router
        container.wire(modules=[
            "adapters.http.company.routers.company_user_router"
        ])
        
        app.container = container
        
        yield app
        
        # Cleanup: unwire after test
        container.unwire()

    @pytest.fixture
    def client(self, app):
        """Test client"""
        return TestClient(app)

    def test_remove_company_user_success(self, client, mock_controller):
        """Test DELETE /companies/{company_id}/users/{user_id} - success"""
        # Arrange
        company_id = "company-123"
        user_id = "user-456"
        current_user_id = "user-123"
        
        mock_controller.remove_company_user.return_value = None

        # Act
        response = client.delete(
            f"/company/{company_id}/users/{user_id}",
            params={"current_user_id": current_user_id}
        )

        # Assert
        assert response.status_code == 204
        mock_controller.remove_company_user.assert_called_once_with(
            company_id, user_id, current_user_id
        )

    def test_remove_company_user_last_admin(self, client, mock_controller):
        """Test DELETE /companies/{company_id}/users/{user_id} - last admin"""
        # Arrange
        company_id = "company-123"
        user_id = "user-456"
        current_user_id = "user-123"
        
        from fastapi import HTTPException
        mock_controller.remove_company_user.side_effect = HTTPException(
            status_code=400,
            detail="Cannot remove the last admin user from the company"
        )

        # Act
        response = client.delete(
            f"/company/{company_id}/users/{user_id}",
            params={"current_user_id": current_user_id}
        )

        # Assert
        assert response.status_code == 400
        assert "last admin" in response.json()["detail"].lower()

    def test_remove_company_user_auto_deletion(self, client, mock_controller):
        """Test DELETE /companies/{company_id}/users/{user_id} - self deletion attempt"""
        # Arrange
        company_id = "company-123"
        user_id = "user-123"  # Same as current_user_id
        current_user_id = "user-123"
        
        from fastapi import HTTPException
        mock_controller.remove_company_user.side_effect = HTTPException(
            status_code=400,
            detail="Cannot remove yourself from the company"
        )

        # Act
        response = client.delete(
            f"/company/{company_id}/users/{user_id}",
            params={"current_user_id": current_user_id}
        )

        # Assert
        assert response.status_code == 400
        assert "yourself" in response.json()["detail"].lower()

    def test_assign_role_to_user_success(self, client, mock_controller):
        """Test PUT /companies/{company_id}/users/{user_id}/role - success"""
        # Arrange
        company_id = "company-123"
        user_id = "user-456"
        request_data = {
            "role": "admin",
            "permissions": {
                "can_create_candidates": True,
                "can_invite_candidates": True,
                "can_manage_users": True
            }
        }
        
        expected_response = CompanyUserResponse(
            id="company-user-123",
            company_id=company_id,
            user_id=user_id,
            role="admin",
            permissions=request_data["permissions"],
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        mock_controller.assign_role_to_user.return_value = expected_response

        # Act
        response = client.put(
            f"/company/{company_id}/users/{user_id}/role",
            json=request_data
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
        assert data["user_id"] == user_id
        assert data["company_id"] == company_id
        mock_controller.assign_role_to_user.assert_called_once()

    def test_list_company_users_success(self, client, mock_controller):
        """Test GET /companies/{company_id}/users - list users"""
        # Arrange
        company_id = "company-123"
        active_only = False
        
        expected_users = [
            CompanyUserResponse(
                id="company-user-1",
                company_id=company_id,
                user_id="user-1",
                role="admin",
                permissions={"can_manage_users": True},
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            CompanyUserResponse(
                id="company-user-2",
                company_id=company_id,
                user_id="user-2",
                role="recruiter",
                permissions={"can_create_candidates": True},
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        mock_controller.list_company_users.return_value = expected_users

        # Act
        response = client.get(
            f"/company/{company_id}/users",
            params={"active_only": active_only}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["role"] == "admin"
        assert data[1]["role"] == "recruiter"
        mock_controller.list_company_users.assert_called_once_with(company_id, active_only)

    def test_list_company_users_active_only(self, client, mock_controller):
        """Test GET /companies/{company_id}/users - with active_only filter"""
        # Arrange
        company_id = "company-123"
        active_only = True
        
        expected_users = [
            CompanyUserResponse(
                id="company-user-1",
                company_id=company_id,
                user_id="user-1",
                role="admin",
                permissions={"can_manage_users": True},
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        mock_controller.list_company_users.return_value = expected_users

        # Act
        response = client.get(
            f"/company/{company_id}/users",
            params={"active_only": active_only}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert all(user["status"] == "active" for user in data)
        mock_controller.list_company_users.assert_called_once_with(company_id, active_only)

