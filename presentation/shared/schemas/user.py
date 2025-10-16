from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

from src.staff.domain.enums.staff_enums import RoleEnum


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    is_active: bool
    subscription_tier: str = 'FREE'
    subscription_expires_at: Optional[datetime] = None
    is_staff: bool = False
    roles: List[RoleEnum] = []

    class Config:
        from_attributes = True


class UserAuthDTO(BaseModel):
    id: str
    email: str
    hashed_password: str
    is_active: bool
    subscription_tier: str = 'FREE'
    subscription_expires_at: Optional[datetime] = None
    password_reset_token: Optional[str] = None
    password_reset_expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserAutoCreateRequest(BaseModel):
    email: str  # Using str instead of EmailStr for flexibility


class UserAutoCreateResponse(BaseModel):
    user_id: str
    email: str
    message: str
    password_reset_sent: bool


class UserLanguageRequest(BaseModel):
    language_code: str


class UserLanguageResponse(BaseModel):
    language_code: str


class UserLanguageUpdateResponse(BaseModel):
    message: str
    language_code: str
