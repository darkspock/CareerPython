from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.domain.enums import CompanyUserRole, CompanyUserStatus
from src.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.user.domain.value_objects.UserId import UserId


@dataclass
class CompanyUser:
    """
    CompanyUser domain entity
    Represents a user who works for a company (recruiter, HR, manager)
    """
    id: CompanyUserId
    company_id: CompanyId
    user_id: UserId
    role: CompanyUserRole
    permissions: CompanyUserPermissions
    status: CompanyUserStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: CompanyUserId,
        company_id: CompanyId,
        user_id: UserId,
        role: CompanyUserRole,
        permissions: Optional[CompanyUserPermissions] = None,
    ) -> "CompanyUser":
        """
        Factory method to create a new company user

        Args:
            id: Company user ID (required, must be provided from outside)
            company_id: Company ID
            user_id: User ID
            role: User role (admin, recruiter, viewer)
            permissions: Custom permissions (optional, uses role defaults)

        Returns:
            CompanyUser: New company user instance

        Raises:
            CompanyValidationError: If data is invalid
        """
        # Validations
        if not company_id:
            raise CompanyValidationError("company_id is required")

        if not user_id:
            raise CompanyValidationError("user_id is required")

        # Default values
        now = datetime.utcnow()

        # Default permissions based on role if not specified
        if permissions is None:
            if role == CompanyUserRole.ADMIN:
                permissions = CompanyUserPermissions.default_for_admin()
            elif role == CompanyUserRole.RECRUITER:
                permissions = CompanyUserPermissions.default_for_recruiter()
            else:  # VIEWER
                permissions = CompanyUserPermissions.default_for_viewer()

        return cls(
            id=id,
            company_id=company_id,
            user_id=user_id,
            role=role,
            permissions=permissions,
            status=CompanyUserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        role: CompanyUserRole,
        permissions: CompanyUserPermissions,
    ) -> "CompanyUser":
        """
        Updates the company user with new values
        Returns a new instance (immutability)

        Args:
            role: New role
            permissions: New permissions

        Returns:
            CompanyUser: New instance with updated data
        """
        return CompanyUser(
            id=self.id,
            company_id=self.company_id,
            user_id=self.user_id,
            role=role,
            permissions=permissions,
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def activate(self) -> "CompanyUser":
        """
        Activates the company user

        Returns:
            CompanyUser: New instance with ACTIVE status
        """
        if self.status == CompanyUserStatus.ACTIVE:
            return self

        return CompanyUser(
            id=self.id,
            company_id=self.company_id,
            user_id=self.user_id,
            role=self.role,
            permissions=self.permissions,
            status=CompanyUserStatus.ACTIVE,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def deactivate(self) -> "CompanyUser":
        """
        Deactivates the company user

        Returns:
            CompanyUser: New instance with INACTIVE status
        """
        if self.status == CompanyUserStatus.INACTIVE:
            return self

        return CompanyUser(
            id=self.id,
            company_id=self.company_id,
            user_id=self.user_id,
            role=self.role,
            permissions=self.permissions,
            status=CompanyUserStatus.INACTIVE,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def is_active(self) -> bool:
        """Checks if user is active"""
        return self.status == CompanyUserStatus.ACTIVE

    def is_admin(self) -> bool:
        """Checks if user is admin"""
        return self.role == CompanyUserRole.ADMIN

    def is_recruiter(self) -> bool:
        """Checks if user is recruiter"""
        return self.role == CompanyUserRole.RECRUITER

    def is_viewer(self) -> bool:
        """Checks if user is viewer"""
        return self.role == CompanyUserRole.VIEWER

    def can_create_candidates(self) -> bool:
        """Checks if user can create candidates"""
        return self.is_active() and self.permissions.can_create_candidates

    def can_invite_candidates(self) -> bool:
        """Checks if user can invite candidates"""
        return self.is_active() and self.permissions.can_invite_candidates

    def can_add_comments(self) -> bool:
        """Checks if user can add comments"""
        return self.is_active() and self.permissions.can_add_comments

    def can_manage_users(self) -> bool:
        """Checks if user can manage users"""
        return self.is_active() and self.permissions.can_manage_users

    def can_view_analytics(self) -> bool:
        """Checks if user can view analytics"""
        return self.is_active() and self.permissions.can_view_analytics
