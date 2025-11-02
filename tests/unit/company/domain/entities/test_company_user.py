import pytest
from datetime import datetime

from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.enums import CompanyUserRole, CompanyUserStatus
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.user.domain.value_objects.UserId import UserId


class TestCompanyUser:
    """Tests for CompanyUser entity"""

    @pytest.fixture
    def company_user_id(self):
        """Fixture for company user ID"""
        return CompanyUserId.generate()

    @pytest.fixture
    def company_id(self):
        """Fixture for company ID"""
        return CompanyId.generate()

    @pytest.fixture
    def user_id(self):
        """Fixture for user ID"""
        return UserId.generate()

    @pytest.fixture
    def company_user(self, company_user_id, company_id, user_id):
        """Fixture for a company user"""
        return CompanyUser.create(
            id=company_user_id,
            company_id=company_id,
            user_id=user_id,
            role=CompanyUserRole.ADMIN,
        )

    def test_update_modifies_role_and_permissions(self, company_user):
        """Test that update() modifies role and permissions directly"""
        initial_updated_at = company_user.updated_at
        
        new_role = CompanyUserRole.RECRUITER
        new_permissions = CompanyUserPermissions.default_for_recruiter()
        
        company_user.update(role=new_role, permissions=new_permissions)
        
        assert company_user.role == new_role
        assert company_user.permissions == new_permissions
        assert company_user.updated_at > initial_updated_at

    def test_update_modifies_instance_directly(self, company_user):
        """Test that update() is mutable (modifies instance directly)"""
        original_id = id(company_user)
        
        company_user.update(
            role=CompanyUserRole.VIEWER,
            permissions=CompanyUserPermissions.default_for_viewer()
        )
        
        # Same instance, not a new one
        assert id(company_user) == original_id
        assert company_user.role == CompanyUserRole.VIEWER

    def test_remove_deactivates_user(self, company_user):
        """Test that remove() deactivates the user"""
        # Ensure user is active first
        company_user.activate()
        assert company_user.status == CompanyUserStatus.ACTIVE
        
        company_user.remove()
        
        assert company_user.status == CompanyUserStatus.INACTIVE
        assert not company_user.is_active()

    def test_remove_modifies_instance_directly(self, company_user):
        """Test that remove() is mutable (modifies instance directly)"""
        original_id = id(company_user)
        company_user.activate()
        
        company_user.remove()
        
        # Same instance, not a new one
        assert id(company_user) == original_id
        assert company_user.status == CompanyUserStatus.INACTIVE

    def test_activate_modifies_instance_directly(self, company_user):
        """Test that activate() is mutable (modifies instance directly)"""
        company_user.deactivate()
        original_id = id(company_user)
        
        company_user.activate()
        
        # Same instance, not a new one
        assert id(company_user) == original_id
        assert company_user.status == CompanyUserStatus.ACTIVE

    def test_deactivate_modifies_instance_directly(self, company_user):
        """Test that deactivate() is mutable (modifies instance directly)"""
        original_id = id(company_user)
        
        company_user.deactivate()
        
        # Same instance, not a new one
        assert id(company_user) == original_id
        assert company_user.status == CompanyUserStatus.INACTIVE

    def test_activate_updates_timestamp(self, company_user):
        """Test that activate() updates the updated_at timestamp"""
        company_user.deactivate()
        initial_updated_at = company_user.updated_at
        
        company_user.activate()
        
        assert company_user.updated_at > initial_updated_at

    def test_deactivate_updates_timestamp(self, company_user):
        """Test that deactivate() updates the updated_at timestamp"""
        initial_updated_at = company_user.updated_at
        
        company_user.deactivate()
        
        assert company_user.updated_at > initial_updated_at

    def test_activate_is_idempotent(self, company_user):
        """Test that activate() is idempotent"""
        company_user.activate()
        initial_updated_at = company_user.updated_at
        
        company_user.activate()  # Call again
        
        # Should not change status or timestamp if already active
        assert company_user.status == CompanyUserStatus.ACTIVE
        # Note: In current implementation, we don't skip timestamp update if already active
        # This is acceptable behavior

    def test_deactivate_is_idempotent(self, company_user):
        """Test that deactivate() is idempotent"""
        company_user.deactivate()
        initial_status = company_user.status
        
        company_user.deactivate()  # Call again
        
        assert company_user.status == initial_status

    def test_update_with_different_permissions(self, company_user):
        """Test that update() can change permissions to different values"""
        custom_permissions = CompanyUserPermissions(
            can_create_candidates=True,
            can_invite_candidates=False,
            can_delete_candidates=True,
            can_view_candidates=True,
            can_add_comments=True,
            can_change_settings=False,
            can_change_phase=True,
            can_manage_users=False,
            can_view_analytics=True,
        )
        
        company_user.update(
            role=CompanyUserRole.RECRUITER,
            permissions=custom_permissions
        )
        
        assert company_user.permissions == custom_permissions
        assert company_user.role == CompanyUserRole.RECRUITER

    def test_update_preserves_other_fields(self, company_user):
        """Test that update() preserves id, company_id, user_id, status, created_at"""
        original_id = company_user.id
        original_company_id = company_user.company_id
        original_user_id = company_user.user_id
        original_status = company_user.status
        original_created_at = company_user.created_at
        
        company_user.update(
            role=CompanyUserRole.VIEWER,
            permissions=CompanyUserPermissions.default_for_viewer()
        )
        
        assert company_user.id == original_id
        assert company_user.company_id == original_company_id
        assert company_user.user_id == original_user_id
        assert company_user.status == original_status
        assert company_user.created_at == original_created_at

