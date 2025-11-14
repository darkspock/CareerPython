"""Response schemas for company registration"""
from typing import Optional

from pydantic import BaseModel


class CompanyRegistrationResponse(BaseModel):
    """Response schema for company registration"""
    company_id: str
    user_id: str
    message: str
    redirect_url: Optional[str] = None


class LinkUserResponse(BaseModel):
    """Response schema for linking user to company"""
    company_id: str
    user_id: str
    message: str
    redirect_url: Optional[str] = None
