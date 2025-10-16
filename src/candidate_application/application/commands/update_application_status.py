from dataclasses import dataclass
from typing import Optional

from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdateApplicationStatusCommand(Command):
    """Comando para actualizar el estado de una aplicación"""
    application_id: str
    status: ApplicationStatusEnum
    notes: Optional[str] = None

    def get_application_id(self) -> CandidateApplicationId:
        """Convertir string a CandidateApplicationId value object"""
        return CandidateApplicationId(self.application_id)


class UpdateApplicationStatusCommandHandler(CommandHandler[UpdateApplicationStatusCommand]):
    """Handler para actualizar el estado de aplicaciones"""

    def __init__(self, candidate_application_repository: CandidateApplicationRepositoryInterface):
        self.candidate_application_repository = candidate_application_repository

    def execute(self, command: UpdateApplicationStatusCommand) -> None:
        """Ejecutar comando de actualizar estado de aplicación"""
        # Get existing application
        application = self.candidate_application_repository.get_by_id(
            command.get_application_id()
        )

        if not application:
            raise ValueError(f"Application with ID {command.application_id} not found")

        # Update status based on the new status
        if command.status == ApplicationStatusEnum.ACCEPTED:
            application.approve()
        elif command.status == ApplicationStatusEnum.REJECTED:
            application.reject(command.notes)
        elif command.status == ApplicationStatusEnum.REVIEWING:
            application.start_review()
        elif command.status == ApplicationStatusEnum.INTERVIEWED:
            application.mark_interviewed()
        elif command.status == ApplicationStatusEnum.WITHDRAWN:
            application.withdraw()
        else:
            # For other statuses, update directly
            application.application_status = command.status
            if command.notes:
                application.update_notes(command.notes)

        # Save updated application
        self.candidate_application_repository.save(application)
