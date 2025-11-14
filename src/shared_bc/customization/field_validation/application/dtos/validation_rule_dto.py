from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass(frozen=True)
class ValidationRuleDto:
    """Data transfer object for validation rule."""

    id: str
    custom_field_id: str
    stage_id: str
    rule_type: str
    comparison_operator: str
    position_field_path: Optional[str]
    comparison_value: Optional[Any]
    severity: str
    validation_message: str
    auto_reject: bool
    rejection_reason: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
