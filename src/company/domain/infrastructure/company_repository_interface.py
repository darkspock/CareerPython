from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.company import Company
from ..value_objects.company_id import CompanyId


class CompanyRepositoryInterface(ABC):
    """Company repository interface"""

    @abstractmethod
    def save(self, company: Company) -> None:
        """Save or update a company"""
        pass

    @abstractmethod
    def get_by_id(self, company_id: CompanyId) -> Optional[Company]:
        """Get a company by ID"""
        pass

    @abstractmethod
    def get_by_domain(self, domain: str) -> Optional[Company]:
        """Get a company by domain"""
        pass

    @abstractmethod
    def list_all(self) -> List[Company]:
        """List all companies"""
        pass

    @abstractmethod
    def list_active(self) -> List[Company]:
        """List all active companies"""
        pass

    @abstractmethod
    def delete(self, company_id: CompanyId) -> None:
        """Delete a company"""
        pass
