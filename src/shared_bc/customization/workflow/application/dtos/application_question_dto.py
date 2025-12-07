from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)


@dataclass(frozen=True)
class ApplicationQuestionDto:
    """Data Transfer Object for ApplicationQuestion."""
    id: str
    workflow_id: str
    company_id: str
    field_key: str
    label: str
    description: Optional[str]
    field_type: ApplicationQuestionFieldType
    options: Optional[List[str]]
    is_required_default: bool
    validation_rules: Optional[Dict[str, Any]]
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ApplicationQuestionListDto:
    """Data Transfer Object for a list of ApplicationQuestions."""
    questions: List[ApplicationQuestionDto]
    total_count: int
