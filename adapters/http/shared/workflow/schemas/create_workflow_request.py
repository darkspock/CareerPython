from typing import Optional
from pydantic import BaseModel, Field


class CreateWorkflowRequest(BaseModel):
    """Request schema for creating a workflow"""
    company_id: str = Field(..., description="Company ID")
    workflow_type: str = Field(..., description="Workflow type: 'PO' (Job Position Opening), 'CA' (Candidate Application), 'CO' (Candidate Onboarding)")
    name: str = Field(..., description="Workflow name")
    description: str = Field(default="", description="Workflow description")
    display: str = Field(default="kanban", description="Display type: 'kanban' or 'list'")
    phase_id: Optional[str] = Field(None, description="Phase ID (Phase 12)")
    is_default: bool = Field(default=False, description="Is this the default workflow")
