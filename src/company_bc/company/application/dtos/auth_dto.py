"""Authentication DTOs for Company."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthenticatedCompanyUserDto:
    """DTO for authenticated company user data."""
    user_id: str
    company_id: str
    company_slug: Optional[str]
    email: str
    role: str
    access_token: str
    token_type: str
    is_active: bool
