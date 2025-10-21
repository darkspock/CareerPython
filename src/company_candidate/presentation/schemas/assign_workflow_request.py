from pydantic import BaseModel, Field
from typing import Optional


class AssignWorkflowRequest(BaseModel):
    """Request schema for assigning a workflow to a company candidate"""
    workflow_id: str = Field(..., description="Workflow ID to assign")
    initial_stage_id: Optional[str] = Field(None, description="Initial stage ID (optional, will use workflow's first stage if not provided)")
