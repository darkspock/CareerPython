from pydantic import BaseModel, Field


class ConfigureStageFieldRequest(BaseModel):
    """Request schema for configuring field visibility in a stage"""
    stage_id: str = Field(..., description="Stage ID")
    custom_field_id: str = Field(..., description="Custom field ID")
    visibility: str = Field(..., description="Field visibility (VISIBLE, HIDDEN, READ_ONLY, REQUIRED)")

    class Config:
        json_schema_extra = {
            "example": {
                "stage_id": "01HXXXXXXXXXXXXXXXXXXX",
                "custom_field_id": "01HXXXXXXXXXXXXXXXXXXX",
                "visibility": "REQUIRED"
            }
        }
