from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class CompanyResponse(BaseModel):
    """Company API response schema"""
    id: str
    name: str
    domain: str
    slug: Optional[str]
    logo_url: Optional[str]
    settings: Dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
