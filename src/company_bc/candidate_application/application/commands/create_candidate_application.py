from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.candidate_bc.candidate.application.services.profile_markdown_service import ProfileMarkdownService
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candidate_project_repository_interface import \
    CandidateProjectRepositoryInterface
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.entities.base import generate_id


@dataclass
class CreateCandidateApplicationCommand(Command):
    """Comando para crear una aplicación de candidato"""
    candidate_id: str
    job_position_id: str
    notes: Optional[str] = None
    application_id: Optional[str] = None
    cv_file_id: Optional[str] = None  # Reference to attached CV file
    language: str = "es"  # Language for markdown rendering
    wants_cv_help: bool = False  # Flag indicating if candidate wants help creating their CV

    def get_candidate_id(self) -> CandidateId:
        """Convertir string a CandidateId value object"""
        return CandidateId(self.candidate_id)

    def get_job_position_id(self) -> JobPositionId:
        """Convertir string a JobPositionId value object"""
        return JobPositionId(self.job_position_id)


class CreateCandidateApplicationCommandHandler(CommandHandler[CreateCandidateApplicationCommand]):
    """Handler para crear aplicaciones de candidatos"""

    def __init__(
            self,
            candidate_application_repository: CandidateApplicationRepositoryInterface,
            candidate_repository: Optional[CandidateRepositoryInterface] = None,
            experience_repository: Optional[CandidateExperienceRepositoryInterface] = None,
            education_repository: Optional[CandidateEducationRepositoryInterface] = None,
            project_repository: Optional[CandidateProjectRepositoryInterface] = None
    ):
        self.candidate_application_repository = candidate_application_repository
        self.candidate_repository = candidate_repository
        self.experience_repository = experience_repository
        self.education_repository = education_repository
        self.project_repository = project_repository

    def execute(self, command: CreateCandidateApplicationCommand) -> None:
        """Ejecutar comando de crear aplicación"""
        # Check if application already exists
        existing_application = self.candidate_application_repository.get_by_candidate_and_position(
            command.get_candidate_id(),
            command.get_job_position_id()
        )

        if existing_application:
            # Application already exists, nothing to do
            return

        # Use provided ID or generate new one
        application_id = CandidateApplicationId(
            command.application_id if command.application_id else generate_id()
        )

        # Generate profile snapshots if repositories are available
        profile_markdown: Optional[str] = None
        profile_json: Optional[Dict[str, Any]] = None

        if self.candidate_repository:
            candidate = self.candidate_repository.get_by_id(command.get_candidate_id())
            if candidate:
                # Fetch related data
                experiences = []
                education = []
                projects = []

                if self.experience_repository:
                    experiences = self.experience_repository.get_by_candidate_id(
                        command.get_candidate_id()
                    )

                if self.education_repository:
                    education = self.education_repository.get_by_candidate_id(
                        command.get_candidate_id()
                    )

                if self.project_repository:
                    projects = self.project_repository.get_by_candidate_id(
                        command.get_candidate_id()
                    )

                # Generate markdown snapshot
                profile_markdown = ProfileMarkdownService.render(
                    candidate=candidate,
                    experiences=experiences,
                    education=education,
                    projects=projects,
                    language=command.language
                )

                # Generate JSON snapshot
                profile_json = ProfileMarkdownService.render_json_snapshot(
                    candidate=candidate,
                    experiences=experiences,
                    education=education,
                    projects=projects
                )

        # Create new application using factory method
        new_application = CandidateApplication.create(
            id=application_id,
            candidate_id=command.get_candidate_id(),
            job_position_id=command.get_job_position_id(),
            notes=command.notes,
            profile_snapshot_markdown=profile_markdown,
            profile_snapshot_json=profile_json,
            cv_file_id=command.cv_file_id,
            wants_cv_help=command.wants_cv_help
        )

        # Save application
        self.candidate_application_repository.save(new_application)
