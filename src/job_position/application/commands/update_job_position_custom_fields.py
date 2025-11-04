from dataclasses import dataclass
from typing import Dict, Any

from src.shared.application.command_bus import Command, CommandHandler
from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface


@dataclass
class UpdateJobPositionCustomFieldsCommand(Command):
    """Command to update custom fields values for a job position"""
    id: JobPositionId
    custom_fields_values: Dict[str, Any]


class UpdateJobPositionCustomFieldsCommandHandler(CommandHandler[UpdateJobPositionCustomFieldsCommand]):
    """Handler for updating custom fields values"""

    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: UpdateJobPositionCustomFieldsCommand) -> None:
        """Execute the command - updates custom fields values"""
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        # Update custom fields values
        job_position.custom_fields_values = command.custom_fields_values
        job_position.updated_at = job_position.updated_at or None  # Will be updated by repository

        self.job_position_repository.save(job_position)

