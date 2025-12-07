from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class UpdateApplicationQuestionCommand(Command):
    """Command to update an application question."""
    id: str
    label: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required_default: Optional[bool] = None
    validation_rules: Optional[Dict[str, Any]] = None
    sort_order: Optional[int] = None


class UpdateApplicationQuestionCommandHandler(CommandHandler[UpdateApplicationQuestionCommand]):
    """Handler for UpdateApplicationQuestionCommand."""

    def __init__(self, repository: ApplicationQuestionRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateApplicationQuestionCommand) -> None:
        """Execute the command."""
        question_id = ApplicationQuestionId.from_string(command.id)
        question = self.repository.get_by_id(question_id)

        if not question:
            raise ValueError(f"Application question not found: {command.id}")

        question.update(
            label=command.label,
            description=command.description,
            options=command.options,
            is_required_default=command.is_required_default,
            validation_rules=command.validation_rules,
            sort_order=command.sort_order
        )

        self.repository.save(question)
