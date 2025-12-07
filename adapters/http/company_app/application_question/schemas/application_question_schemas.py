from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ApplicationQuestionResponse(BaseModel):
    """Response schema for application question."""
    id: str
    workflow_id: str
    company_id: str
    field_key: str
    label: str
    description: Optional[str] = None
    field_type: str
    options: Optional[List[str]] = None
    is_required_default: bool
    validation_rules: Optional[Dict[str, Any]] = None
    sort_order: int
    is_active: bool
    created_at: str
    updated_at: str


class ApplicationQuestionListResponse(BaseModel):
    """Response schema for application question list."""
    questions: List[ApplicationQuestionResponse]
    total_count: int


class CreateApplicationQuestionRequest(BaseModel):
    """Request schema for creating an application question."""
    field_key: str
    label: str
    field_type: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required_default: bool = False
    validation_rules: Optional[Dict[str, Any]] = None
    sort_order: int = 0


class UpdateApplicationQuestionRequest(BaseModel):
    """Request schema for updating an application question."""
    label: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    is_required_default: Optional[bool] = None
    validation_rules: Optional[Dict[str, Any]] = None
    sort_order: Optional[int] = None
