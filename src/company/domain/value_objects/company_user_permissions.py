from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class CompanyUserPermissions:
    """Company user permissions"""
    can_create_candidates: bool
    can_invite_candidates: bool
    can_add_comments: bool
    can_manage_users: bool
    can_view_analytics: bool

    @classmethod
    def default_for_admin(cls) -> "CompanyUserPermissions":
        """Default permissions for admin role"""
        return cls(
            can_create_candidates=True,
            can_invite_candidates=True,
            can_add_comments=True,
            can_manage_users=True,
            can_view_analytics=True,
        )

    @classmethod
    def default_for_recruiter(cls) -> "CompanyUserPermissions":
        """Default permissions for recruiter role"""
        return cls(
            can_create_candidates=True,
            can_invite_candidates=True,
            can_add_comments=True,
            can_manage_users=False,
            can_view_analytics=True,
        )

    @classmethod
    def default_for_viewer(cls) -> "CompanyUserPermissions":
        """Default permissions for viewer role"""
        return cls(
            can_create_candidates=False,
            can_invite_candidates=False,
            can_add_comments=False,
            can_manage_users=False,
            can_view_analytics=True,
        )

    @classmethod
    def from_dict(cls, permissions: Dict[str, Any]) -> "CompanyUserPermissions":
        """Create permissions from dictionary"""
        return cls(
            can_create_candidates=permissions.get("can_create_candidates", False),
            can_invite_candidates=permissions.get("can_invite_candidates", False),
            can_add_comments=permissions.get("can_add_comments", False),
            can_manage_users=permissions.get("can_manage_users", False),
            can_view_analytics=permissions.get("can_view_analytics", False),
        )

    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary"""
        return {
            "can_create_candidates": self.can_create_candidates,
            "can_invite_candidates": self.can_invite_candidates,
            "can_add_comments": self.can_add_comments,
            "can_manage_users": self.can_manage_users,
            "can_view_analytics": self.can_view_analytics,
        }
