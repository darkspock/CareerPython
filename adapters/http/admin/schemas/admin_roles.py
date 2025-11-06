from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.staff.domain.enums.staff_enums import RoleEnum, StaffStatusEnum


class AssignRoleRequest(BaseModel):
    """Schema for assigning roles to user"""
    roles: List[RoleEnum] = Field(..., description="Roles to assign to user")
    status: StaffStatusEnum = Field(StaffStatusEnum.ACTIVE, description="Staff status")
    admin_notes: Optional[str] = Field(None, description="Admin notes about role assignment")

    class Config:
        from_attributes = True


class AssignRoleResponse(BaseModel):
    """Schema for role assignment response"""
    user_id: str
    user_email: str
    previous_roles: List[RoleEnum]
    new_roles: List[RoleEnum]
    staff_status: StaffStatusEnum
    was_new_staff: bool
    assigned_by_admin: str
    assigned_at: datetime

    class Config:
        from_attributes = True


class RemoveRoleRequest(BaseModel):
    """Schema for removing roles from user"""
    roles_to_remove: Optional[List[RoleEnum]] = Field(None, description="Specific roles to remove (None = all)")
    deactivate_staff: bool = Field(False, description="Deactivate instead of removing roles")
    reason: Optional[str] = Field(None, description="Reason for role removal")
    send_notification: bool = Field(True, description="Send notification email")

    class Config:
        from_attributes = True


class RemoveRoleResponse(BaseModel):
    """Schema for role removal response"""
    user_id: str
    user_email: str
    previous_roles: List[RoleEnum]
    remaining_roles: List[RoleEnum]
    staff_deactivated: bool
    completely_removed: bool
    removed_by_admin: str
    removed_at: datetime
    reason: Optional[str]

    class Config:
        from_attributes = True


class UserRoleInfoResponse(BaseModel):
    """Schema for user role information"""
    user_id: str
    user_email: str
    is_staff: bool
    staff_id: Optional[str]
    roles: List[RoleEnum]
    staff_status: Optional[StaffStatusEnum]
    can_access_admin: bool

    class Config:
        from_attributes = True


class AvailableRolesResponse(BaseModel):
    """Schema for available roles information"""
    roles: List[dict]  # [{"value": "admin", "label": "Administrator", "description": "..."}]
    statuses: List[dict]  # [{"value": "active", "label": "Active", "description": "..."}]

    class Config:
        from_attributes = True


class RoleHistoryResponse(BaseModel):
    """Schema for role change history"""
    user_id: str
    user_email: str
    action: str  # "assigned", "removed", "updated", "deactivated"
    previous_roles: List[RoleEnum]
    new_roles: List[RoleEnum]
    performed_by_admin: str
    performed_at: datetime
    reason: Optional[str]

    class Config:
        from_attributes = True
