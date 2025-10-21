from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class CompanyUserResponse(BaseModel):
    """Company user API response schema"""
    id: str
    company_id: str
    user_id: str
    role: str
    permissions: Dict[str, bool]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
