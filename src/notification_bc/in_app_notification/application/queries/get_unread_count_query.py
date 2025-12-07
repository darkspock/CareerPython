from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)


@dataclass
class GetUnreadCountQuery(Query):
    """Query to get the count of unread notifications for a user"""
    user_id: str
    company_id: str


class GetUnreadCountQueryHandler(QueryHandler[GetUnreadCountQuery, int]):
    """Handler for GetUnreadCountQuery"""

    def __init__(self, repository: InAppNotificationRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetUnreadCountQuery) -> int:
        return self.repository.get_unread_count(
            user_id=query.user_id,
            company_id=query.company_id
        )
