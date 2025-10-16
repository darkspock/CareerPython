from dataclasses import dataclass
from typing import Optional

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.entities.base import generate_id


@dataclass
class CreateCandidateApplicationCommand(Command):
    """Comando para crear una aplicación de candidato"""
    candidate_id: str
    job_position_id: str
    notes: Optional[str] = None
    application_id: Optional[str] = None

    def get_candidate_id(self) -> CandidateId:
        """Convertir string a CandidateId value object"""
        return CandidateId(self.candidate_id)

    def get_job_position_id(self) -> JobPositionId:
        """Convertir string a JobPositionId value object"""
        return JobPositionId(self.job_position_id)


class CreateCandidateApplicationCommandHandler(CommandHandler[CreateCandidateApplicationCommand]):
    """Handler para crear aplicaciones de candidatos"""

    def __init__(self, candidate_application_repository: CandidateApplicationRepositoryInterface):
        self.candidate_application_repository = candidate_application_repository

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

        # Create new application using factory method
        new_application = CandidateApplication.create(
            id=application_id,
            candidate_id=command.get_candidate_id(),
            job_position_id=command.get_job_position_id(),
            notes=command.notes
        )

        # Save application
        self.candidate_application_repository.save(new_application)
