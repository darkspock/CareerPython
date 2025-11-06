from typing import List, Optional

from pydantic import BaseModel, Field


class ValidationIssueResponse(BaseModel):
    """Response schema for a validation issue."""

    field_key: str = Field(..., description="Custom field ID")
    field_name: str = Field(..., description="Custom field display name")
    message: str = Field(..., description="Validation message")
    severity: str = Field(..., description="Severity (error or warning)")
    rule_id: str = Field(..., description="Validation rule ID")
    should_auto_reject: bool = Field(..., description="Whether this triggers auto-rejection")
    rejection_reason: Optional[str] = Field(None, description="Auto-rejection reason")


class ValidationResultResponse(BaseModel):
    """Response schema for validation result."""

    is_valid: bool = Field(..., description="Whether validation passed (no errors)")
    has_errors: bool = Field(..., description="Whether there are any errors")
    has_warnings: bool = Field(..., description="Whether there are any warnings")
    errors: List[ValidationIssueResponse] = Field(..., description="List of validation errors")
    warnings: List[ValidationIssueResponse] = Field(..., description="List of validation warnings")
    should_auto_reject: bool = Field(..., description="Whether application should be auto-rejected")
    auto_reject_reason: Optional[str] = Field(None, description="Reason for auto-rejection")

    class Config:
        json_schema_extra = {
            "example": {
                "is_valid": False,
                "has_errors": True,
                "has_warnings": False,
                "errors": [
                    {
                        "field_key": "01H2X3Y4Z5A6B7C8D9E0F1G2H3",
                        "field_name": "Expected Salary",
                        "message": "Expected salary (85000) exceeds position maximum (80000)",
                        "severity": "error",
                        "rule_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H5",
                        "should_auto_reject": True,
                        "rejection_reason": "Salary expectation exceeds budget"
                    }
                ],
                "warnings": [],
                "should_auto_reject": True,
                "auto_reject_reason": "Salary expectation exceeds budget"
            }
        }
