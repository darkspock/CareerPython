from dataclasses import dataclass
from typing import Optional, Dict, List

from src.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.shared.application.command import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.value_objects.visibility_settings import VisibilitySettings
from src.company_candidate.domain.enums.candidate_priority import CandidatePriority


@dataclass(frozen=True)
class UpdateCompanyCandidateCommand(Command):
    """Command to update company candidate information"""
    id: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: Optional[str] = None
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    internal_notes: Optional[str] = None


class UpdateCompanyCandidateCommandHandler(CommandHandler[UpdateCompanyCandidateCommand, None]):
    """Handler for updating company candidate information"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: UpdateCompanyCandidateCommand) -> None:
        """Handle the update company candidate command"""
        # Get existing company candidate
        company_candidate_id = CompanyCandidateId.from_string(command.id)
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Parse visibility settings if provided
        visibility_settings = None
        if command.visibility_settings is not None:
            visibility_settings = VisibilitySettings.from_dict(command.visibility_settings)

        # Parse priority if provided
        priority = None
        if command.priority is not None:
            priority = CandidatePriority(command.priority)

        # Update the company candidate
        updated_candidate = company_candidate.update(
            position=command.position if command.position is not None else company_candidate.position,
            department=command.department if command.department is not None else company_candidate.department,
            priority=priority if priority is not None else company_candidate.priority,
            visibility_settings=visibility_settings if visibility_settings is not None else company_candidate.visibility_settings,
            tags=command.tags if command.tags is not None else company_candidate.tags,
            internal_notes=command.internal_notes if command.internal_notes is not None else company_candidate.internal_notes
        )

        # Save to repository
        self._repository.save(updated_candidate)