from typing import Optional

from pydantic import BaseModel, Field


class CreateWorkflowRequest(BaseModel):
    """Request schema for creating a workflow"""
    company_id: str = Field(..., description="Company ID")
    name: str = Field(..., description="Workflow name")
    description: str = Field(default="", description="Workflow description")
    phase_id: Optional[str] = Field(None, description="Phase ID (Phase 12)")
    is_default: bool = Field(default=False, description="Is this the default workflow")
