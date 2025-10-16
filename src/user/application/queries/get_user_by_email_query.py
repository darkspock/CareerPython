from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.staff.infrastructure.repositories.staff_repository import StaffRepositoryInterface
from src.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface


@dataclass
class GetUserByEmailQuery(Query):
    email: str


class GetUserByEmailQueryHandler(QueryHandler[GetUserByEmailQuery, Optional[CurrentUserDto]]):
    def __init__(self, user_repository: UserRepositoryInterface, staff_repository: StaffRepositoryInterface):
        self.user_repository = user_repository
        self.staff_repository = staff_repository

    def handle(self, query: GetUserByEmailQuery) -> Optional[CurrentUserDto]:
        """Get user by email address"""
        user = self.user_repository.get_by_email(query.email)
        if user:
            # Create CurrentUserDto from user entity
            user_dto = CurrentUserDto(
                user_id=str(user.id),
                email=user.email,
                is_active=user.is_active
            )

            # Add staff information if available
            if self.staff_repository:
                try:
                    staff = self.staff_repository.get_by_user_id(user_id=user.id)
                    if staff:
                        user_dto = CurrentUserDto(
                            user_id=str(user.id),
                            email=user.email,
                            is_active=user.is_active,
                            is_staff=True,
                            roles=getattr(staff, 'roles', [])
                        )
                except Exception:
                    # If staff repository fails, continue without staff info
                    pass

            return user_dto
        return None
