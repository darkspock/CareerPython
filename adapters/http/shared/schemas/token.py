from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    candidate_id: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    email: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    reset_token: str
    new_password: str


class PasswordResetResponse(BaseModel):
    message: str
    success: bool


class UserExistsResponse(BaseModel):
    exists: bool
    message: str
