"""
Talent Pool Entry Repository Interface
Phase 8: Repository interface for talent pool entries
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.talent_pool.domain.entities.talent_pool_entry import TalentPoolEntry
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId


class TalentPoolEntryRepositoryInterface(ABC):
    """
    Interface for talent pool entry repository.

    Defines all persistence operations for talent pool entries.
    """

    @abstractmethod
    def get_by_id(self, entry_id: TalentPoolEntryId) -> Optional[TalentPoolEntry]:
        """
        Get a talent pool entry by ID.

        Args:
            entry_id: The talent pool entry ID

        Returns:
            TalentPoolEntry if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_candidate(self, company_id: str, candidate_id: str) -> Optional[TalentPoolEntry]:
        """
        Get a talent pool entry for a specific candidate in a company.

        Args:
            company_id: The company ID
            candidate_id: The candidate ID

        Returns:
            TalentPoolEntry if found, None otherwise
        """
        pass

    @abstractmethod
    def list_by_company(
            self,
            company_id: str,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntry]:
        """
        List talent pool entries for a company with optional filters.

        Args:
            company_id: The company ID
            status: Filter by status (optional)
            tags: Filter by tags (entries must have ALL specified tags)
            min_rating: Filter by minimum rating (optional)

        Returns:
            List of talent pool entries
        """
        pass

    @abstractmethod
    def search(
            self,
            company_id: str,
            search_term: Optional[str] = None,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntry]:
        """
        Search talent pool entries with filters.

        Args:
            company_id: The company ID
            search_term: Search in notes and added_reason (optional)
            status: Filter by status (optional)
            tags: Filter by tags (optional)
            min_rating: Filter by minimum rating (optional)

        Returns:
            List of matching talent pool entries
        """
        pass

    @abstractmethod
    def save(self, entry: TalentPoolEntry) -> None:
        """
        Save a talent pool entry (create or update).

        Args:
            entry: The talent pool entry to save
        """
        pass

    @abstractmethod
    def delete(self, entry_id: TalentPoolEntryId) -> None:
        """
        Delete a talent pool entry.

        Args:
            entry_id: The talent pool entry ID to delete
        """
        pass

    @abstractmethod
    def exists(self, company_id: str, candidate_id: str) -> bool:
        """
        Check if a candidate exists in company's talent pool.

        Args:
            company_id: The company ID
            candidate_id: The candidate ID

        Returns:
            True if exists, False otherwise
        """
        pass

    @abstractmethod
    def count_by_company(self, company_id: str, status: Optional[TalentPoolStatus] = None) -> int:
        """
        Count talent pool entries for a company.

        Args:
            company_id: The company ID
            status: Filter by status (optional)

        Returns:
            Count of entries
        """
        pass
