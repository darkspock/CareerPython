"""Update Role Request Schema."""
from typing import Optional

from pydantic import BaseModel, Field


class UpdateRoleRequest(BaseModel):
    """Request schema for updating a company role."""

    name: str = Field(..., min_length=1, max_length=100, description="Role name")
    description: Optional[str] = Field(None, description="Role description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Senior Backend Engineer",
                "description": "Responsible for backend systems and API development"
            }
        }
    }
