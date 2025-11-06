from pydantic import BaseModel, Field
from typing import Any


class UpdateSingleFieldValueRequest(BaseModel):
    """Request schema for updating a single custom field value by field_key"""
    field_key: str = Field(..., description="The field_key of the custom field to update")
    value: Any = Field(..., description="The new value for the field")

    class Config:
        json_schema_extra = {
            "example": {
                "field_key": "expected_salary",
                "value": "75000"
            }
        }

