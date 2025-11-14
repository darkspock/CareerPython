from dataclasses import dataclass
from typing import Optional

from src.auth_bc.user.application.queries.dtos.auth_dto import AuthenticatedUserDto
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.services.token_service import TokenService
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class AuthenticateUserQuery(Query):
    """Query to authenticate a user with email and password"""
    email: str
    password: str


class AuthenticateUserQueryHandler(QueryHandler[AuthenticateUserQuery, Optional[AuthenticatedUserDto]]):
    """Handler for user authentication query"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, query: AuthenticateUserQuery) -> Optional[AuthenticatedUserDto]:
        """
        Handle user authentication

        Returns:
            AuthenticatedUserDto if authentication successful, None if failed
        """
        # Get user auth data
        user = self.user_repository.get_user_auth_data_by_email(query.email)
        if not user:
            return None

        # Verify password
        if not PasswordService.verify_password(query.password, user.hashed_password):
            return None

        # Create access token
        access_token = TokenService.create_access_token(data={"sub": user.email})

        return AuthenticatedUserDto(
            user_id=user.id.value,
            email=user.email,
            access_token=access_token,
            token_type="bearer",
            is_active=user.is_active
        )
