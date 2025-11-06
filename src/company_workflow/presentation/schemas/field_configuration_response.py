from datetime import datetime

from pydantic import BaseModel


class FieldConfigurationResponse(BaseModel):
    """Field configuration API response schema"""
    id: str
    stage_id: str
    custom_field_id: str
    visibility: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
