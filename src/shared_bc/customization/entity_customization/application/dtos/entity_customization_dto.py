from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.shared_bc.customization.entity_customization.application.dtos.custom_field_dto import CustomFieldDto


@dataclass
class EntityCustomizationDto:
    """DTO for entity customization"""
    id: str
    entity_type: str
    entity_id: str
    fields: List[CustomFieldDto]
    validation: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

