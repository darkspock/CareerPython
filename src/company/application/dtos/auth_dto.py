"""Authentication DTOs for Company."""
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedCompanyUserDto:
    """DTO for authenticated company user data."""
    user_id: str
    company_id: str
    email: str
    role: str
    access_token: str
    token_type: str
    is_active: bool
