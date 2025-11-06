from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.validation_rule import ValidationRule
from ..value_objects.validation_rule_id import ValidationRuleId
from src.workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class ValidationRuleRepositoryInterface(ABC):
    """Repository interface for validation rule operations."""

    @abstractmethod
    def save(self, validation_rule: ValidationRule) -> None:
        """Save a validation rule."""
        pass

    @abstractmethod
    def get_by_id(self, rule_id: ValidationRuleId) -> Optional[ValidationRule]:
        """Get validation rule by ID."""
        pass

    @abstractmethod
    def list_by_stage(self, stage_id: WorkflowStageId, active_only: bool = False) -> List[ValidationRule]:
        """List all validation rules for a stage, ordered by creation date."""
        pass

    @abstractmethod
    def list_by_custom_field(self, field_id: CustomFieldId, active_only: bool = False) -> List[ValidationRule]:
        """List all validation rules for a custom field."""
        pass

    @abstractmethod
    def delete(self, rule_id: ValidationRuleId) -> None:
        """Delete a validation rule."""
        pass
