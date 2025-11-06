from abc import ABC, abstractmethod
from typing import Optional, List

from src.company_workflow.domain.entities.custom_field import CustomField
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId


class CustomFieldRepositoryInterface(ABC):
    """Repository interface for custom field operations"""

    @abstractmethod
    def save(self, custom_field: CustomField) -> None:
        """Save a custom field"""
        pass

    @abstractmethod
    def get_by_id(self, custom_field_id: CustomFieldId) -> Optional[CustomField]:
        """Get custom field by ID"""
        pass

    @abstractmethod
    def list_by_workflow(self, workflow_id: CompanyWorkflowId) -> List[CustomField]:
        """List all custom fields for a workflow, ordered by order_index"""
        pass

    @abstractmethod
    def get_by_workflow_and_key(self, workflow_id: CompanyWorkflowId, field_key: str) -> Optional[CustomField]:
        """Get a custom field by workflow ID and field key"""
        pass

    @abstractmethod
    def delete(self, custom_field_id: CustomFieldId) -> None:
        """Delete a custom field"""
        pass
