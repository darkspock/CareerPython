from dataclasses import dataclass
from typing import Dict, Any

from src.shared.application.query_bus import Query, QueryHandler
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.customization.infrastructure.repositories.custom_field_value_repository import CustomFieldValueRepository
from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class GetAllCustomFieldValuesByCompanyCandidateQuery(Query):
    """Query to get all custom field values for a company candidate, organized by workflow_id"""
    company_candidate_id: CompanyCandidateId


class GetAllCustomFieldValuesByCompanyCandidateQueryHandler(
    QueryHandler[GetAllCustomFieldValuesByCompanyCandidateQuery, Dict[str, Dict[str, Any]]]
):
    """Handler for getting all custom field values by company candidate, organized by workflow_id"""

    def __init__(
        self, 
        custom_field_value_repository: CustomFieldValueRepository,
        custom_field_repository: CustomFieldRepositoryInterface
    ):
        self._custom_field_value_repository = custom_field_value_repository
        self._custom_field_repository = custom_field_repository

    def handle(self, query: GetAllCustomFieldValuesByCompanyCandidateQuery) -> Dict[str, Dict[str, Any]]:
        """
        Handle the get all custom field values by company candidate query
        Returns a dict keyed by workflow_id, each containing a dict keyed by field_key with metadata and values
        """
        # Get all custom field values for this candidate (raw values organized by workflow_id)
        all_values = self._custom_field_value_repository.get_values_by_company_candidate(query.company_candidate_id)
        
        # Build result organized by workflow_id
        result = {}
        for workflow_id_str, values_dict in all_values.items():
            workflow_id = WorkflowId(workflow_id_str)
            
            # Get all custom fields for this workflow (metadata)
            custom_fields = self._custom_field_repository.list_by_workflow(workflow_id)
            
            # Build result with ALL custom fields (including those without values)
            workflow_result = {}
            for custom_field in custom_fields:
                field_id = str(custom_field.id)
                field_key = custom_field.field_key
                # Read from JSON using field_id as key (not field_key, to avoid data loss on rename)
                # Try field_id first, then fallback to field_key for backward compatibility
                field_value = values_dict.get(field_id) if values_dict else None
                if field_value is None and values_dict:
                    field_value = values_dict.get(field_key)
                
                # Get the CustomFieldValue entity to get id, created_at, updated_at
                existing_value = self._custom_field_value_repository.get_by_company_candidate_and_workflow(
                    query.company_candidate_id,
                    workflow_id
                )
                
                # Return with field_key as key for frontend compatibility
                workflow_result[field_key] = {
                    'id': str(existing_value.id) if existing_value else None,
                    'field_id': field_id,
                    'field_name': custom_field.field_name,
                    'field_type': custom_field.field_type.value,
                    'field_config': custom_field.field_config,
                    'value': field_value,
                    'created_at': existing_value.created_at.isoformat() if existing_value else None,
                    'updated_at': existing_value.updated_at.isoformat() if existing_value else None
                }
            
            # Only include workflow if it has custom fields
            if workflow_result:
                result[workflow_id_str] = workflow_result
        
        return result

