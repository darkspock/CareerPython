"""Company Role Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional, List

from src.company_bc.company_role.domain.entities.company_role import CompanyRole
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_bc.company.domain.value_objects import CompanyId


class CompanyRoleRepositoryInterface(ABC):
    """Interface for company role repository."""

    @abstractmethod
    def save(self, role: CompanyRole) -> None:
        """Save a company role."""
        pass

    @abstractmethod
    def get_by_id(self, role_id: CompanyRoleId) -> Optional[CompanyRole]:
        """Get role by ID."""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId, active_only: bool = False) -> List[CompanyRole]:
        """List all roles for a company."""
        pass

    @abstractmethod
    def delete(self, role_id: CompanyRoleId) -> None:
        """Delete a role."""
        pass

    @abstractmethod
    def exists_by_name(self, company_id: CompanyId, name: str, exclude_id: Optional[CompanyRoleId] = None) -> bool:
        """Check if a role with the given name exists for the company."""
        pass
