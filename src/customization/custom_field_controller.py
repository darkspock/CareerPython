"""Custom Field Controller."""
import ulid
from typing import List, Optional

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.customization.application.custom_field_dto import CustomFieldDto
from src.customization.application.field_configuration_dto import FieldConfigurationDto
from src.customization.applicatoin.create_custom_field_command import CreateCustomFieldCommand
from src.customization.application.update_custom_field_command import UpdateCustomFieldCommand
from src.customization.application.delete_custom_field_command import DeleteCustomFieldCommand
from src.customization.application.reorder_custom_field_command import ReorderCustomFieldCommand
from src.customization.applicatoin.configure_stage_field_command import ConfigureStageFieldCommand
from src.customization.application.update_field_visibility_command import UpdateFieldVisibilityCommand
from src.customization.application.get_custom_field_by_id import GetCustomFieldByIdQuery
from src.customization.application.list_custom_fields_by_workflow import ListCustomFieldsByWorkflowQuery
from src.customization.application.list_field_configurations_by_stage import ListFieldConfigurationsByStageQuery
from src.customization.application.get_field_configuration_by_id import GetFieldConfigurationByIdQuery
from src.customization.create_custom_field_request import CreateCustomFieldRequest
from src.customization.update_custom_field_request import UpdateCustomFieldRequest
from src.customization.reorder_custom_field_request import ReorderCustomFieldRequest
from src.customization.configure_stage_field_request import ConfigureStageFieldRequest
from src.customization.custom_field_response import CustomFieldResponse
from src.customization.field_configuration_response import FieldConfigurationResponse
from src.customization.custom_field_mapper import CustomFieldResponseMapper
from adapters.http.workflow.mappers.field_configuration_mapper import FieldConfigurationResponseMapper


class CustomFieldController:
    """Controller for custom field operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_custom_field(self, request: CreateCustomFieldRequest) -> CustomFieldResponse:
        """Create a new custom field."""
        field_id = str(ulid.new())

        command = CreateCustomFieldCommand(
            id=field_id,
            workflow_id=request.workflow_id,
            field_key=request.field_key,
            field_name=request.field_name,
            field_type=request.field_type,
            order_index=request.order_index,
            field_config=request.field_config
        )

        self._command_bus.dispatch(command)

        query = GetCustomFieldByIdQuery(id=field_id)
        dto: Optional[CustomFieldDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Custom field not found after creation")

        return CustomFieldResponseMapper.dto_to_response(dto)

    def get_custom_field_by_id(self, field_id: str) -> Optional[CustomFieldResponse]:
        """Get a custom field by ID."""
        query = GetCustomFieldByIdQuery(id=field_id)
        dto: Optional[CustomFieldDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CustomFieldResponseMapper.dto_to_response(dto)

    def list_custom_fields_by_workflow(self, workflow_id: str) -> List[CustomFieldResponse]:
        """List all custom fields for a workflow."""
        query = ListCustomFieldsByWorkflowQuery(workflow_id=workflow_id)
        dtos: List[CustomFieldDto] = self._query_bus.query(query)

        return [CustomFieldResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_custom_field(self, field_id: str, request: UpdateCustomFieldRequest) -> CustomFieldResponse:
        """Update a custom field."""
        command = UpdateCustomFieldCommand(
            id=field_id,
            field_name=request.field_name,
            field_type=request.field_type,
            field_config=request.field_config
        )

        self._command_bus.dispatch(command)

        query = GetCustomFieldByIdQuery(id=field_id)
        dto: Optional[CustomFieldDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Custom field not found after update")

        return CustomFieldResponseMapper.dto_to_response(dto)

    def reorder_custom_field(self, field_id: str, request: ReorderCustomFieldRequest) -> CustomFieldResponse:
        """Reorder a custom field."""
        command = ReorderCustomFieldCommand(
            id=field_id,
            new_order_index=request.new_order_index
        )

        self._command_bus.dispatch(command)

        query = GetCustomFieldByIdQuery(id=field_id)
        dto: Optional[CustomFieldDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Custom field not found after reorder")

        return CustomFieldResponseMapper.dto_to_response(dto)

    def delete_custom_field(self, field_id: str) -> None:
        """Delete a custom field."""
        command = DeleteCustomFieldCommand(id=field_id)
        self._command_bus.dispatch(command)

    def configure_stage_field(self, request: ConfigureStageFieldRequest) -> FieldConfigurationResponse:
        """Configure how a custom field behaves in a stage."""
        config_id = str(ulid.new())

        command = ConfigureStageFieldCommand(
            id=config_id,
            stage_id=request.stage_id,
            custom_field_id=request.custom_field_id,
            visibility=request.visibility
        )

        self._command_bus.dispatch(command)

        # Return the configuration by querying all configs for the stage
        # and finding the one we just created
        query = ListFieldConfigurationsByStageQuery(stage_id=request.stage_id)
        dtos: List[FieldConfigurationDto] = self._query_bus.query(query)

        # Find the config we just created
        created_dto = next((dto for dto in dtos if dto.id == config_id), None)

        if not created_dto:
            raise Exception("Field configuration not found after creation")

        return FieldConfigurationResponseMapper.dto_to_response(created_dto)

    def update_field_visibility(self, config_id: str, visibility: str) -> FieldConfigurationResponse:
        """Update field visibility in a stage."""
        command = UpdateFieldVisibilityCommand(
            id=config_id,
            visibility=visibility
        )

        self._command_bus.dispatch(command)

        query = GetFieldConfigurationByIdQuery(id=config_id)
        dto: Optional[FieldConfigurationDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Field configuration not found after update")

        return FieldConfigurationResponseMapper.dto_to_response(dto)

    def list_field_configurations_by_stage(self, stage_id: str) -> List[FieldConfigurationResponse]:
        """List all field configurations for a stage."""
        query = ListFieldConfigurationsByStageQuery(stage_id=stage_id)
        dtos: List[FieldConfigurationDto] = self._query_bus.query(query)

        return [FieldConfigurationResponseMapper.dto_to_response(dto) for dto in dtos]
