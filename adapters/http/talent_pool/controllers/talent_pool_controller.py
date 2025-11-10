"""
Talent Pool Controller
Phase 8: Controller for talent pool operations
"""

from typing import List, Optional

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.company_bc.talent_pool.application.commands.add_to_talent_pool_command import AddToTalentPoolCommand
from src.company_bc.talent_pool.application.commands.change_talent_pool_entry_status_command import (
    ChangeTalentPoolEntryStatusCommand,
)
from src.company_bc.talent_pool.application.commands.remove_from_talent_pool_command import RemoveFromTalentPoolCommand
from src.company_bc.talent_pool.application.commands.update_talent_pool_entry_command import UpdateTalentPoolEntryCommand
from src.company_bc.talent_pool.application.dtos.talent_pool_entry_dto import TalentPoolEntryDto
from src.company_bc.talent_pool.application.queries.get_talent_pool_entry_by_id_query import GetTalentPoolEntryByIdQuery
from src.company_bc.talent_pool.application.queries.list_talent_pool_entries_query import ListTalentPoolEntriesQuery
from src.company_bc.talent_pool.application.queries.search_talent_pool_query import SearchTalentPoolQuery
from src.company_bc.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.company_bc.talent_pool.presentation.mappers.talent_pool_mapper import TalentPoolMapper
from src.company_bc.talent_pool.presentation.schemas.talent_pool_schemas import TalentPoolEntryResponse


class TalentPoolController:
    """Controller for talent pool operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def add_to_talent_pool(
            self,
            company_id: str,
            candidate_id: str,
            added_reason: Optional[str] = None,
            tags: Optional[List[str]] = None,
            rating: Optional[int] = None,
            notes: Optional[str] = None,
            status: TalentPoolStatus = TalentPoolStatus.ACTIVE,
            source_application_id: Optional[str] = None,
            source_position_id: Optional[str] = None,
            added_by_user_id: Optional[str] = None,
    ) -> dict:
        """
        Add a candidate to the talent pool.

        Args:
            company_id: Company ID
            candidate_id: Candidate ID
            added_reason: Reason for adding
            tags: List of tags
            rating: Rating 1-5
            notes: Additional notes
            status: Entry status
            source_application_id: Source application if from application
            source_position_id: Source position if from application
            added_by_user_id: User who added the entry

        Returns:
            Success message
        """
        command = AddToTalentPoolCommand(
            company_id=company_id,
            candidate_id=candidate_id,
            added_reason=added_reason,
            tags=tags,
            rating=rating,
            notes=notes,
            status=status,
            source_application_id=source_application_id,
            source_position_id=source_position_id,
            added_by_user_id=added_by_user_id,
        )
        self._command_bus.execute(command)
        return {"message": "Candidate added to talent pool successfully"}

    def get_entry_by_id(self, entry_id: str) -> Optional[TalentPoolEntryResponse]:
        """
        Get a talent pool entry by ID.

        Args:
            entry_id: Entry ID

        Returns:
            Talent pool entry response or None
        """
        query = GetTalentPoolEntryByIdQuery(entry_id=entry_id)
        dto: Optional[TalentPoolEntryDto] = self._query_bus.query(query)

        if not dto:
            return None

        return TalentPoolMapper.dto_to_response(dto)

    def list_entries(
            self,
            company_id: str,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntryResponse]:
        """
        List talent pool entries for a company.

        Args:
            company_id: Company ID
            status: Filter by status
            tags: Filter by tags
            min_rating: Filter by minimum rating

        Returns:
            List of talent pool entries
        """
        query = ListTalentPoolEntriesQuery(
            company_id=company_id,
            status=status,
            tags=tags,
            min_rating=min_rating,
        )
        dtos: List[TalentPoolEntryDto] = self._query_bus.query(query)
        return [TalentPoolMapper.dto_to_response(dto) for dto in dtos]

    def search_entries(
            self,
            company_id: str,
            search_term: Optional[str] = None,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntryResponse]:
        """
        Search talent pool entries.

        Args:
            company_id: Company ID
            search_term: Search term
            status: Filter by status
            tags: Filter by tags
            min_rating: Filter by minimum rating

        Returns:
            List of matching talent pool entries
        """
        query = SearchTalentPoolQuery(
            company_id=company_id,
            search_term=search_term,
            status=status,
            tags=tags,
            min_rating=min_rating,
        )
        dtos: List[TalentPoolEntryDto] = self._query_bus.query(query)
        return [TalentPoolMapper.dto_to_response(dto) for dto in dtos]

    def update_entry(
            self,
            entry_id: str,
            added_reason: Optional[str] = None,
            tags: Optional[List[str]] = None,
            rating: Optional[int] = None,
            notes: Optional[str] = None,
    ) -> dict:
        """
        Update a talent pool entry.

        Args:
            entry_id: Entry ID
            added_reason: Updated reason
            tags: Updated tags
            rating: Updated rating
            notes: Updated notes

        Returns:
            Success message
        """
        command = UpdateTalentPoolEntryCommand(
            entry_id=entry_id,
            added_reason=added_reason,
            tags=tags,
            rating=rating,
            notes=notes,
        )
        self._command_bus.execute(command)
        return {"message": "Talent pool entry updated successfully"}

    def change_status(self, entry_id: str, new_status: TalentPoolStatus) -> dict:
        """
        Change talent pool entry status.

        Args:
            entry_id: Entry ID
            new_status: New status

        Returns:
            Success message
        """
        command = ChangeTalentPoolEntryStatusCommand(
            entry_id=entry_id,
            new_status=new_status,
        )
        self._command_bus.execute(command)
        return {"message": "Talent pool entry status changed successfully"}

    def remove_from_talent_pool(self, entry_id: str) -> dict:
        """
        Remove a candidate from the talent pool.

        Args:
            entry_id: Entry ID

        Returns:
            Success message
        """
        command = RemoveFromTalentPoolCommand(entry_id=entry_id)
        self._command_bus.execute(command)
        return {"message": "Candidate removed from talent pool successfully"}
