"""Custom Field Value Controller."""
import ulid
from typing import Optional, Dict, Any

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.customization.old.application.custom_field_value_dto import CustomFieldValueDto
from src.customization.applicatoin.create_custom_field_value_command import CreateCustomFieldValueCommand
from src.customization.old.application.update_custom_field_value_command import UpdateCustomFieldValueCommand
from src.customization.old.application.delete_custom_field_value_command import DeleteCustomFieldValueCommand
from src.customization.old.application.get_custom_field_value_by_id import GetCustomFieldValueByIdQuery
from src.customization.old.application.get_custom_field_values_by_company_candidate import GetCustomFieldValuesByCompanyCandidateQuery
from src.customization.old.application.get_all_custom_field_values_by_company_candidate import GetAllCustomFieldValuesByCompanyCandidateQuery
from src.customization.old.application.get_custom_field_by_id import GetCustomFieldByIdQuery
from src.customization.old.application.custom_field_dto import CustomFieldDto
from src.customization.old.infrastructure.repositories.custom_field_value_repository import CustomFieldValueRepository
from src.customization.old.create_custom_field_value_request import CreateCustomFieldValueRequest
from src.customization.old.update_custom_field_value_request import UpdateCustomFieldValueRequest
from src.customization.old.custom_field_value_response import CustomFieldValueResponse
from src.customization.old.custom_field_value_mapper import CustomFieldValueResponseMapper


class CustomFieldValueController:
    """Controller for custom field value operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus, custom_field_value_repository: CustomFieldValueRepository):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._custom_field_value_repository = custom_field_value_repository

    def create_custom_field_value(self, request: CreateCustomFieldValueRequest) -> CustomFieldValueResponse:
        """Create a new custom field value record."""
        value_id = str(ulid.new())

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

    def get_custom_field_values_by_company_candidate(self, company_candidate_id: str) -> Dict[str, Any]:
        """
        Get all custom field values for a company candidate.
        Returns a dict keyed by field_key, with metadata and values for each field
        """
        from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
        query = GetCustomFieldValuesByCompanyCandidateQuery(
            company_candidate_id=CompanyCandidateId(company_candidate_id)
        )
        return self._query_bus.query(query)

    def get_all_custom_field_values_by_company_candidate(self, company_candidate_id: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all custom field values for a company candidate, organized by workflow_id.
        Returns a dict keyed by workflow_id, each containing a dict keyed by field_key with metadata and values
        """
        from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
        query = GetAllCustomFieldValuesByCompanyCandidateQuery(
            company_candidate_id=CompanyCandidateId(company_candidate_id)
        )
        return self._query_bus.query(query)

    def update_custom_field_value(self, value_id: str, request: UpdateCustomFieldValueRequest) -> Optional[CustomFieldValueResponse]:
        """Update a custom field value (merge values with existing)."""
        # Handle backward compatibility: if field_value is provided but not values, 
        # we need to get the existing value to know which field_key to update
        # For now, if only field_value is provided, we can't update without knowing the field_key
        # So we'll require values to be provided
        values_to_update = request.values
        if not values_to_update and request.field_value is not None:
            # Backward compatibility: if only field_value is provided, we can't determine which field to update
            # This case should be handled by the upsert_single_field_value method instead
            raise ValueError("Cannot update with field_value alone. Use values dict or upsert_single_field_value endpoint.")
        
        command = UpdateCustomFieldValueCommand(
            id=value_id,
            values=values_to_update
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

    def upsert_single_field_value(
        self, 
        company_candidate_id: str, 
        custom_field_id: str, 
        value: Any
    ) -> CustomFieldValueResponse:
        """
        Update or create a single custom field value for a company candidate.
        This is a convenience method for updating individual fields.
        """
        from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
        from src.workflow.domain.value_objects.custom_field_id import CustomFieldId
        from src.workflow.domain.value_objects.workflow_id import WorkflowId
        from src.workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
        
        # Get custom field to obtain field_key and workflow_id
        custom_field_query = GetCustomFieldByIdQuery(id=custom_field_id)
        custom_field_dto: Optional[CustomFieldDto] = self._query_bus.query(custom_field_query)
        if not custom_field_dto:
            raise ValueError(f"Custom field with id {custom_field_id} not found")
        
        field_id = custom_field_dto.id
        workflow_id = WorkflowId(custom_field_dto.workflow_id)
        
        # Get existing CustomFieldValue record
        company_candidate_id_vo = CompanyCandidateId(company_candidate_id)
        existing_value = self._custom_field_value_repository.get_by_company_candidate_and_workflow(
            company_candidate_id_vo,
            workflow_id
        )
        
        # Get workflow_id - use from custom field
        workflow_id_str = custom_field_dto.workflow_id
        
        # Store in JSON using field_id as key (not field_key, to avoid data loss on rename)
        values_to_store = {field_id: value}
        
        if existing_value:
            # Update existing - merge with existing values
            update_request = UpdateCustomFieldValueRequest(values=values_to_store)
            result = self.update_custom_field_value(str(existing_value.id), update_request)
            if not result:
                raise ValueError(f"Failed to update custom field value")
            return result
        else:
            # Create new CustomFieldValue record for this workflow
            create_request = CreateCustomFieldValueRequest(
                company_candidate_id=company_candidate_id,
                workflow_id=workflow_id_str,
                values=values_to_store
            )
            return self.create_custom_field_value(create_request)
