"""
CompleteApplicationWithGeneratedCVCommand

Finalizes a CV builder application by generating the profile snapshot
and attaching the generated CV. Transitions the application from
PENDING_CV to APPLIED status.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.candidate_bc.candidate.application.services.profile_markdown_service import ProfileMarkdownService
from src.candidate_bc.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candidate_project_repository_interface import \
    CandidateProjectRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class CompleteApplicationWithGeneratedCVCommand(Command):
    """Command to complete a CV builder application.

    Finalizes the application by generating a profile snapshot from
    the candidate's current profile data and attaching the generated CV.
    """
    application_id: str
    cv_file_id: Optional[str] = None  # Reference to the generated CV file
    language: str = "es"  # Language for markdown rendering

    def get_application_id(self) -> CandidateApplicationId:
        """Convert string to CandidateApplicationId value object"""
        return CandidateApplicationId(self.application_id)


class CompleteApplicationWithGeneratedCVCommandHandler(CommandHandler[CompleteApplicationWithGeneratedCVCommand]):
    """Handler for completing CV builder application.

    Generates the profile snapshot from current candidate data,
    attaches the CV file, and transitions status to APPLIED.
    """

    def __init__(
            self,
            candidate_application_repository: CandidateApplicationRepositoryInterface,
            candidate_repository: CandidateRepositoryInterface,
            experience_repository: CandidateExperienceRepositoryInterface,
            education_repository: CandidateEducationRepositoryInterface,
            project_repository: CandidateProjectRepositoryInterface
    ):
        self.candidate_application_repository = candidate_application_repository
        self.candidate_repository = candidate_repository
        self.experience_repository = experience_repository
        self.education_repository = education_repository
        self.project_repository = project_repository

    def execute(self, command: CompleteApplicationWithGeneratedCVCommand) -> None:
        """Execute the command to complete CV builder application.

        Generates snapshot, attaches CV, and submits the application.
        """
        # Get the application
        application = self.candidate_application_repository.get_by_id(
            command.get_application_id()
        )

        if not application:
            raise ValueError(f"Application not found: {command.application_id}")

        # Verify application is in PENDING_CV or DRAFT status
        if application.application_status not in [ApplicationStatusEnum.PENDING_CV, ApplicationStatusEnum.DRAFT]:
            raise ValueError(
                f"Application cannot be completed. Current status: {application.application_status.value}. "
                f"Expected: {ApplicationStatusEnum.PENDING_CV.value} or {ApplicationStatusEnum.DRAFT.value}"
            )

        # Fetch candidate data
        candidate = self.candidate_repository.get_by_id(application.candidate_id)
        if not candidate:
            raise ValueError(f"Candidate not found for application: {command.application_id}")

        # Fetch related profile data
        experiences = self.experience_repository.get_by_candidate_id(application.candidate_id)
        education = self.education_repository.get_by_candidate_id(application.candidate_id)
        projects = self.project_repository.get_by_candidate_id(application.candidate_id)

        # Generate profile snapshots
        profile_markdown = ProfileMarkdownService.render(
            candidate=candidate,
            experiences=experiences,
            education=education,
            projects=projects,
            language=command.language
        )

        profile_json = ProfileMarkdownService.render_json_snapshot(
            candidate=candidate,
            experiences=experiences,
            education=education,
            projects=projects
        )

        # Update application with snapshot and CV
        application.profile_snapshot_markdown = profile_markdown
        application.profile_snapshot_json = profile_json

        if command.cv_file_id:
            application.cv_file_id = command.cv_file_id

        # Transition to APPLIED status
        application.application_status = ApplicationStatusEnum.APPLIED

        # Save the completed application
        self.candidate_application_repository.save(application)
