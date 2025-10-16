from dataclasses import dataclass

from src.shared.application.query_bus import Query, QueryHandler
from src.user.application.queries.dtos.auth_dto import UserExistsDto
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface


@dataclass(frozen=True)
class CheckUserExistsQuery(Query):
    """Query to check if a user exists by email"""
    email: str


class CheckUserExistsQueryHandler(QueryHandler[CheckUserExistsQuery, UserExistsDto]):
    """Handler for checking user existence"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, query: CheckUserExistsQuery) -> UserExistsDto:
        """
        Handle user existence check

        Returns:
            UserExistsDto with existence status and email
        """
        user = self.user_repository.get_by_email(query.email)
        exists = user is not None

        return UserExistsDto(
            exists=exists,
            email=query.email
        )
