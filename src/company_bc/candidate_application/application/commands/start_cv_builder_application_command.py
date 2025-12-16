"""
StartCVBuilderApplicationCommand

Creates a draft application for candidates who want help building their CV.
This initiates the CV Builder flow where the candidate fills in their profile
data step by step, and the system generates a professional CV for them.
"""
from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.entities.base import generate_id


@dataclass
class StartCVBuilderApplicationCommand(Command):
    """Command to start a CV builder application flow.

    This creates a draft application with PENDING_CV status, allowing
    the candidate to build their profile step by step before submitting.
    """
    candidate_id: str
    job_position_id: str
    application_id: Optional[str] = None  # Allow specifying ID for idempotency

    def get_candidate_id(self) -> CandidateId:
        """Convert string to CandidateId value object"""
        return CandidateId(self.candidate_id)

    def get_job_position_id(self) -> JobPositionId:
        """Convert string to JobPositionId value object"""
        return JobPositionId(self.job_position_id)


class StartCVBuilderApplicationCommandHandler(CommandHandler[StartCVBuilderApplicationCommand]):
    """Handler for starting CV builder application flow.

    Creates an application with PENDING_CV status that allows the candidate
    to build their profile through the wizard before final submission.
    """

    def __init__(
            self,
            candidate_application_repository: CandidateApplicationRepositoryInterface,
            candidate_repository: Optional[CandidateRepositoryInterface] = None
    ):
        self.candidate_application_repository = candidate_application_repository
        self.candidate_repository = candidate_repository

    def execute(self, command: StartCVBuilderApplicationCommand) -> None:
        """Execute the command to start CV builder application.

        Creates a new application with PENDING_CV status if one doesn't exist.
        If an application already exists for this candidate+position, does nothing.
        """
        # Check if application already exists for this candidate and position
        existing_application = self.candidate_application_repository.get_by_candidate_and_position(
            command.get_candidate_id(),
            command.get_job_position_id()
        )

        if existing_application:
            # Application already exists, nothing to do
            return

        # Verify candidate exists if repository is available
        if self.candidate_repository:
            candidate = self.candidate_repository.get_by_id(command.get_candidate_id())
            if not candidate:
                raise ValueError(f"Candidate not found: {command.candidate_id}")

        # Generate application ID
        application_id = CandidateApplicationId(
            command.application_id if command.application_id else generate_id()
        )

        # Create application with PENDING_CV status (no snapshot yet)
        new_application = CandidateApplication.create(
            id=application_id,
            candidate_id=command.get_candidate_id(),
            job_position_id=command.get_job_position_id(),
            notes="CV Builder flow - pending profile completion",
            profile_snapshot_markdown=None,
            profile_snapshot_json=None,
            cv_file_id=None
        )

        # Set status to PENDING_CV (waiting for CV generation)
        new_application.application_status = ApplicationStatusEnum.PENDING_CV

        # Save the draft application
        self.candidate_application_repository.save(new_application)
