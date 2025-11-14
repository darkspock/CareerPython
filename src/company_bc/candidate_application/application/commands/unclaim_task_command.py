"""
Unclaim Task Command
Phase 6: Command to release/unclaim a task back to available pool
"""

from dataclasses import dataclass

from src.company_bc.candidate_application.domain.enums.task_status import TaskStatus
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import (
    CandidateApplicationRepositoryInterface
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UnclaimTaskCommand(Command):
    """Command to unclaim/release a task"""
    application_id: str
    user_id: str


class UnclaimTaskCommandHandler(CommandHandler[UnclaimTaskCommand]):
    """Handler for unclaiming tasks"""

    def __init__(
            self,
            application_repository: CandidateApplicationRepositoryInterface
    ):
        self.application_repository = application_repository

    def execute(self, command: UnclaimTaskCommand) -> None:
        """Release a task back to pending status

        When a user unclaims a task:
        1. Get the application
        2. Update task_status back to PENDING
        3. Save the application
        """
        # Get application
        application = self.application_repository.get_by_id(
            CandidateApplicationId(command.application_id)
        )

        if not application:
            raise ValueError(f"Application {command.application_id} not found")

        # Update task status back to pending
        application.update_task_status(TaskStatus.PENDING)

        # Save
        self.application_repository.save(application)
