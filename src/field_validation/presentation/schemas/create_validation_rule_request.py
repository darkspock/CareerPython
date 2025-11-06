from typing import Optional, Any

from pydantic import BaseModel, Field


class CreateValidationRuleRequest(BaseModel):
    """Request schema for creating a validation rule."""

    custom_field_id: str = Field(..., description="ID of the custom field to validate")
    stage_id: str = Field(..., description="ID of the workflow stage")
    rule_type: str = Field(
        ..., description="Type of validation rule (compare_position_field, range, pattern, custom)"
    )
    comparison_operator: str = Field(
        ...,
        description="Comparison operator (gt, gte, lt, lte, eq, neq, in_range, out_range, contains, not_contains)"
    )
    severity: str = Field(..., description="Severity level (warning, error)")
    validation_message: str = Field(
        ...,
        description="Message shown when validation fails. Supports {field_name}, {candidate_value}, {position_value}"
    )
    position_field_path: Optional[str] = Field(None,
                                               description="Path to position field for comparison (e.g., 'salary.max')")
    comparison_value: Optional[Any] = Field(None, description="Static comparison value (for non-position rules)")
    auto_reject: bool = Field(False, description="Automatically reject application if this rule fails")
    rejection_reason: Optional[str] = Field(None, description="Reason for auto-rejection")
    is_active: bool = Field(True, description="Whether the rule is active")

    class Config:
        json_schema_extra = {
            "example": {
                "custom_field_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H3",
                "stage_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H4",
                "rule_type": "compare_position_field",
                "comparison_operator": "lte",
                "severity": "error",
                "validation_message": "Expected salary ({candidate_value}) exceeds position maximum ({position_value})",
                "position_field_path": "salary.max",
                "auto_reject": True,
                "rejection_reason": "Salary expectation exceeds budget",
                "is_active": True
            }
        }
