from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AdminPasswordResetRequest(BaseModel):
    """Schema for admin password reset request"""
    generate_temporary: bool = Field(True, description="Generate temporary password vs reset token")
    send_email: bool = Field(True, description="Send reset email to user")
    admin_notes: Optional[str] = Field(None, description="Admin notes about the reset")

    class Config:
        from_attributes = True


class AdminPasswordResetResponse(BaseModel):
    """Schema for admin password reset response"""
    user_id: str
    user_email: str
    reset_method: str  # "temporary_password" or "reset_token"
    temporary_password: Optional[str] = None  # Only if generate_temporary=True
    reset_token: Optional[str] = None  # Only if generate_temporary=False
    reset_token_expires_at: Optional[datetime] = None
    email_sent: bool
    reset_by_admin: str
    reset_at: datetime

    class Config:
        from_attributes = True


class ForcePasswordChangeRequest(BaseModel):
    """Schema for forcing password change"""
    reason: Optional[str] = Field(None, description="Reason for forced password change")
    send_notification: bool = Field(True, description="Send notification email to user")

    class Config:
        from_attributes = True


class ForcePasswordChangeResponse(BaseModel):
    """Schema for force password change response"""
    user_id: str
    user_email: str
    forced_by_admin: str
    reason: Optional[str]
    notification_sent: bool
    forced_at: datetime

    class Config:
        from_attributes = True


class PasswordResetHistoryResponse(BaseModel):
    """Schema for password reset history"""
    user_id: str
    user_email: str
    reset_method: str
    reset_by_admin: str
    reset_at: datetime
    reason: Optional[str]
    email_sent: bool

    class Config:
        from_attributes = True
