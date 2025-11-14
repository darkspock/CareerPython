from typing import Optional

import ulid
from fastapi import HTTPException, status

from adapters.http.auth.schemas.token import PasswordResetConfirm, PasswordResetResponse, PasswordResetRequest, \
    UserExistsResponse
from adapters.http.auth.schemas.user import UserResponse, UserCreate, UserAutoCreateRequest, UserAutoCreateResponse
from core.exceptions import UserAlreadyExistsException
from src.auth_bc.user.application import GetUserByEmailQuery
from src.auth_bc.user.application import ResetPasswordWithTokenCommand
from src.auth_bc.user.application import UpdateUserLanguageCommand
from src.auth_bc.user.application.commands.create_user_automatically_command import CreateUserAutomaticallyCommand
from src.auth_bc.user.application.commands.create_user_command import CreateUserCommand
from src.auth_bc.user.application.commands.request_password_reset_command import RequestPasswordResetCommand
from src.auth_bc.user.application.queries.check_user_exists_query import CheckUserExistsQuery
from src.auth_bc.user.application.queries.dtos.auth_dto import UserExistsDto, CurrentUserDto
from src.auth_bc.user.application.queries.get_user_language_query import GetUserLanguageQuery
from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects import UserId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class UserController:
    def __init__(
            self,
            query_bus: QueryBus,
            command_bus: CommandBus,
    ):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def create_user(self, user_data: UserCreate) -> UserResponse:
        try:
            new_user_id = ulid.new().str
            hashed_password = PasswordService.hash_password(user_data.password)
            self.command_bus.dispatch(
                CreateUserCommand(UserId.from_string(new_user_id), user_data.email, hashed_password))
            return self.get_user(user_data.email)
        except UserAlreadyExistsException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    def get_user(self, email: str) -> UserResponse:
        user: Optional[UserResponse] = self.query_bus.query(GetUserByEmailQuery(email))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def create_user_automatically(self, request: UserAutoCreateRequest) -> UserAutoCreateResponse:
        """Create user automatically for PDF upload with random password"""
        try:
            # Check if user already exists first
            existing_user_query = CheckUserExistsQuery(email=request.email)
            user_exists_dto: UserExistsDto = self.query_bus.query(existing_user_query)

            if user_exists_dto.exists:
                # User already exists, get user data
                user_query = GetUserByEmailQuery(email=request.email)
                user_dto: Optional[CurrentUserDto] = self.query_bus.query(user_query)

                if not user_dto:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Failed to retrieve existing user")

                return UserAutoCreateResponse(
                    user_id=user_dto.user_id,
                    email=user_dto.email,
                    message="User already exists. Please authenticate with your existing password.",
                    password_reset_sent=False
                )
            else:
                # Create new user automatically
                new_user_id = UserId.from_string(ulid.new().str)
                # Generate password for email sending (not used in response for security)
                User.generate_random_password()

                command = CreateUserAutomaticallyCommand(
                    id=new_user_id,
                    email=request.email
                )
                self.command_bus.dispatch(command)

                # Get the created user
                user_query = GetUserByEmailQuery(email=request.email)
                user_dto = self.query_bus.query(user_query)

                if not user_dto:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Failed to create user automatically")

                return UserAutoCreateResponse(  # type: ignore[unreachable]
                    user_id=user_dto.user_id,
                    email=user_dto.email,
                    message="User created successfully. Password reset email sent.",
                    password_reset_sent=True
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user automatically: {str(e)}"
            )

    async def request_password_reset(self, request: PasswordResetRequest) -> PasswordResetResponse:
        """Request password reset for existing user"""
        try:
            # Execute the request password reset command
            command = RequestPasswordResetCommand(email=request.email)
            self.command_bus.dispatch(command)
            success = True  # If no exception was thrown, it succeeded

            if success:
                return PasswordResetResponse(
                    message="If the email exists, a password reset link has been sent.",
                    success=True
                )
            else:
                return PasswordResetResponse(
                    message="Failed to process password reset request.",
                    success=False
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to request password reset: {str(e)}"
            )

    def reset_password(self, request: PasswordResetConfirm) -> PasswordResetResponse:
        """Reset password using valid reset token"""
        try:
            # Execute the reset password command
            command = ResetPasswordWithTokenCommand(
                reset_token=request.reset_token,
                new_password=request.new_password
            )
            self.command_bus.dispatch(command)
            success = True  # If no exception was thrown, it succeeded

            if success:
                return PasswordResetResponse(
                    message="Password reset successfully.",
                    success=True
                )
            else:
                return PasswordResetResponse(
                    message="Invalid or expired reset token.",
                    success=False
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reset password: {str(e)}"
            )

    def check_user_exists(self, email: str) -> UserExistsResponse:
        """Check if user exists by email"""
        try:
            query = CheckUserExistsQuery(email=email)
            user_exists_dto: UserExistsDto = self.query_bus.query(query)

            return UserExistsResponse(
                exists=user_exists_dto.exists,
                message="User exists" if user_exists_dto.exists else "User does not exist"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to check user existence: {str(e)}"
            )

    def get_user_language(self, user_id: str) -> str:
        """Get user's preferred language"""
        try:
            query = GetUserLanguageQuery(user_id=user_id)
            language: str = self.query_bus.query(query)
            return language
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get user language: {str(e)}"
            )

    def update_user_language(self, user_id: str, language_code: str) -> dict:
        """Update user's preferred language"""
        try:
            command = UpdateUserLanguageCommand(user_id=user_id, language_code=language_code)
            self.command_bus.dispatch(command)

            return {
                "message": "Language preference updated successfully",
                "language_code": language_code
            }
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user language: {str(e)}"
            )
