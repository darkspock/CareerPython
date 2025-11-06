from dataclasses import dataclass

from src.company_workflow.domain.entities.field_configuration import FieldConfiguration
from src.company_workflow.domain.enums.field_visibility import FieldVisibility
from src.company_workflow.domain.infrastructure.field_configuration_repository_interface import \
    FieldConfigurationRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ConfigureStageFieldCommand(Command):
    """Command to configure how a custom field behaves in a stage"""
    id: str
    stage_id: str
    custom_field_id: str
    visibility: str


class ConfigureStageFieldCommandHandler(CommandHandler[ConfigureStageFieldCommand]):
    """Handler for configuring a stage field"""

    def __init__(self, repository: FieldConfigurationRepositoryInterface):
        self._repository = repository

    def execute(self, command: ConfigureStageFieldCommand) -> None:
        """Handle the configure stage field command"""
        field_configuration = FieldConfiguration.create(
            id=FieldConfigurationId.from_string(command.id),
            stage_id=WorkflowStageId.from_string(command.stage_id),
            custom_field_id=CustomFieldId.from_string(command.custom_field_id),
            visibility=FieldVisibility(command.visibility)
        )

        self._repository.save(field_configuration)
