"""Schemas for Position Question Config endpoints"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ConfigurePositionQuestionRequest(BaseModel):
    """Request to configure a question for a position."""
    question_id: str = Field(..., description="The application question ID")
    enabled: bool = Field(True, description="Whether the question is enabled for this position")
    is_required_override: Optional[bool] = Field(
        None,
        description="Override the default required state (null = use workflow default)"
    )
    sort_order_override: Optional[int] = Field(
        None,
        description="Override the display order (null = use workflow default)"
    )


class PositionQuestionConfigResponse(BaseModel):
    """Response for a single position question config."""
    id: str
    position_id: str
    question_id: str
    enabled: bool
    is_required_override: Optional[bool]
    sort_order_override: Optional[int]
    created_at: datetime
    updated_at: datetime


class PositionQuestionConfigListResponse(BaseModel):
    """Response for list of position question configs."""
    configs: List[PositionQuestionConfigResponse]
    total: int
