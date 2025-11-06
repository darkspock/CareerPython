from dataclasses import dataclass
from typing import Dict, Any

from src.shared.application.query_bus import Query, QueryHandler
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.customization.infrastructure.repositories.custom_field_value_repository import CustomFieldValueRepository
from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class GetCustomFieldValuesByCompanyCandidateQuery(Query):
    """Query to get custom field values for a company candidate"""
    company_candidate_id: CompanyCandidateId


class GetCustomFieldValuesByCompanyCandidateQueryHandler(
    QueryHandler[GetCustomFieldValuesByCompanyCandidateQuery, Dict[str, Any]]
):
    """Handler for getting custom field values by company candidate"""

    def __init__(
        self, 
        custom_field_value_repository: CustomFieldValueRepository,
        custom_field_repository: CustomFieldRepositoryInterface,
        company_candidate_repository: CompanyCandidateRepositoryInterface
    ):
        self._custom_field_value_repository = custom_field_value_repository
        self._custom_field_repository = custom_field_repository
        self._company_candidate_repository = company_candidate_repository

    def handle(self, query: GetCustomFieldValuesByCompanyCandidateQuery) -> Dict[str, Any]:
        """
        Handle the get custom field values by company candidate query
        Returns a dict keyed by field_key, with metadata and values for each field
        """
        # Get the company candidate to retrieve workflow_id
        company_candidate = self._company_candidate_repository.get_by_id(query.company_candidate_id)
        if not company_candidate or not company_candidate.workflow_id:
            # No workflow assigned, return empty dict
            return {}
        
        # Get all custom fields for the workflow (metadata)
        workflow_id = WorkflowId(company_candidate.workflow_id.value)
        custom_fields = self._custom_field_repository.list_by_workflow(workflow_id)
        
        # Get existing values for this candidate and workflow
        existing_value = self._custom_field_value_repository.get_by_company_candidate_and_workflow(
            query.company_candidate_id,
            workflow_id
        )
        values_dict = existing_value.values if existing_value else {}
        
        # Build result with ALL custom fields (including those without values)
        result = {}
        for custom_field in custom_fields:
            field_id = str(custom_field.id)
            field_key = custom_field.field_key
            # Read from JSON using field_id as key (not field_key, to avoid data loss on rename)
            # Try field_id first, then fallback to field_key for backward compatibility
            field_value = values_dict.get(field_id) if values_dict else None
            if field_value is None and values_dict:
                field_value = values_dict.get(field_key)
            
            # Return with field_key as key for frontend compatibility
            result[field_key] = {
                'id': str(existing_value.id) if existing_value else None,
                'field_id': field_id,
                'field_name': custom_field.field_name,
                'field_type': custom_field.field_type.value,
                'field_config': custom_field.field_config,
                'value': field_value,
                'created_at': existing_value.created_at.isoformat() if existing_value else None,
                'updated_at': existing_value.updated_at.isoformat() if existing_value else None
            }
        
        return result
