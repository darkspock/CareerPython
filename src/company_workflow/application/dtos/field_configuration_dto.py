from dataclasses import dataclass
from datetime import datetime


@dataclass
class FieldConfigurationDto:
    """DTO for field configuration"""
    id: str
    stage_id: str
    custom_field_id: str
    visibility: str
    created_at: datetime
    updated_at: datetime
