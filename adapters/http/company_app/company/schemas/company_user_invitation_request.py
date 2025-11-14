from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator


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

    @model_validator(mode='after')
    def validate_mutually_exclusive_fields(self) -> 'AcceptInvitationRequest':
        """Validate that either user_id OR (email, name, password) are provided, but not both"""
        has_user_id = self.user_id is not None
        has_new_user_fields = all([
            self.email is not None,
            self.name is not None,
            self.password is not None
        ])

        if has_user_id and (self.email is not None or self.name is not None or self.password is not None):
            raise ValueError(
                "If user_id is provided, email, name, and password must not be provided"
            )

        if not has_user_id and not has_new_user_fields:
            raise ValueError(
                "Either user_id must be provided, or all of email, name, and password must be provided"
            )

        return self


class AssignRoleRequest(BaseModel):
    """Request schema to assign a role to a company user"""
    role: str
    permissions: Optional[dict[str, bool]] = None
    company_roles: Optional[list[str]] = None  # IDs of CompanyRole to assign

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of the allowed values"""
        allowed_roles = ['admin', 'recruiter', 'viewer']
        if v.lower() not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v.lower()
