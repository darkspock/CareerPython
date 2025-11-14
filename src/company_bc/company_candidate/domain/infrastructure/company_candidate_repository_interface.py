from abc import ABC, abstractmethod
from typing import Optional, List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.company.domain.value_objects import CompanyId
from ..entities.company_candidate import CompanyCandidate
from ..read_models.company_candidate_with_candidate_read_model import CompanyCandidateWithCandidateReadModel
from ..value_objects import CompanyCandidateId


class CompanyCandidateRepositoryInterface(ABC):
    """CompanyCandidate repository interface"""

    @abstractmethod
    def save(self, company_candidate: CompanyCandidate) -> None:
        """Save or update a company candidate relationship"""
        pass

    @abstractmethod
    def get_by_id(self, company_candidate_id: CompanyCandidateId) -> Optional[CompanyCandidate]:
        """Get a company candidate by ID"""
        pass

    @abstractmethod
    def get_by_id_with_candidate_info(self, company_candidate_id: CompanyCandidateId) -> Optional[
        CompanyCandidateWithCandidateReadModel]:
        """
        Get a single company candidate by ID with candidate basic info.
        Returns read model (not entity) with data from both tables via JOIN.
        """
        pass

    @abstractmethod
    def get_by_company_and_candidate(
            self,
            company_id: CompanyId,
            candidate_id: CandidateId
    ) -> Optional[CompanyCandidate]:
        """Get a company candidate by company and candidate IDs"""
        pass

    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all company candidates for a company"""
        pass

    @abstractmethod
    def list_by_candidate(self, candidate_id: CandidateId) -> List[CompanyCandidate]:
        """List all company candidates for a candidate"""
        pass

    @abstractmethod
    def list_active_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all active company candidates for a company"""
        pass

    @abstractmethod
    def delete(self, company_candidate_id: CompanyCandidateId) -> None:
        """Delete a company candidate relationship"""
        pass

    @abstractmethod
    def list_by_company_with_candidate_info(self, company_id: CompanyId) -> List[
        CompanyCandidateWithCandidateReadModel]:
        """
        List all company candidates for a company with candidate basic info.
        Returns read models (not entities) with data from both tables via JOIN.
        """
        pass
