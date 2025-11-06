"""Delete job position workflow command"""
from dataclasses import dataclass

from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import (
    JobPositionWorkflowRepositoryInterface
)
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeleteJobPositionWorkflowCommand(Command):
    """Command to delete a job position workflow"""
    id: JobPositionWorkflowId


class DeleteJobPositionWorkflowCommandHandler(CommandHandler[DeleteJobPositionWorkflowCommand]):
    """Handler for DeleteJobPositionWorkflowCommand"""

    def __init__(self, repository: JobPositionWorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteJobPositionWorkflowCommand) -> None:
        """Execute the delete command"""
        self._repository.delete(command.id)
