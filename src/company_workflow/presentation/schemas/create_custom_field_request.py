from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class CreateCustomFieldRequest(BaseModel):
    """Request schema for creating a custom field"""
    workflow_id: str = Field(..., description="Workflow ID")
    field_key: str = Field(..., description="Unique field identifier (e.g., 'expected_salary')")
    field_name: str = Field(..., description="Display name (e.g., 'Expected Salary')")
    field_type: str = Field(..., description="Field type (TEXT, DROPDOWN, NUMBER, etc.)")
    order_index: int = Field(..., description="Position in field list")
    field_config: Optional[Dict[str, Any]] = Field(default=None, description="Field-specific configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "01HXXXXXXXXXXXXXXXXXXX",
                "field_key": "expected_salary",
                "field_name": "Expected Salary",
                "field_type": "CURRENCY",
                "order_index": 0,
                "field_config": {
                    "currency_code": "USD",
                    "min": 0,
                    "max": 500000
                }
            }
        }
