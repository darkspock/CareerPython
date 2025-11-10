from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ValidationRuleResponse(BaseModel):
    """Response schema for validation rule."""

    id: str = Field(..., description="Validation rule ID")
    custom_field_id: str = Field(..., description="Custom field ID")
    stage_id: str = Field(..., description="Workflow stage ID")
    rule_type: str = Field(..., description="Type of validation rule")
    comparison_operator: str = Field(..., description="Comparison operator")
    position_field_path: Optional[str] = Field(None, description="Path to position field")
    comparison_value: Optional[Any] = Field(None, description="Static comparison value")
    severity: str = Field(..., description="Severity level")
    validation_message: str = Field(..., description="Validation message")
    auto_reject: bool = Field(..., description="Whether to auto-reject on failure")
    rejection_reason: Optional[str] = Field(None, description="Auto-rejection reason")
    is_active: bool = Field(..., description="Whether the rule is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01H2X3Y4Z5A6B7C8D9E0F1G2H5",
                "custom_field_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H3",
                "stage_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H4",
                "rule_type": "compare_position_field",
                "comparison_operator": "lte",
                "position_field_path": "salary.max",
                "comparison_value": None,
                "severity": "error",
                "validation_message": "Expected salary exceeds position maximum",
                "auto_reject": True,
                "rejection_reason": "Salary expectation exceeds budget",
                "is_active": True,
                "created_at": "2025-10-26T10:00:00Z",
                "updated_at": "2025-10-26T10:00:00Z"
            }
        }
