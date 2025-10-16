"""
Integration tests for user registration functionality
Tests both normal registration and automatic registration using Clean Architecture commands/queries
"""
import uuid

import pytest

from core.container import Container
from src.user.application.commands.create_user_automatically_command import CreateUserAutomaticallyCommand
from src.user.application.commands.create_user_command import CreateUserCommand
from src.user.application.queries.authenticate_user_query import AuthenticateUserQuery
from src.user.application.queries.check_user_exists_query import CheckUserExistsQuery
from src.user.domain.value_objects.UserId import UserId
from tests.fixtures.auth import TestAuthMixin


class TestAuthRegistrationIntegration(TestAuthMixin):
    """Integration tests for user registration using direct handlers"""

    @pytest.fixture(autouse=True)
    def setup_container(self):
        """Setup dependency injection container for tests"""
        self.container = Container()
        self.container.wire(modules=[__name__])

        # Get handlers directly from container
        self.create_user_handler = self.container.create_user_command_handler()
        self.create_user_auto_handler = self.container.create_user_automatically_command_handler()
        self.authenticate_user_handler = self.container.authenticate_user_query_handler()
        self.check_user_exists_handler = self.container.check_user_exists_query_handler()

        yield
        self.container.unwire()

    def test_normal_user_registration_flow(self):
        """Test complete flow of normal user registration"""
        # Arrange
        test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "securepassword123"

        # Act 1: Check user doesn't exist initially
        check_query = CheckUserExistsQuery(email=test_email)
        exists_result = self.check_user_exists_handler.handle(check_query)

        # Assert 1: User should not exist
        assert not exists_result.exists
        assert exists_result.email == test_email

        # Act 2: Create user using command
        create_command = CreateUserCommand(
            email=test_email,
            password=test_password,
            is_active=True
        )
        self.create_user_handler.execute(create_command)

        # Assert 2: User should now exist
        check_query_after = CheckUserExistsQuery(email=test_email)
        exists_result_after = self.check_user_exists_handler.handle(check_query_after)
        assert exists_result_after.exists

        # Act 3: Authenticate the created user
        auth_query = AuthenticateUserQuery(
            email=test_email,
            password=test_password
        )
        auth_result = self.authenticate_user_handler.handle(auth_query)

        # Assert 3: Authentication should succeed
        assert auth_result is not None
        assert auth_result.email == test_email
        assert auth_result.is_active is True
        assert auth_result.access_token is not None
        assert auth_result.token_type == "bearer"

    def test_normal_user_registration_with_wrong_password(self):
        """Test that authentication fails with wrong password"""
        # Arrange
        test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        correct_password = "securepassword123"
        wrong_password = "wrongpassword"

        # Act 1: Create user
        create_command = CreateUserCommand(
            email=test_email,
            password=correct_password,
            is_active=True
        )
        self.create_user_handler.execute(create_command)

        # Act 2: Try to authenticate with wrong password
        auth_query = AuthenticateUserQuery(
            email=test_email,
            password=wrong_password
        )
        auth_result = self.authenticate_user_handler.handle(auth_query)

        # Assert: Authentication should fail
        assert auth_result is None

    @pytest.mark.asyncio
    async def test_automatic_user_registration_flow(self):
        """Test complete flow of automatic user registration"""
        # Arrange
        test_email = f"auto_user_{uuid.uuid4().hex[:8]}@example.com"

        # Act 1: Check user doesn't exist initially
        check_query = CheckUserExistsQuery(email=test_email)
        exists_result = self.check_user_exists_handler.handle(check_query)

        # Assert 1: User should not exist
        assert not exists_result.exists

        # Act 2: Create user automatically using command
        create_auto_command = CreateUserAutomaticallyCommand(id=UserId.generate(), email=test_email)
        await self.create_user_auto_handler.execute(create_auto_command)

        # Assert 2: User should now exist
        check_query_after = CheckUserExistsQuery(email=test_email)
        exists_result_after = self.check_user_exists_handler.handle(check_query_after)
        assert exists_result_after.exists

    @pytest.mark.asyncio
    async def test_automatic_user_registration_existing_user(self):
        """Test automatic registration when user already exists"""
        # Arrange
        test_email = f"existing_user_{uuid.uuid4().hex[:8]}@example.com"

        # Act 1: Create user normally first
        create_command = CreateUserCommand(
            email=test_email,
            password="originalpassword",
            is_active=True
        )
        self.create_user_handler.execute(create_command)

        # Act 2: Try automatic creation for existing user
        create_auto_command = CreateUserAutomaticallyCommand(id=UserId.generate(), email=test_email)
        await self.create_user_auto_handler.execute(create_auto_command)

        # Assert: User should still exist (no exception should be thrown)
        check_query = CheckUserExistsQuery(email=test_email)
        exists_result = self.check_user_exists_handler.handle(check_query)
        assert exists_result.exists

    def test_registration_with_inactive_user(self):
        """Test registration and authentication with inactive user"""
        # Arrange
        test_email = f"inactive_user_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "password123"

        # Act 1: Create inactive user
        create_command = CreateUserCommand(
            email=test_email,
            password=test_password,
            is_active=False
        )
        self.create_user_handler.execute(create_command)

        # Act 2: Try to authenticate
        auth_query = AuthenticateUserQuery(
            email=test_email,
            password=test_password
        )
        auth_result = self.authenticate_user_handler.handle(auth_query)

        # Assert: Authentication should succeed but user should be marked as inactive
        assert auth_result is not None
        assert auth_result.email == test_email
        assert auth_result.is_active is False

    def test_duplicate_user_registration(self):
        """Test that duplicate user registration is handled properly"""
        # Arrange
        test_email = f"duplicate_user_{uuid.uuid4().hex[:8]}@example.com"
        test_password = "password123"

        # Act 1: Create user first time
        create_command = CreateUserCommand(
            email=test_email,
            password=test_password,
            is_active=True
        )
        self.create_user_handler.execute(create_command)

        # Act 2: Try to create same user again
        create_command_duplicate = CreateUserCommand(
            email=test_email,
            password="differentpassword",
            is_active=True
        )

        # Assert: Should raise an exception for duplicate user
        with pytest.raises(Exception):
            self.create_user_handler.handle(create_command_duplicate)
