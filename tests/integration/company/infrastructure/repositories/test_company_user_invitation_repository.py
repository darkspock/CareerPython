"""
Integration tests for CompanyUserInvitationRepository
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine

from src.company_bc.company.domain.entities.company_user_invitation import CompanyUserInvitation
from src.company_bc.company.domain.enums import CompanyUserInvitationStatus
from src.company_bc.company.domain.value_objects import CompanyId, CompanyUserId
from src.company_bc.company.domain.value_objects.company_user_invitation_id import (
    CompanyUserInvitationId
)
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken
from src.company_bc.company.infrastructure.repositories.company_user_invitation_repository import (
    CompanyUserInvitationRepository
)
from core.database import SQLAlchemyDatabase
from core.base import Base


class TestCompanyUserInvitationRepository:
    """Tests for CompanyUserInvitationRepository"""

    @pytest.fixture
    def database(self):
        """Create in-memory database for tests"""
        engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(engine)
        db = SQLAlchemyDatabase()
        db._engine = engine  # Use in-memory engine
        return db

    @pytest.fixture
    def repository(self, database):
        """Create repository for tests"""
        return CompanyUserInvitationRepository(database)

    @pytest.fixture
    def company_id(self):
        """Fixture for company ID"""
        return CompanyId.generate()

    @pytest.fixture
    def invited_by_user_id(self):
        """Fixture for invited by user ID"""
        return CompanyUserId.generate()

    @pytest.fixture
    def invitation_id(self):
        """Fixture for invitation ID"""
        return CompanyUserInvitationId.generate()

    @pytest.fixture
    def test_invitation(self, invitation_id, company_id, invited_by_user_id):
        """Create test invitation"""
        return CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email="test@example.com",
            invited_by_user_id=invited_by_user_id,
            expires_in_days=7
        )

    def test_save_new_invitation_success(self, repository, test_invitation):
        """Test saving a new invitation successfully"""
        # Act
        repository.save(test_invitation)

        # Assert
        found = repository.get_by_id(test_invitation.id)
        assert found is not None
        assert found.id == test_invitation.id
        assert found.email == test_invitation.email
        assert found.company_id == test_invitation.company_id
        assert found.status == CompanyUserInvitationStatus.PENDING

    def test_get_by_id_success(self, repository, test_invitation):
        """Test getting invitation by ID"""
        # Arrange
        repository.save(test_invitation)

        # Act
        found = repository.get_by_id(test_invitation.id)

        # Assert
        assert found is not None
        assert found.id == test_invitation.id
        assert found.email == test_invitation.email

    def test_get_by_id_not_found(self, repository):
        """Test getting invitation by ID that doesn't exist"""
        # Arrange
        invitation_id = CompanyUserInvitationId.generate()

        # Act
        found = repository.get_by_id(invitation_id)

        # Assert
        assert found is None

    def test_get_by_token_success(self, repository, test_invitation):
        """Test getting invitation by token"""
        # Arrange
        repository.save(test_invitation)

        # Act
        found = repository.get_by_token(test_invitation.token)

        # Assert
        assert found is not None
        assert found.id == test_invitation.id
        assert found.token == test_invitation.token

    def test_get_by_token_not_found(self, repository):
        """Test getting invitation by token that doesn't exist"""
        # Arrange
        token = InvitationToken.generate()

        # Act
        found = repository.get_by_token(token)

        # Assert
        assert found is None

    def test_get_by_email_and_company_success(self, repository, company_id, invited_by_user_id):
        """Test getting invitation by email and company"""
        # Arrange
        invitation_id = CompanyUserInvitationId.generate()
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email="test@example.com",
            invited_by_user_id=invited_by_user_id
        )
        repository.save(invitation)

        # Act
        found = repository.get_by_email_and_company("test@example.com", company_id)

        # Assert
        assert found is not None
        assert found.email.lower() == "test@example.com"
        assert found.company_id == company_id

    def test_get_by_email_and_company_not_found(self, repository, company_id):
        """Test getting invitation by email and company that doesn't exist"""
        # Act
        found = repository.get_by_email_and_company("nonexistent@example.com", company_id)

        # Assert
        assert found is None

    def test_find_pending_by_email_success(self, repository, company_id, invited_by_user_id):
        """Test finding pending invitations by email"""
        # Arrange
        invitation1_id = CompanyUserInvitationId.generate()
        invitation1 = CompanyUserInvitation.create(
            id=invitation1_id,
            company_id=company_id,
            email="test@example.com",
            invited_by_user_id=invited_by_user_id
        )
        repository.save(invitation1)

        invitation2_id = CompanyUserInvitationId.generate()
        invitation2 = CompanyUserInvitation.create(
            id=invitation2_id,
            company_id=company_id,
            email="test@example.com",
            invited_by_user_id=invited_by_user_id
        )
        repository.save(invitation2)

        # Act
        pending = repository.find_pending_by_email("test@example.com")

        # Assert
        assert len(pending) == 2
        assert all(inv.status == CompanyUserInvitationStatus.PENDING for inv in pending)

    def test_find_pending_by_email_empty(self, repository):
        """Test finding pending invitations when none exist"""
        # Act
        pending = repository.find_pending_by_email("nonexistent@example.com")

        # Assert
        assert len(pending) == 0

    def test_find_expired_invitations(self, repository, company_id, invited_by_user_id):
        """Test finding expired invitations"""
        # Arrange - Create expired invitation
        invitation_id = CompanyUserInvitationId.generate()
        now = datetime.utcnow()
        expired_at = now - timedelta(days=1)
        
        invitation = CompanyUserInvitation(
            id=invitation_id,
            company_id=company_id,
            email="expired@example.com",
            invited_by_user_id=invited_by_user_id,
            token=InvitationToken.generate(),
            status=CompanyUserInvitationStatus.PENDING,
            expires_at=expired_at,
            accepted_at=None,
            rejected_at=None,
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=2),
        )
        repository.save(invitation)

        # Create non-expired invitation
        invitation2_id = CompanyUserInvitationId.generate()
        invitation2 = CompanyUserInvitation.create(
            id=invitation2_id,
            company_id=company_id,
            email="active@example.com",
            invited_by_user_id=invited_by_user_id,
            expires_in_days=7
        )
        repository.save(invitation2)

        # Act
        expired = repository.find_expired()

        # Assert
        assert len(expired) >= 1
        assert any(inv.email == "expired@example.com" for inv in expired)

    def test_delete_invitation_success(self, repository, test_invitation):
        """Test deleting an invitation"""
        # Arrange
        repository.save(test_invitation)

        # Act
        repository.delete(test_invitation.id)

        # Assert
        found = repository.get_by_id(test_invitation.id)
        assert found is None

    def test_domain_to_model_conversion(self, repository, test_invitation):
        """Test domain entity to model conversion"""
        # Arrange
        repository.save(test_invitation)

        # Act - Get from DB and verify conversion
        found = repository.get_by_id(test_invitation.id)

        # Assert
        assert found is not None
        assert found.id == test_invitation.id
        assert found.email == test_invitation.email
        assert found.company_id == test_invitation.company_id
        assert found.token == test_invitation.token
        assert found.status == test_invitation.status
        assert found.expires_at == test_invitation.expires_at

    def test_update_invitation_status(self, repository, test_invitation):
        """Test updating invitation status"""
        # Arrange
        repository.save(test_invitation)

        # Act - Update status
        test_invitation.accept()
        repository.save(test_invitation)

        # Assert
        found = repository.get_by_id(test_invitation.id)
        assert found is not None
        assert found.status == CompanyUserInvitationStatus.ACCEPTED
        assert found.accepted_at is not None

    def test_email_case_insensitive(self, repository, company_id, invited_by_user_id):
        """Test that email lookups are case insensitive"""
        # Arrange
        invitation_id = CompanyUserInvitationId.generate()
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email="Test@Example.COM",
            invited_by_user_id=invited_by_user_id
        )
        repository.save(invitation)

        # Act - Search with different case
        found = repository.get_by_email_and_company("test@example.com", company_id)

        # Assert
        assert found is not None
        assert found.email.lower() == "test@example.com"

