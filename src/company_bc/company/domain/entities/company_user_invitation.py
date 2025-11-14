from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.company_bc.company.domain.enums import CompanyUserInvitationStatus
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.company.domain.value_objects.company_user_invitation_id import CompanyUserInvitationId
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken


@dataclass
class CompanyUserInvitation:
    """
    CompanyUserInvitation domain entity
    Represents an invitation for a user to join a company
    """
    id: CompanyUserInvitationId
    company_id: CompanyId
    email: str
    invited_by_user_id: CompanyUserId
    token: InvitationToken
    status: CompanyUserInvitationStatus
    expires_at: datetime
    accepted_at: Optional[datetime]
    rejected_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: CompanyUserInvitationId,
            company_id: CompanyId,
            email: str,
            invited_by_user_id: CompanyUserId,
            token: Optional[InvitationToken] = None,
            expires_in_days: int = 7,
    ) -> "CompanyUserInvitation":
        """
        Factory method to create a new company user invitation

        Args:
            id: Invitation ID (required)
            company_id: Company ID
            email: Email of the user to invite
            invited_by_user_id: ID of the user who sent the invitation
            token: Invitation token (optional, will be generated if not provided)
            expires_in_days: Days until invitation expires (default: 7)

        Returns:
            CompanyUserInvitation: New invitation instance

        Raises:
            CompanyValidationError: If data is invalid
        """
        # Validations
        if not company_id:
            raise CompanyValidationError("company_id is required")

        if not email or not email.strip():
            raise CompanyValidationError("email is required and cannot be empty")

        if not invited_by_user_id:
            raise CompanyValidationError("invited_by_user_id is required")

        # Validate email format (basic check)
        if "@" not in email or "." not in email.split("@")[-1]:
            raise CompanyValidationError("Invalid email format")

        # Default values
        now = datetime.utcnow()

        # Generate token if not provided
        if token is None:
            token = InvitationToken.generate()

        # Set expiration date
        expires_at = now + timedelta(days=expires_in_days)

        return cls(
            id=id,
            company_id=company_id,
            email=email.strip().lower(),
            invited_by_user_id=invited_by_user_id,
            token=token,
            status=CompanyUserInvitationStatus.PENDING,
            expires_at=expires_at,
            accepted_at=None,
            rejected_at=None,
            created_at=now,
            updated_at=now,
        )

    def accept(self) -> None:
        """
        Accepts the invitation
        Updates the status to ACCEPTED

        Raises:
            CompanyValidationError: If invitation cannot be accepted
        """
        if self.status != CompanyUserInvitationStatus.PENDING:
            raise CompanyValidationError(
                f"Cannot accept invitation with status {self.status.value}. Only PENDING invitations can be accepted."
            )

        if self.is_expired():
            raise CompanyValidationError("Cannot accept expired invitation")

        self.status = CompanyUserInvitationStatus.ACCEPTED
        self.accepted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def reject(self) -> None:
        """
        Rejects the invitation
        Updates the status to REJECTED

        Raises:
            CompanyValidationError: If invitation cannot be rejected
        """
        if self.status != CompanyUserInvitationStatus.PENDING:
            raise CompanyValidationError(
                f"Cannot reject invitation with status {self.status.value}. Only PENDING invitations can be rejected."
            )

        self.status = CompanyUserInvitationStatus.REJECTED
        self.rejected_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def expire(self) -> None:
        """
        Marks the invitation as expired
        Updates the status to EXPIRED
        """
        if self.status == CompanyUserInvitationStatus.EXPIRED:
            return

        self.status = CompanyUserInvitationStatus.EXPIRED
        self.updated_at = datetime.utcnow()

    def cancel(self) -> None:
        """
        Cancels the invitation
        Updates the status to CANCELLED

        Raises:
            CompanyValidationError: If invitation cannot be cancelled
        """
        if self.status != CompanyUserInvitationStatus.PENDING:
            raise CompanyValidationError(
                f"Cannot cancel invitation with status {self.status.value}. Only PENDING invitations can be cancelled."
            )

        self.status = CompanyUserInvitationStatus.CANCELLED
        self.updated_at = datetime.utcnow()

    def is_expired(self) -> bool:
        """
        Checks if the invitation is expired

        Returns:
            bool: True if expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at

    def is_pending(self) -> bool:
        """
        Checks if the invitation is pending

        Returns:
            bool: True if pending, False otherwise
        """
        return self.status == CompanyUserInvitationStatus.PENDING
