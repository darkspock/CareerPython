from typing import Optional
from pydantic import BaseModel, Field


class UpdateWorkflowRequest(BaseModel):
    """Request schema for updating a workflow"""
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    display: Optional[str] = Field(None, description="Display type: 'kanban' or 'list'")
    phase_id: Optional[str] = Field(None, description="Phase ID (Phase 12)")
