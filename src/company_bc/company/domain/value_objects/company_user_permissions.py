from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class CompanyUserPermissions:
    """Company user permissions"""
    can_create_candidates: bool
    can_invite_candidates: bool
    can_delete_candidates: bool
    can_view_candidates: bool
    can_add_comments: bool
    can_change_settings: bool
    can_change_phase: bool
    can_manage_users: bool
    can_view_analytics: bool

    @classmethod
    def default_for_admin(cls) -> "CompanyUserPermissions":
        """Default permissions for admin role"""
        return cls(
            can_create_candidates=True,
            can_invite_candidates=True,
            can_delete_candidates=True,
            can_view_candidates=True,
            can_add_comments=True,
            can_change_settings=True,
            can_change_phase=True,
            can_manage_users=True,
            can_view_analytics=True,
        )

    @classmethod
    def default_for_recruiter(cls) -> "CompanyUserPermissions":
        """Default permissions for recruiter role"""
        return cls(
            can_create_candidates=True,
            can_invite_candidates=True,
            can_delete_candidates=True,
            can_view_candidates=True,
            can_add_comments=True,
            can_change_settings=False,
            can_change_phase=True,
            can_manage_users=False,
            can_view_analytics=True,
        )

    @classmethod
    def default_for_viewer(cls) -> "CompanyUserPermissions":
        """Default permissions for viewer role"""
        return cls(
            can_create_candidates=False,
            can_invite_candidates=False,
            can_delete_candidates=False,
            can_view_candidates=True,
            can_add_comments=False,
            can_change_settings=False,
            can_change_phase=False,
            can_manage_users=False,
            can_view_analytics=True,
        )

    @classmethod
    def from_dict(cls, permissions: Dict[str, Any]) -> "CompanyUserPermissions":
        """Create permissions from dictionary"""
        return cls(
            can_create_candidates=permissions.get("can_create_candidates", False),
            can_invite_candidates=permissions.get("can_invite_candidates", False),
            can_delete_candidates=permissions.get("can_delete_candidates", False),
            can_view_candidates=permissions.get("can_view_candidates", False),
            can_add_comments=permissions.get("can_add_comments", False),
            can_change_settings=permissions.get("can_change_settings", False),
            can_change_phase=permissions.get("can_change_phase", False),
            can_manage_users=permissions.get("can_manage_users", False),
            can_view_analytics=permissions.get("can_view_analytics", False),
        )

    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary"""
        return {
            "can_create_candidates": self.can_create_candidates,
            "can_invite_candidates": self.can_invite_candidates,
            "can_delete_candidates": self.can_delete_candidates,
            "can_view_candidates": self.can_view_candidates,
            "can_add_comments": self.can_add_comments,
            "can_change_settings": self.can_change_settings,
            "can_change_phase": self.can_change_phase,
            "can_manage_users": self.can_manage_users,
            "can_view_analytics": self.can_view_analytics,
        }
