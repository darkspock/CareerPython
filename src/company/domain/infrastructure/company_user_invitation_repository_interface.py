from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.company_user_invitation import CompanyUserInvitation
from ..value_objects.company_id import CompanyId
from ..value_objects.company_user_invitation_id import CompanyUserInvitationId
from ..value_objects.invitation_token import InvitationToken


class CompanyUserInvitationRepositoryInterface(ABC):
    """Company user invitation repository interface"""

    @abstractmethod
    def save(self, invitation: CompanyUserInvitation) -> None:
        """Save or update a company user invitation"""
        pass

    @abstractmethod
    def get_by_id(self, invitation_id: CompanyUserInvitationId) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by ID"""
        pass

    @abstractmethod
    def get_by_token(self, token: InvitationToken) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by token"""
        pass

    @abstractmethod
    def get_by_email_and_company(
            self,
            email: str,
            company_id: CompanyId
    ) -> Optional[CompanyUserInvitation]:
        """Get a company user invitation by email and company ID"""
        pass

    @abstractmethod
    def find_pending_by_email(self, email: str) -> List[CompanyUserInvitation]:
        """Find all pending invitations for an email"""
        pass

    @abstractmethod
    def find_expired(self) -> List[CompanyUserInvitation]:
        """Find all expired invitations"""
        pass

    @abstractmethod
    def delete(self, invitation_id: CompanyUserInvitationId) -> None:
        """Delete a company user invitation"""
        pass
