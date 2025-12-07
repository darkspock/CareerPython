from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.job_position.domain.repositories.position_question_config_repository_interface import (
    PositionQuestionConfigRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class RemovePositionQuestionConfigCommand(Command):
    """
    Command to remove a question configuration from a position.

    This removes the position-specific override, reverting to workflow defaults.
    """
    position_id: str
    question_id: str


class RemovePositionQuestionConfigCommandHandler(CommandHandler[RemovePositionQuestionConfigCommand]):
    """Handler for RemovePositionQuestionConfigCommand."""

    def __init__(self, repository: PositionQuestionConfigRepositoryInterface):
        self.repository = repository

    def execute(self, command: RemovePositionQuestionConfigCommand) -> None:
        """Execute the command - removes the config if it exists."""
        position_id = JobPositionId(command.position_id)
        question_id = ApplicationQuestionId(command.question_id)

        # Find the existing config
        existing = self.repository.get_by_position_and_question(position_id, question_id)

        if existing:
            self.repository.delete(existing.id)
