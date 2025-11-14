from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass
class GetUserLanguageQuery(Query):
    """Query to get user's preferred language"""
    user_id: str


class GetUserLanguageQueryHandler(QueryHandler[GetUserLanguageQuery, str]):
    """Handler for getting user's preferred language"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, query: GetUserLanguageQuery) -> str:
        """Handle the get user language query"""
        # Get user by ID
        user_id = UserId.from_string(query.user_id)
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError(f"User with id {query.user_id} not found")

        return user.preferred_language
