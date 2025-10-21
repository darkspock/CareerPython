from pydantic import BaseModel, Field


class ChangeStageRequest(BaseModel):
    """Request schema for changing the workflow stage of a company candidate"""
    new_stage_id: str = Field(..., description="New stage ID")
