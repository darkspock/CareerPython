from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class DeleteApplicationQuestionCommand(Command):
    """Command to delete an application question."""
    id: str


class DeleteApplicationQuestionCommandHandler(CommandHandler[DeleteApplicationQuestionCommand]):
    """Handler for DeleteApplicationQuestionCommand."""

    def __init__(self, repository: ApplicationQuestionRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteApplicationQuestionCommand) -> None:
        """Execute the command."""
        question_id = ApplicationQuestionId.from_string(command.id)
        question = self.repository.get_by_id(question_id)

        if not question:
            raise ValueError(f"Application question not found: {command.id}")

        self.repository.delete(question_id)
