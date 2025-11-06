from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class CustomFieldResponse(BaseModel):
    """Custom field API response schema"""
    id: str
    workflow_id: str
    field_key: str
    field_name: str
    field_type: str
    field_config: Optional[Dict[str, Any]]
    order_index: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
