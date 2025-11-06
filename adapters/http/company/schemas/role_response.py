"""Role Response Schema."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    """Response schema for company role."""

    id: str = Field(..., description="Role unique identifier")
    company_id: str = Field(..., description="Company unique identifier")
    name: str = Field(..., description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    is_active: bool = Field(..., description="Whether the role is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "01HQZJXYZ123456789ABCDEFG",
                "company_id": "01HQZJXYZ123456789ABCDEFG",
                "name": "Senior Backend Engineer",
                "description": "Responsible for backend systems and API development",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        },
        "from_attributes": True
    }
