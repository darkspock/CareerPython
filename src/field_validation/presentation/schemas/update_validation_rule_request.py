from typing import Optional, Any

from pydantic import BaseModel, Field


class UpdateValidationRuleRequest(BaseModel):
    """Request schema for updating a validation rule."""

    comparison_operator: str = Field(..., description="Comparison operator")
    severity: str = Field(..., description="Severity level (warning, error)")
    validation_message: str = Field(..., description="Message shown when validation fails")
    position_field_path: Optional[str] = Field(None, description="Path to position field for comparison")
    comparison_value: Optional[Any] = Field(None, description="Static comparison value")
    auto_reject: bool = Field(False, description="Automatically reject application if this rule fails")
    rejection_reason: Optional[str] = Field(None, description="Reason for auto-rejection")
    is_active: bool = Field(True, description="Whether the rule is active")

    class Config:
        json_schema_extra = {
            "example": {
                "comparison_operator": "lte",
                "severity": "warning",
                "validation_message": "Expected salary ({candidate_value}) is close to position maximum ({position_value})",
                "position_field_path": "salary.max",
                "auto_reject": False,
                "is_active": True
            }
        }
