"""Phase request and response schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.enums.phase_status_enum import PhaseStatus


class CreatePhaseRequest(BaseModel):
    """Request schema for creating a phase"""
    name: str = Field(..., min_length=1, max_length=100, description="Phase name")
    sort_order: int = Field(..., ge=0, description="Sort order for the phase")
    default_view: DefaultView = Field(..., description="Default view type (KANBAN or LIST)")
    objective: Optional[str] = Field(None, max_length=500, description="Phase objective")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Interview",
                "sort_order": 1,
                "default_view": "KANBAN",
                "objective": "Conduct interviews and assess candidate fit"
            }
        }


class UpdatePhaseRequest(BaseModel):
    """Request schema for updating a phase"""
    name: str = Field(..., min_length=1, max_length=100, description="Phase name")
    sort_order: int = Field(..., ge=0, description="Sort order for the phase")
    default_view: DefaultView = Field(..., description="Default view type (KANBAN or LIST)")
    objective: Optional[str] = Field(None, max_length=500, description="Phase objective")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Interview",
                "sort_order": 1,
                "default_view": "KANBAN",
                "objective": "Conduct interviews and assess candidate fit"
            }
        }


class PhaseResponse(BaseModel):
    """Response schema for phase"""
    id: str
    company_id: str
    name: str
    sort_order: int
    default_view: DefaultView
    status: PhaseStatus
    objective: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01HZXYZ123ABC",
                "company_id": "01HZABC789XYZ",
                "name": "Interview",
                "sort_order": 1,
                "default_view": "KANBAN",
                "status": "ACTIVE",
                "objective": "Conduct interviews and assess candidate fit",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
