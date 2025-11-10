from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from src.auth_bc.user.application.queries.dtos.auth_dto import AuthenticatedUserDto


class LoginResponse(BaseModel):
    """Response schema for login endpoint"""
    access_token: str
    token_type: str
    user_id: str
    email: str
    is_active: bool
    subscription_tier: str = 'FREE'
    subscription_expires_at: Optional[datetime] = None

    @classmethod
    def from_dto(cls, dto: AuthenticatedUserDto) -> 'LoginResponse':
        """Convert DTO to Response schema"""
        return cls(
            access_token=dto.access_token,
            token_type=dto.token_type,
            user_id=dto.user_id,
            email=dto.email,
            is_active=dto.is_active,
        )
