from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyUserInvitationResponse(BaseModel):
    """Company user invitation API response schema"""
    id: str
    company_id: str
    email: str
    invited_by_user_id: str
    token: str
    status: str
    expires_at: datetime
    accepted_at: Optional[datetime]
    rejected_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    invitation_link: str  # Full URL with token

    class Config:
        from_attributes = True


class UserInvitationLinkResponse(BaseModel):
    """Response schema for user invitation link (for sharing)"""
    invitation_id: str
    invitation_link: str  # For manual sharing
    expires_at: datetime
    email: str

    class Config:
        from_attributes = True
