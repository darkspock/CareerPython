from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class InviteCompanyUserRequest(BaseModel):
    """Request schema to invite a user to a company"""
    email: EmailStr
    role: Optional[str] = None

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        """Validate role is one of the allowed values"""
        if v is None:
            return None
        allowed_roles = ['admin', 'recruiter', 'viewer']
        if v.lower() not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v.lower()


class AcceptInvitationRequest(BaseModel):
    """Request schema to accept a user invitation"""
    token: str
    email: Optional[str] = None  # Required if user is new
    name: Optional[str] = None  # Required if user is new
    password: Optional[str] = None  # Required if user is new
    user_id: Optional[str] = None  # If user already exists

    @field_validator('email', 'name', 'password')
    @classmethod
    def validate_new_user_fields(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that if user_id is not provided, all new user fields are provided"""
        # This will be validated at handler level for better error messages
        return v


class AssignRoleRequest(BaseModel):
    """Request schema to assign a role to a company user"""
    role: str
    permissions: Optional[dict[str, bool]] = None

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of the allowed values"""
        allowed_roles = ['admin', 'recruiter', 'viewer']
        if v.lower() not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v.lower()

