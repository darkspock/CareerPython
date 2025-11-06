from dataclasses import dataclass
from datetime import datetime

from src.company_workflow.domain.enums.field_visibility import FieldVisibility
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.company_workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class FieldConfiguration:
    """Field configuration entity - defines how a custom field behaves in a specific stage"""
    id: FieldConfigurationId
    stage_id: WorkflowStageId
    custom_field_id: CustomFieldId
    visibility: FieldVisibility
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            id: FieldConfigurationId,
            stage_id: WorkflowStageId,
            custom_field_id: CustomFieldId,
            visibility: FieldVisibility
    ) -> "FieldConfiguration":
        """Factory method to create a new field configuration"""
        now = datetime.utcnow()
        return FieldConfiguration(
            id=id,
            stage_id=stage_id,
            custom_field_id=custom_field_id,
            visibility=visibility,
            created_at=now,
            updated_at=now
        )

    def update_visibility(self, visibility: FieldVisibility) -> "FieldConfiguration":
        """Update the visibility setting for this field in this stage"""
        return FieldConfiguration(
            id=self.id,
            stage_id=self.stage_id,
            custom_field_id=self.custom_field_id,
            visibility=visibility,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def is_editable(self) -> bool:
        """Check if the field is editable in this stage"""
        return self.visibility in [FieldVisibility.VISIBLE, FieldVisibility.REQUIRED]

    def is_required(self) -> bool:
        """Check if the field is required in this stage"""
        return self.visibility == FieldVisibility.REQUIRED

    def is_visible(self) -> bool:
        """Check if the field is visible in this stage"""
        return self.visibility != FieldVisibility.HIDDEN
