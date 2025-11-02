"""
Integration tests for CompanyUserRepository
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.enums import CompanyUserRole, CompanyUserStatus
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.domain.value_objects.company_user_permissions import (
    CompanyUserPermissions
)
from src.company.infrastructure.repositories.company_user_repository import (
    CompanyUserRepository
)
from src.company.infrastructure.models.company_user_model import CompanyUserModel
from src.user.domain.value_objects.UserId import UserId
from core.database import SQLAlchemyDatabase
from core.base import Base


class TestCompanyUserRepository:
    """Tests for CompanyUserRepository"""

    @pytest.fixture
    def database(self):
        """Create in-memory database for tests"""
        engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(engine)
        db = SQLAlchemyDatabase()
        db._engine = engine  # Use in-memory engine
        return db

    @pytest.fixture
    def repository(self, database):
        """Create repository for tests"""
        return CompanyUserRepository(database)

    @pytest.fixture
    def company_id(self):
        """Fixture for company ID"""
        return CompanyId.generate()

    @pytest.fixture
    def user_id(self):
        """Fixture for user ID"""
        return UserId.generate()

    @pytest.fixture
    def company_user_id(self):
        """Fixture for company user ID"""
        return CompanyUserId.generate()

    @pytest.fixture
    def test_company_user(self, company_user_id, company_id, user_id):
        """Create test company user"""
        return CompanyUser.create(
            id=company_user_id,
            company_id=company_id,
            user_id=user_id,
            role=CompanyUserRole.RECRUITER
        )

    def test_count_admins_by_company_zero_admins(self, repository, company_id):
        """Test counting admins when there are no admins"""
        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 0

    def test_count_admins_by_company_one_admin(self, repository, company_id):
        """Test counting admins when there is one admin"""
        # Arrange - Create one admin user
        admin_user_id = CompanyUserId.generate()
        admin_user = CompanyUser.create(
            id=admin_user_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin_user)

        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 1

    def test_count_admins_by_company_multiple_admins(self, repository, company_id):
        """Test counting admins when there are multiple admins"""
        # Arrange - Create multiple admin users
        admin1_id = CompanyUserId.generate()
        admin1 = CompanyUser.create(
            id=admin1_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin1)

        admin2_id = CompanyUserId.generate()
        admin2 = CompanyUser.create(
            id=admin2_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin2)

        admin3_id = CompanyUserId.generate()
        admin3 = CompanyUser.create(
            id=admin3_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin3)

        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 3

    def test_count_admins_by_company_excludes_non_admins(self, repository, company_id):
        """Test that counting admins excludes non-admin users"""
        # Arrange - Create admin and non-admin users
        admin_id = CompanyUserId.generate()
        admin = CompanyUser.create(
            id=admin_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin)

        recruiter_id = CompanyUserId.generate()
        recruiter = CompanyUser.create(
            id=recruiter_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.RECRUITER
        )
        repository.save(recruiter)

        viewer_id = CompanyUserId.generate()
        viewer = CompanyUser.create(
            id=viewer_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.VIEWER
        )
        repository.save(viewer)

        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 1  # Only the admin

    def test_count_admins_by_company_excludes_inactive_admins(
        self, repository, company_id
    ):
        """Test that counting admins excludes inactive admin users"""
        # Arrange - Create active and inactive admins
        active_admin_id = CompanyUserId.generate()
        active_admin = CompanyUser.create(
            id=active_admin_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(active_admin)

        # Create inactive admin
        inactive_admin_id = CompanyUserId.generate()
        inactive_admin = CompanyUser.create(
            id=inactive_admin_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        inactive_admin.deactivate()
        repository.save(inactive_admin)

        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 1  # Only the active admin

    def test_count_admins_by_company_different_companies(self, repository):
        """Test that counting admins is scoped to the specific company"""
        # Arrange - Create admins for different companies
        company1_id = CompanyId.generate()
        admin1_id = CompanyUserId.generate()
        admin1 = CompanyUser.create(
            id=admin1_id,
            company_id=company1_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin1)

        company2_id = CompanyId.generate()
        admin2_id = CompanyUserId.generate()
        admin2 = CompanyUser.create(
            id=admin2_id,
            company_id=company2_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin2)

        # Act
        count1 = repository.count_admins_by_company(company1_id)
        count2 = repository.count_admins_by_company(company2_id)

        # Assert
        assert count1 == 1
        assert count2 == 1

    def test_count_admins_by_company_mixed_roles_and_statuses(
        self, repository, company_id
    ):
        """Test counting admins with mixed roles and statuses"""
        # Arrange - Create various combinations
        # Active admin
        admin1_id = CompanyUserId.generate()
        admin1 = CompanyUser.create(
            id=admin1_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        repository.save(admin1)

        # Inactive admin (should not count)
        admin2_id = CompanyUserId.generate()
        admin2 = CompanyUser.create(
            id=admin2_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.ADMIN
        )
        admin2.deactivate()
        repository.save(admin2)

        # Active recruiter (should not count)
        recruiter_id = CompanyUserId.generate()
        recruiter = CompanyUser.create(
            id=recruiter_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.RECRUITER
        )
        repository.save(recruiter)

        # Active viewer (should not count)
        viewer_id = CompanyUserId.generate()
        viewer = CompanyUser.create(
            id=viewer_id,
            company_id=company_id,
            user_id=UserId.generate(),
            role=CompanyUserRole.VIEWER
        )
        repository.save(viewer)

        # Act
        count = repository.count_admins_by_company(company_id)

        # Assert
        assert count == 1  # Only the active admin

