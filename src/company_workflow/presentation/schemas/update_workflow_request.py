from pydantic import BaseModel, Field


class UpdateWorkflowRequest(BaseModel):
    """Request schema for updating a workflow"""
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
