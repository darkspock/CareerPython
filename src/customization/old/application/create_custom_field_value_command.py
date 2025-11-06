from dataclasses import dataclass
from typing import Dict, Any, Optional

from src.shared.application.command_bus import Command, CommandHandler
from src.workflow.domain.entities.custom_field_value import CustomFieldValue
from src.workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.infrastructure.custom_field_value_repository_interface import CustomFieldValueRepositoryInterface


@dataclass(frozen=True)
class CreateCustomFieldValueCommand(Command):
    """Command to create a new custom field value record (one per candidate+workflow)"""
    id: str
    company_candidate_id: str
    workflow_id: str
    values: Optional[Dict[str, Any]] = None


class CreateCustomFieldValueCommandHandler(CommandHandler[CreateCustomFieldValueCommand]):
    """Handler for creating custom field values"""

    def __init__(self, repository: CustomFieldValueRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateCustomFieldValueCommand) -> None:
        """Handle the create custom field value command"""
        custom_field_value = CustomFieldValue.create(
            id=CustomFieldValueId(command.id),
            company_candidate_id=CompanyCandidateId(command.company_candidate_id),
            workflow_id=WorkflowId(command.workflow_id),
            values=command.values
        )
        
        self._repository.save(custom_field_value)
