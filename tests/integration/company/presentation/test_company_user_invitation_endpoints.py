"""
Integration tests for Company User Invitation endpoints
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime, timedelta

from adapters.http.company_app.company.routers.company_user_router import router as company_user_router
from adapters.http.auth.invitations.routers.invitation_router import router as invitation_router
from adapters.http.company_app.company.schemas.company_user_invitation_response import (
    UserInvitationLinkResponse,
    CompanyUserInvitationResponse
)
from core.container import Container


class TestCompanyUserInvitationEndpoints:
    """Tests for company user invitation endpoints"""

    @pytest.fixture
    def mock_company_user_controller(self):
        """Mock controller for company user operations"""
        return Mock()

    @pytest.fixture
    def mock_invitation_controller(self):
        """Mock controller for invitation operations"""
        return Mock()

    @pytest.fixture
    def app(self, mock_company_user_controller, mock_invitation_controller):
        """Create FastAPI app with mocked controllers"""
        from dependency_injector import providers
        
        app = FastAPI()
        app.include_router(company_user_router)
        app.include_router(invitation_router)
        
        # Override container providers with mocks
        container = Container()
        # Override the provider factory with a singleton that returns our mock
        container.company_user_controller.override(
            providers.Singleton(lambda: mock_company_user_controller)
        )
        container.invitation_controller.override(
            providers.Singleton(lambda: mock_invitation_controller)
        )
        
        # Wire the container to the routers
        container.wire(modules=[
            "adapters.http.company.routers.company_user_router",
            "adapters.http.invitations.routers.invitation_router"
        ])
        
        app.container = container
        
        yield app
        
        # Cleanup: unwire after test
        container.unwire()

    @pytest.fixture
    def client(self, app):
        """Test client"""
        return TestClient(app)

    def test_invite_company_user_success(self, client, mock_company_user_controller):
        """Test POST /companies/{company_id}/users/invite - success"""
        # Arrange
        company_id = "company-123"
        current_user_id = "user-123"
        request_data = {
            "email": "newuser@example.com",
            "role": "recruiter"
        }
        
        expected_response = UserInvitationLinkResponse(
            invitation_id="inv-123",
            invitation_link="http://localhost:3000/invitations/accept?token=abc123",
            expires_at=datetime.utcnow() + timedelta(days=7),
            email="newuser@example.com"
        )
        
        mock_company_user_controller.invite_company_user.return_value = expected_response

        # Act
        response = client.post(
            f"/company/{company_id}/users/invite",
            json=request_data,
            params={"current_user_id": current_user_id}
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "invitation_link" in data
        assert "invitation_id" in data
        mock_company_user_controller.invite_company_user.assert_called_once()

    def test_invite_company_user_duplicate_email(self, client, mock_company_user_controller):
        """Test POST /companies/{company_id}/users/invite - duplicate email"""
        # Arrange
        company_id = "company-123"
        current_user_id = "user-123"
        request_data = {
            "email": "existing@example.com",
            "role": "recruiter"
        }
        
        from fastapi import HTTPException
        mock_company_user_controller.invite_company_user.side_effect = HTTPException(
            status_code=400,
            detail="User with this email is already part of this company"
        )

        # Act
        response = client.post(
            f"/company/{company_id}/users/invite",
            json=request_data,
            params={"current_user_id": current_user_id}
        )

        # Assert
        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

    def test_get_invitation_by_token_success(self, client, mock_invitation_controller):
        """Test GET /invitations/{token} - success"""
        # Arrange
        token = "valid_token_1234567890"
        expected_response = CompanyUserInvitationResponse(
            id="inv-123",
            company_id="company-123",
            email="test@example.com",
            invited_by_user_id="user-123",
            token=token,
            status="pending",
            expires_at=datetime.utcnow() + timedelta(days=7),
            accepted_at=None,
            rejected_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            invitation_link=f"http://localhost:3000/invitations/accept?token={token}"
        )
        
        mock_invitation_controller.get_invitation_by_token.return_value = expected_response

        # Act
        response = client.get(f"/invitations/{token}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["status"] == "pending"
        assert data["token"] == token
        assert "invitation_link" in data
        mock_invitation_controller.get_invitation_by_token.assert_called_once_with(token)

    def test_get_invitation_by_token_invalid(self, client, mock_invitation_controller):
        """Test GET /invitations/{token} - invalid token"""
        # Arrange
        token = "invalid_token"
        
        from fastapi import HTTPException
        mock_invitation_controller.get_invitation_by_token.side_effect = HTTPException(
            status_code=404,
            detail="Invitation not found"
        )

        # Act
        response = client.get(f"/invitations/{token}")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_invitation_by_token_expired(self, client, mock_invitation_controller):
        """Test GET /invitations/{token} - expired token"""
        # Arrange
        token = "expired_token_1234567890"
        expired_response = CompanyUserInvitationResponse(
            id="inv-123",
            company_id="company-123",
            email="test@example.com",
            invited_by_user_id="user-123",
            token=token,
            status="expired",
            expires_at=datetime.utcnow() - timedelta(days=1),
            accepted_at=None,
            rejected_at=None,
            created_at=datetime.utcnow() - timedelta(days=8),
            updated_at=datetime.utcnow() - timedelta(days=1),
            invitation_link=f"http://localhost:3000/invitations/accept?token={token}"
        )
        
        mock_invitation_controller.get_invitation_by_token.return_value = expired_response

        # Act
        response = client.get(f"/invitations/{token}")

        # Assert
        assert response.status_code == 200  # Token exists but is expired
        data = response.json()
        assert data["status"] == "expired"
        assert datetime.fromisoformat(data["expires_at"].replace('Z', '+00:00')) < datetime.utcnow()

    def test_accept_invitation_new_user(self, client, mock_invitation_controller):
        """Test POST /invitations/accept - new user"""
        # Arrange
        request_data = {
            "token": "valid_token_1234567890",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "secure_password123"
        }
        
        mock_invitation_controller.accept_invitation.return_value = {
            "message": "Invitation accepted successfully"
        }

        # Act
        response = client.post("/invitations/accept", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"].lower()
        mock_invitation_controller.accept_invitation.assert_called_once()

    def test_accept_invitation_existing_user(self, client, mock_invitation_controller):
        """Test POST /invitations/accept - existing user"""
        # Arrange
        request_data = {
            "token": "valid_token_1234567890",
            "user_id": "user-456"
        }
        
        mock_invitation_controller.accept_invitation.return_value = {
            "message": "Invitation accepted successfully"
        }

        # Act
        response = client.post("/invitations/accept", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"].lower()

    def test_accept_invitation_invalid_token(self, client, mock_invitation_controller):
        """Test POST /invitations/accept - invalid token"""
        # Arrange
        request_data = {
            "token": "invalid_token",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "secure_password123"
        }
        
        from fastapi import HTTPException
        mock_invitation_controller.accept_invitation.side_effect = HTTPException(
            status_code=400,
            detail="Invalid or expired invitation token"
        )

        # Act
        response = client.post("/invitations/accept", json=request_data)

        # Assert
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower() or "expired" in response.json()["detail"].lower()

    def test_accept_invitation_expired_token(self, client, mock_invitation_controller):
        """Test POST /invitations/accept - expired token"""
        # Arrange
        request_data = {
            "token": "expired_token_1234567890",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "secure_password123"
        }
        
        from fastapi import HTTPException
        mock_invitation_controller.accept_invitation.side_effect = HTTPException(
            status_code=400,
            detail="Invitation has expired"
        )

        # Act
        response = client.post("/invitations/accept", json=request_data)

        # Assert
        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower()

