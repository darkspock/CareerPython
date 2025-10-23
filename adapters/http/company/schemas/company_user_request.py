from typing import Optional, Dict

from pydantic import BaseModel, field_validator


class AddCompanyUserRequest(BaseModel):
    """Request schema to add a user to a company"""
    user_id: str
    role: str
    permissions: Optional[Dict[str, bool]] = None

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of the allowed values"""
        allowed_roles = ['admin', 'recruiter', 'viewer']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UpdateCompanyUserRequest(BaseModel):
    """Request schema to update a company user"""
    role: str
    permissions: Dict[str, bool]

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of the allowed values"""
        allowed_roles = ['admin', 'recruiter', 'viewer']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v

    @field_validator('permissions')
    @classmethod
    def validate_permissions(cls, v: Dict[str, bool]) -> Dict[str, bool]:
        """Validate permissions structure"""
        required_keys = [
            'can_create_candidates',
            'can_invite_candidates',
            'can_add_comments',
            'can_manage_users',
            'can_view_analytics',
        ]
        for key in required_keys:
            if key not in v:
                raise ValueError(f'Missing required permission: {key}')
        return v
