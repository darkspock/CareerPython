from dataclasses import dataclass
from typing import List, Tuple

from src.framework.application.query_bus import Query, QueryHandler
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)
from src.notification_bc.in_app_notification.application.queries.shared.in_app_notification_dto import (
    InAppNotificationDto
)
from src.notification_bc.in_app_notification.application.queries.shared.in_app_notification_dto_mapper import (
    InAppNotificationDtoMapper
)


@dataclass
class ListUserNotificationsQuery(Query):
    """Query to list notifications for a user"""
    user_id: str
    company_id: str
    limit: int = 20
    offset: int = 0
    unread_only: bool = False


@dataclass
class ListUserNotificationsResult:
    """Result containing notifications and total count"""
    notifications: List[InAppNotificationDto]
    total_count: int
    unread_count: int


class ListUserNotificationsQueryHandler(QueryHandler[ListUserNotificationsQuery, ListUserNotificationsResult]):
    """Handler for ListUserNotificationsQuery"""

    def __init__(self, repository: InAppNotificationRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListUserNotificationsQuery) -> ListUserNotificationsResult:
        notifications, total_count = self.repository.list_by_user(
            user_id=query.user_id,
            company_id=query.company_id,
            limit=query.limit,
            offset=query.offset,
            unread_only=query.unread_only
        )

        unread_count = self.repository.get_unread_count(
            user_id=query.user_id,
            company_id=query.company_id
        )

        return ListUserNotificationsResult(
            notifications=[InAppNotificationDtoMapper.from_entity(n) for n in notifications],
            total_count=total_count,
            unread_count=unread_count
        )
