from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company_workflow.domain.entities.custom_field import CustomField
from src.company_workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.enums.field_type import FieldType
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateCustomFieldCommand(Command):
    """Command to create a new custom field"""
    id: str
    workflow_id: str
    field_key: str
    field_name: str
    field_type: str
    order_index: int
    field_config: Optional[Dict[str, Any]] = None


class CreateCustomFieldCommandHandler(CommandHandler[CreateCustomFieldCommand]):
    """Handler for creating a new custom field"""

    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateCustomFieldCommand) -> None:
        """Handle the create custom field command"""
        custom_field = CustomField.create(
            id=CustomFieldId.from_string(command.id),
            workflow_id=CompanyWorkflowId.from_string(command.workflow_id),
            field_key=command.field_key,
            field_name=command.field_name,
            field_type=FieldType(command.field_type),
            order_index=command.order_index,
            field_config=command.field_config
        )

        self._repository.save(custom_field)
