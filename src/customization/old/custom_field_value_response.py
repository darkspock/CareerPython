from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any


class CustomFieldValueResponse(BaseModel):
    """Custom field value API response schema"""
    id: str
    company_candidate_id: str
    workflow_id: str
    values: Dict[str, Any]  # JSON with all field values, keyed by field_key
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
