from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.company_user import CompanyUser
from ..value_objects.company_id import CompanyId
from ..value_objects.company_user_id import CompanyUserId
from src.auth_bc.user.domain.value_objects.UserId import UserId


class CompanyUserRepositoryInterface(ABC):
    """Company user repository interface"""

    @abstractmethod
    def save(self, company_user: CompanyUser) -> None:
        """Save or update a company user"""
        pass

    @abstractmethod
    def get_by_id(self, company_user_id: CompanyUserId) -> Optional[CompanyUser]:
        """Get a company user by ID"""
        pass

    @abstractmethod
    def get_by_company_and_user(
        self,
        company_id: CompanyId,
        user_id: UserId
    ) -> Optional[CompanyUser]:
        """Get a company user by company and user ID"""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[CompanyUser]:
        """List all users for a company"""
        pass

    @abstractmethod
    def list_active_by_company(self, company_id: CompanyId) -> List[CompanyUser]:
        """List all active users for a company"""
        pass

    @abstractmethod
    def delete(self, company_user_id: CompanyUserId) -> None:
        """Delete a company user"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> Optional[CompanyUser]:
        """Get a company user by user ID"""
        pass

    @abstractmethod
    def count_admins_by_company(self, company_id: CompanyId) -> int:
        """Count the number of admin users for a company"""
        pass

    @abstractmethod
    def assign_company_roles(self, company_user_id: CompanyUserId, company_role_ids: List[str]) -> None:
        """Assign company roles to a company user"""
        pass

    @abstractmethod
    def get_company_role_ids(self, company_user_id: CompanyUserId) -> List[str]:
        """Get list of company role IDs assigned to a company user"""
        pass
