from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.entities.application_question import (
    ApplicationQuestion
)
from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass
class CreateApplicationQuestionCommand(Command):
    """Command to create a new application question."""
    id: str
    workflow_id: str
    company_id: str
    field_key: str
    label: str
    field_type: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required_default: bool = False
    validation_rules: Optional[Dict[str, Any]] = None
    sort_order: int = 0


class CreateApplicationQuestionCommandHandler(CommandHandler[CreateApplicationQuestionCommand]):
    """Handler for CreateApplicationQuestionCommand."""

    def __init__(self, repository: ApplicationQuestionRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateApplicationQuestionCommand) -> None:
        """Execute the command."""
        # Check if field_key already exists in workflow
        workflow_id = WorkflowId.from_string(command.workflow_id)
        existing = self.repository.get_by_field_key(workflow_id, command.field_key)
        if existing:
            raise ValueError(f"Field key '{command.field_key}' already exists in this workflow")

        # Create the entity
        question = ApplicationQuestion.create(
            id=ApplicationQuestionId.from_string(command.id),
            workflow_id=workflow_id,
            company_id=CompanyId.from_string(command.company_id),
            field_key=command.field_key,
            label=command.label,
            field_type=ApplicationQuestionFieldType(command.field_type),
            description=command.description,
            options=command.options,
            is_required_default=command.is_required_default,
            validation_rules=command.validation_rules,
            sort_order=command.sort_order
        )

        self.repository.save(question)
