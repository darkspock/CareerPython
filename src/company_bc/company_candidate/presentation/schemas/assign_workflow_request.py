from pydantic import BaseModel, Field


class AssignWorkflowRequest(BaseModel):
    """Request schema for assigning a workflow to a company candidate"""
    workflow_id: str = Field(..., description="Workflow ID to assign")
    initial_stage_id: str = Field(..., description="Initial stage ID")
