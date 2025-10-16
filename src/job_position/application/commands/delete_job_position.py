from dataclasses import dataclass

from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command


@dataclass
class DeleteJobPositionCommand(Command):
    id: JobPositionId


class DeleteJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: DeleteJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        self.job_position_repository.delete(command.id)
