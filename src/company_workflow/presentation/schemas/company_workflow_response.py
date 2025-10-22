from pydantic import BaseModel
from datetime import datetime


class CompanyWorkflowResponse(BaseModel):
    """Company workflow API response schema"""
    id: str
    company_id: str
    name: str
    description: str
    status: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
