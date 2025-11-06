from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class CustomFieldValueDto:
    """DTO for custom field value"""
    id: str
    company_candidate_id: str
    workflow_id: str
    values: Dict[str, Any]  # JSON with all field values, keyed by field_key
    created_at: datetime
    updated_at: datetime
