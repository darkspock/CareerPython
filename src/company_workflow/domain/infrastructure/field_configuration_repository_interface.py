from abc import ABC, abstractmethod
from typing import Optional, List

from src.company_workflow.domain.entities.field_configuration import FieldConfiguration
from src.company_workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId


class FieldConfigurationRepositoryInterface(ABC):
    """Repository interface for field configuration operations"""

    @abstractmethod
    def save(self, field_configuration: FieldConfiguration) -> None:
        """Save a field configuration"""
        pass

    @abstractmethod
    def get_by_id(self, field_configuration_id: FieldConfigurationId) -> Optional[FieldConfiguration]:
        """Get field configuration by ID"""
        pass

    @abstractmethod
    def list_by_stage(self, stage_id: WorkflowStageId) -> List[FieldConfiguration]:
        """List all field configurations for a stage"""
        pass

    @abstractmethod
    def get_by_stage_and_field(self, stage_id: WorkflowStageId, custom_field_id: CustomFieldId) -> Optional[FieldConfiguration]:
        """Get a field configuration by stage ID and custom field ID"""
        pass

    @abstractmethod
    def delete(self, field_configuration_id: FieldConfigurationId) -> None:
        """Delete a field configuration"""
        pass

    @abstractmethod
    def delete_by_stage(self, stage_id: WorkflowStageId) -> None:
        """Delete all field configurations for a stage"""
        pass
