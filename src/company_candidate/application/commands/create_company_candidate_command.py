from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List

import ulid

from src.shared.application.command import Command, CommandHandler
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.company_candidate.domain.entities.company_candidate import CompanyCandidate
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company.domain.value_objects.company_id import CompanyId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_candidate.domain.value_objects.visibility_settings import VisibilitySettings
from src.company_candidate.domain.enums.candidate_priority import CandidatePriority


@dataclass(frozen=True)
class CreateCompanyCandidateCommand(Command):
    """Command to create a new company candidate relationship"""
    id: str
    company_id: str
    candidate_id: str
    created_by_user_id: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: str = "medium"
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    internal_notes: str = ""


class CreateCompanyCandidateCommandHandler(CommandHandler[CreateCompanyCandidateCommand, None]):
    """Handler for creating a new company candidate relationship"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def handle(self, command: CreateCompanyCandidateCommand) -> None:
        """Handle the create company candidate command"""
        # Parse visibility settings or use default
        visibility_settings = VisibilitySettings.from_dict(command.visibility_settings) if command.visibility_settings else VisibilitySettings.default()

        # Create the company candidate entity
        company_candidate = CompanyCandidate.create(
            id=CompanyCandidateId.from_string(command.id),
            company_id=CompanyId.from_string(command.company_id),
            candidate_id=CandidateId.from_string(command.candidate_id),
            created_by_user_id=CompanyUserId.from_string(command.created_by_user_id),
            position=command.position,
            department=command.department,
            priority=CandidatePriority(command.priority),
            visibility_settings=visibility_settings,
            tags=command.tags or [],
            internal_notes=command.internal_notes
        )

        # Save to repository
        self._repository.save(company_candidate)