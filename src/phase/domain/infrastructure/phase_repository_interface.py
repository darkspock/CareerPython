"""Phase repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.entities.phase import Phase
from src.phase.domain.value_objects.phase_id import PhaseId


class PhaseRepositoryInterface(ABC):
    """Interface for Phase repository"""

    @abstractmethod
    def save(self, phase: Phase) -> None:
        """Save a phase"""
        pass

    @abstractmethod
    def get_by_id(self, phase_id: PhaseId) -> Optional[Phase]:
        """Get phase by ID"""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[Phase]:
        """List all phases for a company, ordered by sort_order"""
        pass

    @abstractmethod
    def delete(self, phase_id: PhaseId) -> None:
        """Delete a phase"""
        pass

    @abstractmethod
    def exists(self, phase_id: PhaseId) -> bool:
        """Check if phase exists"""
        pass
