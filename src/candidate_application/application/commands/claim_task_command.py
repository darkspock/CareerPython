"""
Claim Task Command
Phase 6: Command to claim/assign a task to the current user
"""

from dataclasses import dataclass

from src.candidate_application.domain.enums.task_status import TaskStatus
from src.candidate_application.domain.repositories.candidate_application_repository_interface import (
    CandidateApplicationRepositoryInterface
)
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ClaimTaskCommand(Command):
    """Command to claim a task (application) for processing"""
    application_id: str
    user_id: str


class ClaimTaskCommandHandler(CommandHandler[ClaimTaskCommand]):
    """Handler for claiming tasks"""

    def __init__(
            self,
            application_repository: CandidateApplicationRepositoryInterface
    ):
        self.application_repository = application_repository

    def execute(self, command: ClaimTaskCommand) -> None:
        """Claim a task by updating its status to in_progress

        When a user claims a task:
        1. Get the application
        2. Update task_status to IN_PROGRESS
        3. Save the application

        Note: User must have permission to process the stage (checked in controller)
        """
        # Get application
        application = self.application_repository.get_by_id(
            CandidateApplicationId(command.application_id)
        )

        if not application:
            raise ValueError(f"Application {command.application_id} not found")

        # Update task status to in_progress
        application.update_task_status(TaskStatus.IN_PROGRESS)

        # Save
        self.application_repository.save(application)
