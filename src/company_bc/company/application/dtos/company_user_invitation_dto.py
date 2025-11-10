from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CompanyUserInvitationDto:
    """Company user invitation data transfer object"""
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

