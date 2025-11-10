import pytest
from datetime import datetime, timedelta

from src.company_bc.company.domain.entities.company_user_invitation import CompanyUserInvitation
from src.company_bc.company.domain.enums.company_user_invitation_status import CompanyUserInvitationStatus
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company_bc.company.domain.value_objects import CompanyId, CompanyUserId
from src.company_bc.company.domain.value_objects.company_user_invitation_id import CompanyUserInvitationId
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken


class TestCompanyUserInvitation:
    """Tests for CompanyUserInvitation entity"""

    @pytest.fixture
    def invitation_id(self):
        """Fixture for invitation ID"""
        return CompanyUserInvitationId.generate()

    @pytest.fixture
    def company_id(self):
        """Fixture for company ID"""
        return CompanyId.generate()

    @pytest.fixture
    def invited_by_user_id(self):
        """Fixture for invited by user ID"""
        return CompanyUserId.generate()

    @pytest.fixture
    def valid_email(self):
        """Fixture for valid email"""
        return "test@example.com"

    def test_create_generates_token_if_not_provided(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that create() generates token if not provided"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        assert invitation.token is not None
        assert isinstance(invitation.token, InvitationToken)

    def test_create_uses_provided_token(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that create() uses provided token"""
        token = InvitationToken.generate()
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
            token=token,
        )
        
        assert invitation.token == token

    def test_create_sets_status_to_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that create() sets status to PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        assert invitation.status == CompanyUserInvitationStatus.PENDING

    def test_create_sets_expires_at(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that create() sets expires_at correctly"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
            expires_in_days=7,
        )
        
        expected_expiry = datetime.utcnow() + timedelta(days=7)
        # Allow 1 second difference for timing
        assert abs((invitation.expires_at - expected_expiry).total_seconds()) < 2

    def test_create_raises_on_empty_email(self, invitation_id, company_id, invited_by_user_id):
        """Test that create() raises error on empty email"""
        with pytest.raises(CompanyValidationError, match="email is required"):
            CompanyUserInvitation.create(
                id=invitation_id,
                company_id=company_id,
                email="",
                invited_by_user_id=invited_by_user_id,
            )

    def test_create_raises_on_invalid_email(self, invitation_id, company_id, invited_by_user_id):
        """Test that create() raises error on invalid email"""
        with pytest.raises(CompanyValidationError, match="Invalid email format"):
            CompanyUserInvitation.create(
                id=invitation_id,
                company_id=company_id,
                email="notanemail",
                invited_by_user_id=invited_by_user_id,
            )

    def test_create_normalizes_email(self, invitation_id, company_id, invited_by_user_id):
        """Test that create() normalizes email to lowercase"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email="  TEST@EXAMPLE.COM  ",
            invited_by_user_id=invited_by_user_id,
        )
        
        assert invitation.email == "test@example.com"

    def test_accept_changes_status_to_accepted(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that accept() changes status to ACCEPTED"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.accept()
        
        assert invitation.status == CompanyUserInvitationStatus.ACCEPTED
        assert invitation.accepted_at is not None

    def test_accept_raises_if_not_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that accept() raises error if status is not PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.accept()
        
        with pytest.raises(CompanyValidationError, match="Cannot accept invitation"):
            invitation.accept()

    def test_accept_raises_if_expired(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that accept() raises error if invitation is expired"""
        # Create invitation with past expiry
        now = datetime.utcnow()
        expired_at = now - timedelta(days=1)
        
        invitation = CompanyUserInvitation(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
            token=InvitationToken.generate(),
            status=CompanyUserInvitationStatus.PENDING,
            expires_at=expired_at,
            accepted_at=None,
            rejected_at=None,
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=2),
        )
        
        with pytest.raises(CompanyValidationError, match="Cannot accept expired invitation"):
            invitation.accept()

    def test_reject_changes_status_to_rejected(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that reject() changes status to REJECTED"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.reject()
        
        assert invitation.status == CompanyUserInvitationStatus.REJECTED
        assert invitation.rejected_at is not None

    def test_reject_raises_if_not_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that reject() raises error if status is not PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.reject()
        
        with pytest.raises(CompanyValidationError, match="Cannot reject invitation"):
            invitation.reject()

    def test_expire_changes_status_to_expired(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that expire() changes status to EXPIRED"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.expire()
        
        assert invitation.status == CompanyUserInvitationStatus.EXPIRED

    def test_expire_is_idempotent(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that expire() is idempotent"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.expire()
        initial_status = invitation.status
        invitation.expire()  # Call again
        
        assert invitation.status == initial_status

    def test_cancel_changes_status_to_cancelled(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that cancel() changes status to CANCELLED"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.cancel()
        
        assert invitation.status == CompanyUserInvitationStatus.CANCELLED

    def test_cancel_raises_if_not_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that cancel() raises error if status is not PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.cancel()
        
        with pytest.raises(CompanyValidationError, match="Cannot cancel invitation"):
            invitation.cancel()

    def test_is_expired_returns_true_when_expired(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that is_expired() returns True when invitation is expired"""
        now = datetime.utcnow()
        expired_at = now - timedelta(days=1)
        
        invitation = CompanyUserInvitation(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
            token=InvitationToken.generate(),
            status=CompanyUserInvitationStatus.PENDING,
            expires_at=expired_at,
            accepted_at=None,
            rejected_at=None,
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=2),
        )
        
        assert invitation.is_expired() is True

    def test_is_expired_returns_false_when_not_expired(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that is_expired() returns False when invitation is not expired"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        assert invitation.is_expired() is False

    def test_is_pending_returns_true_when_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that is_pending() returns True when status is PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        assert invitation.is_pending() is True

    def test_is_pending_returns_false_when_not_pending(self, invitation_id, company_id, invited_by_user_id, valid_email):
        """Test that is_pending() returns False when status is not PENDING"""
        invitation = CompanyUserInvitation.create(
            id=invitation_id,
            company_id=company_id,
            email=valid_email,
            invited_by_user_id=invited_by_user_id,
        )
        
        invitation.accept()
        
        assert invitation.is_pending() is False

