from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class UpdateCustomFieldValueRequest(BaseModel):
    """Request schema for updating a custom field value"""
    values: Optional[Dict[str, Any]] = Field(default=None,
                                             description="Dictionary of field_key -> value to merge with existing")
    # For backward compatibility with old frontend
    field_value: Optional[Any] = Field(default=None, description="Single field value (deprecated, use values instead)")

    class Config:
        json_schema_extra = {
            "example": {
                "values": {
                    "salary": "75000",
                    "availability": "2 weeks"
                }
            }
        }
