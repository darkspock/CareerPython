from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId


@dataclass(frozen=True)
class CustomFieldValue:
    """
    Custom field value entity - stores all custom field values for a company candidate in a single JSON
    This improves performance by having one record per candidate+workflow instead of one per field
    """
    id: CustomFieldValueId
    company_candidate_id: CompanyCandidateId
    workflow_id: CompanyWorkflowId
    values: Dict[
        str, Any]  # JSON with all field values, keyed by field_id (not field_key, to avoid data loss on rename)
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            id: CustomFieldValueId,
            company_candidate_id: CompanyCandidateId,
            workflow_id: CompanyWorkflowId,
            values: Optional[Dict[str, Any]] = None
    ) -> "CustomFieldValue":
        """Create a corresponding custom field value record"""
        now = datetime.utcnow()
        return CustomFieldValue(
            id=id,
            company_candidate_id=company_candidate_id,
            workflow_id=workflow_id,
            values=values or {},
            created_at=now,
            updated_at=now
        )

    def update_values(self, new_values: Dict[str, Any]) -> "CustomFieldValue":
        """Update all field values (merge with existing)"""
        merged_values = {**(self.values or {}), **new_values}
        return CustomFieldValue(
            id=self.id,
            company_candidate_id=self.company_candidate_id,
            workflow_id=self.workflow_id,
            values=merged_values,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def update_single_value(self, field_key: str, value: Any) -> "CustomFieldValue":
        """Update a single field value"""
        updated_values = {**(self.values or {}), field_key: value}
        return CustomFieldValue(
            id=self.id,
            company_candidate_id=self.company_candidate_id,
            workflow_id=self.workflow_id,
            values=updated_values,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
