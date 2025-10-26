"""
Add to Talent Pool Command
Phase 8: Command to add a candidate to company's talent pool
"""

from dataclasses import dataclass
from typing import Optional, List

from core.cqrs.command import Command
from core.cqrs.command_handler import CommandHandler
from src.talent_pool.domain.entities.talent_pool_entry import TalentPoolEntry
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)


@dataclass(frozen=True)
class AddToTalentPoolCommand(Command):
    """Command to add a candidate to talent pool"""

    company_id: str
    candidate_id: str
    added_reason: Optional[str] = None
    tags: Optional[List[str]] = None
    rating: Optional[int] = None
    notes: Optional[str] = None
    status: TalentPoolStatus = TalentPoolStatus.ACTIVE
    source_application_id: Optional[str] = None
    source_position_id: Optional[str] = None
    added_by_user_id: Optional[str] = None


class AddToTalentPoolCommandHandler(CommandHandler[AddToTalentPoolCommand]):
    """Handler for add to talent pool command"""

    def __init__(self, repository: TalentPoolEntryRepositoryInterface):
        self._repository = repository

    def execute(self, command: AddToTalentPoolCommand) -> None:
        """
        Execute the command to add candidate to talent pool.

        Raises:
            ValueError: If candidate already exists in talent pool
        """
        # Check if candidate already exists in talent pool
        if self._repository.exists(command.company_id, command.candidate_id):
            raise ValueError(
                f"Candidate {command.candidate_id} already exists in company {command.company_id} talent pool"
            )

        # Create talent pool entry
        entry = TalentPoolEntry.create(
            company_id=command.company_id,
            candidate_id=command.candidate_id,
            added_reason=command.added_reason,
            tags=command.tags,
            rating=command.rating,
            notes=command.notes,
            status=command.status,
            source_application_id=command.source_application_id,
            source_position_id=command.source_position_id,
            added_by_user_id=command.added_by_user_id,
        )

        # Save to repository
        self._repository.save(entry)
