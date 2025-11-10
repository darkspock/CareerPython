from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.token_service import TokenService


@dataclass(frozen=True)
class GetCurrentUserFromTokenQuery(Query):
    """Query to get current user from JWT token"""
    token: str


class GetCurrentUserFromTokenQueryHandler(QueryHandler[GetCurrentUserFromTokenQuery, CurrentUserDto]):
    """Handler for getting current user from token"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, query: GetCurrentUserFromTokenQuery) -> CurrentUserDto:
        """
        Handle getting current user from token

        Returns:
            CurrentUserDto with user data

        Raises:
            Exception: If token is invalid or user not found
        """
        # Decode token
        payload = TokenService.decode_access_token(query.token)
        if not payload:
            raise Exception("Invalid token")

        email = payload.get("sub")
        if not email:
            raise Exception("Invalid token payload")

        # Get user data
        user = self.user_repository.get_user_auth_data_by_email(email)
        if not user:
            raise Exception("User not found")

        return CurrentUserDto(
            user_id=user.id.value,
            email=user.email,
            is_active=user.is_active
        )
