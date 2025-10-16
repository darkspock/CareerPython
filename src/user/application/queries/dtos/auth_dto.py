from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class AuthenticatedUserDto:
    """DTO for authenticated user data returned by queries"""
    user_id: str
    email: str
    access_token: str
    token_type: str
    is_active: bool


@dataclass(frozen=True)
class UserExistsDto:
    """DTO for user existence check query"""
    exists: bool
    email: str


@dataclass(frozen=True)
class CurrentUserDto:
    """DTO for current user data from token"""
    user_id: str
    email: str
    is_active: bool
    is_staff: Optional[bool] = None
    roles: Optional[List[str]] = None


@dataclass(frozen=True)
class TokenDto:
    """DTO for token creation queries"""
    access_token: str
    token_type: str
    expires_in: int
