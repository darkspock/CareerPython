"""Custom Field Value Controller."""
import ulid
from typing import Optional, Dict, Any

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.company_workflow.application.dtos.custom_field_value_dto import CustomFieldValueDto
from src.company_workflow.application.commands.create_custom_field_value_command import CreateCustomFieldValueCommand
from src.company_workflow.application.commands.update_custom_field_value_command import UpdateCustomFieldValueCommand
from src.company_workflow.application.commands.delete_custom_field_value_command import DeleteCustomFieldValueCommand
from src.company_workflow.application.queries.get_custom_field_value_by_id import GetCustomFieldValueByIdQuery
from src.company_workflow.application.queries.get_custom_field_values_by_company_candidate import GetCustomFieldValuesByCompanyCandidateQuery
from src.company_workflow.presentation.schemas.create_custom_field_value_request import CreateCustomFieldValueRequest
from src.company_workflow.presentation.schemas.update_custom_field_value_request import UpdateCustomFieldValueRequest
from src.company_workflow.presentation.schemas.custom_field_value_response import CustomFieldValueResponse
from src.company_workflow.presentation.mappers.custom_field_value_mapper import CustomFieldValueResponseMapper


class CustomFieldValueController:
    """Controller for custom field value operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_custom_field_value(self, request: CreateCustomFieldValueRequest) -> CustomFieldValueResponse:
        """Create a new custom field value record."""
        valueíc = str(ulid.new())

        command = CreateCustomFieldValueCommand(
            id=value_id,
            company_candidate_id=request.company_candidate_id,
            workflow_id=request.workflow_id,
            values=request.values
        )

        self._command_bus.dispatch(command)

        query = GetCustomFieldValueByIdQuery(id=value_id)
        dto: Optional[CustomFieldValueDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Custom field value not found after creation")

        return CustomFieldValueResponseMapper.dto_to_response(dto)

    def get_custom_field_value_by_id(self, value_id: str) -> Optional[CustomFieldValueResponse]:
        """Get a custom field value by ID."""
        query = GetCustomFieldValueByIdQuery(id=value_id)
        dto: Optional[CustomFieldValueDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CustomFieldValueResponseMapper.dto_to_response(dto)

    def get_custom_field_values_by_company_candidate(self, company_candidate_id: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all custom field values for a company candidate.
        Returns a dict keyed by workflow_id, each containing a dict of field_key -> value
        """
        from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
        query = GetCustomFieldValuesByCompanyCandidateQuery(
            company_candidate_id=CompanyCandidateId(company_candidate_id)
        )
        return self._query_bus.query(query)

    def update_custom_field_value(self, value_id: str, request: UpdateCustomFieldValueRequest) -> Optional[CustomFieldValueResponse]:
        """Update a custom field value (merge values with existing)."""
        command = UpdateCustomFieldValueCommand(
            id=value_id,
            values=request.values
        )

        self._command_bus.dispatch(command)

        # Return updated value
        query = GetCustomFieldValueByIdQuery(id=value_id)
        dto: Optional[CustomFieldValueDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CustomFieldValueResponseMapper.dto_to_response(dto)

    def delete_custom_field_value(self, value_id: str) -> None:
        """Delete a custom field value."""
        command = DeleteCustomFieldValueCommand(id=value_id)
        self._command_bus.dispatch(command)

