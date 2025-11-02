import pytest

from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions


class TestCompanyUserPermissionsExpanded:
    """Tests for expanded CompanyUserPermissions"""

    def test_permissions_has_all_new_fields(self):
        """Test that permissions include all new fields"""
        perms = CompanyUserPermissions(
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
        
        assert perms.can_delete_candidates is True
        assert perms.can_view_candidates is True
        assert perms.can_change_settings is True
        assert perms.can_change_phase is True

    def test_default_for_admin_includes_all_permissions(self):
        """Test that admin has all permissions enabled"""
        admin_perms = CompanyUserPermissions.default_for_admin()
        
        assert admin_perms.can_create_candidates is True
        assert admin_perms.can_invite_candidates is True
        assert admin_perms.can_delete_candidates is True
        assert admin_perms.can_view_candidates is True
        assert admin_perms.can_add_comments is True
        assert admin_perms.can_change_settings is True
        assert admin_perms.can_change_phase is True
        assert admin_perms.can_manage_users is True
        assert admin_perms.can_view_analytics is True

    def test_default_for_recruiter_has_limited_permissions(self):
        """Test that recruiter has appropriate permissions"""
        recruiter_perms = CompanyUserPermissions.default_for_recruiter()
        
        assert recruiter_perms.can_create_candidates is True
        assert recruiter_perms.can_delete_candidates is True
        assert recruiter_perms.can_view_candidates is True
        assert recruiter_perms.can_add_comments is True
        assert recruiter_perms.can_change_phase is True
        assert recruiter_perms.can_change_settings is False
        assert recruiter_perms.can_manage_users is False

    def test_default_for_viewer_has_read_only_permissions(self):
        """Test that viewer has read-only permissions"""
        viewer_perms = CompanyUserPermissions.default_for_viewer()
        
        assert viewer_perms.can_create_candidates is False
        assert viewer_perms.can_delete_candidates is False
        assert viewer_perms.can_view_candidates is True
        assert viewer_perms.can_add_comments is False
        assert viewer_perms.can_change_settings is False
        assert viewer_perms.can_change_phase is False
        assert viewer_perms.can_manage_users is False
        assert viewer_perms.can_view_analytics is True

    def test_from_dict_includes_new_permissions(self):
        """Test that from_dict handles all new permissions"""
        perms_dict = {
            "can_create_candidates": True,
            "can_invite_candidates": True,
            "can_delete_candidates": True,
            "can_view_candidates": True,
            "can_add_comments": True,
            "can_change_settings": False,
            "can_change_phase": True,
            "can_manage_users": False,
            "can_view_analytics": True,
        }
        
        perms = CompanyUserPermissions.from_dict(perms_dict)
        
        assert perms.can_delete_candidates is True
        assert perms.can_view_candidates is True
        assert perms.can_change_settings is False
        assert perms.can_change_phase is True

    def test_from_dict_defaults_missing_permissions_to_false(self):
        """Test that from_dict defaults missing permissions to False"""
        perms_dict = {
            "can_create_candidates": True,
        }
        
        perms = CompanyUserPermissions.from_dict(perms_dict)
        
        assert perms.can_create_candidates is True
        assert perms.can_delete_candidates is False
        assert perms.can_view_candidates is False
        assert perms.can_change_settings is False
        assert perms.can_change_phase is False

    def test_to_dict_includes_all_permissions(self):
        """Test that to_dict includes all permissions"""
        perms = CompanyUserPermissions.default_for_admin()
        perms_dict = perms.to_dict()
        
        assert "can_create_candidates" in perms_dict
        assert "can_delete_candidates" in perms_dict
        assert "can_view_candidates" in perms_dict
        assert "can_change_settings" in perms_dict
        assert "can_change_phase" in perms_dict
        assert len(perms_dict) == 9  # All 9 permissions

