from dataclasses import dataclass
from typing import Optional, Dict, List

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.company.domain.value_objects.company_id import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_candidate.domain.entities.company_candidate import CompanyCandidate
from src.company_candidate.domain.enums.candidate_priority import CandidatePriority
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.value_objects.visibility_settings import VisibilitySettings
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateCompanyCandidateCommand(Command):
    """Command to create a new company candidate relationship"""
    id: CompanyCandidateId
    company_id: CompanyId
    candidate_id: CandidateId
    created_by_user_id: CompanyUserId
    source: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: CandidatePriority = CandidatePriority.MEDIUM
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    internal_notes: str = ""
    lead_id: Optional[str] = None
    resume_url: Optional[str] = None
    resume_uploaded_by: Optional[CompanyUserId] = None


class CreateCompanyCandidateCommandHandler(CommandHandler):
    """Handler for creating a new company candidate relationship"""

    def __init__(self, repository: CompanyCandidateRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateCompanyCandidateCommand) -> None:
        """Handle the create company candidate command"""
        # Parse visibility settings or use default
        visibility_settings = VisibilitySettings.from_dict(
            command.visibility_settings) if command.visibility_settings else VisibilitySettings.default()

        # Create the company candidate entity
        company_candidate = CompanyCandidate.create(
            id=command.id,
            company_id=command.company_id,
            candidate_id=command.candidate_id,
            created_by_user_id=command.created_by_user_id,
            source=command.source,
            position=command.position,
            department=command.department,
            priority=command.priority,
            visibility_settings=visibility_settings,
            tags=command.tags or [],
            internal_notes=command.internal_notes,
            lead_id=command.lead_id,
            resume_url=command.resume_url,
            resume_uploaded_by=command.resume_uploaded_by
        )

        # Save to repository
        self._repository.save(company_candidate)
