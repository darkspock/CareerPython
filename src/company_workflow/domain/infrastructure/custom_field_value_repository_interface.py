from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_workflow.domain.entities.custom_field_value import CustomFieldValue
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId


class CustomFieldValueRepositoryInterface(ABC):
    """Interface for custom field value repository operations"""

    @abstractmethod
    def save(self, custom_field_value: CustomFieldValue) -> None:
        """Save a custom field value (one record per company_candidate + workflow)"""
        pass

    @abstractmethod
    def get_by_id(self, custom_field_value_id: CustomFieldValueId) -> Optional[CustomFieldValue]:
        """Get custom field value by ID"""
        pass

    @abstractmethod
    def get_by_company_candidate_and_workflow(
            self,
            company_candidate_id: CompanyCandidateId,
            workflow_id: CompanyWorkflowId
    ) -> Optional[CustomFieldValue]:
        """Get custom field value by company candidate and workflow"""
        pass

    @abstractmethod
    def get_values_by_company_candidate(
            self,
            company_candidate_id: CompanyCandidateId
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get all custom field values for a company candidate
        Returns a dict keyed by workflow_id, each containing a dict of field_key -> value
        """
        pass

    @abstractmethod
    def delete(self, custom_field_value_id: CustomFieldValueId) -> None:
        """Delete a custom field value"""
        pass
