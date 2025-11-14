from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class CustomFieldDto:
    """DTO for custom field"""
    id: str
    entity_customization_id: str
    field_key: str
    field_name: str
    field_type: str
    field_config: Optional[Dict[str, Any]]
    order_index: int
    created_at: datetime
    updated_at: datetime
