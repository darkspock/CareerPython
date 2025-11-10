"""Reorder Stages Request Schema."""
from typing import List
from pydantic import BaseModel, Field


class ReorderStagesRequest(BaseModel):
    """Request schema for reordering stages in a workflow."""

    stage_ids_in_order: List[str] = Field(..., description="List of stage IDs in the desired order")

    class Config:
        json_schema_extra = {
            "example": {
                "stage_ids_in_order": [
                    "01HQZX...",
                    "01HQZY...",
                    "01HQZZ..."
                ]
            }
        }
