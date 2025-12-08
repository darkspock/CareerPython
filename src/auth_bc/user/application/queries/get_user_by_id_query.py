from dataclasses import dataclass
from typing import Optional

from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetUserByIdQuery(Query):
    user_id: UserId


class GetUserByIdQueryHandler(QueryHandler[GetUserByIdQuery, Optional[CurrentUserDto]]):
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def handle(self, query: GetUserByIdQuery) -> Optional[CurrentUserDto]:
        """Get user by ID"""
        user = self.user_repository.get_by_id(query.user_id)
        if user:
            return CurrentUserDto(
                user_id=str(user.id),
                email=user.email,
                is_active=user.is_active,
                has_password=bool(user.hashed_password)
            )
        return None
