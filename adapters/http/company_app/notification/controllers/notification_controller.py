from src.framework.application.query_bus import QueryBus
from src.framework.application.command_bus import CommandBus
from src.notification_bc.in_app_notification.domain.entities.in_app_notification import InAppNotificationId
from src.notification_bc.in_app_notification.application.queries.list_user_notifications_query import (
    ListUserNotificationsQuery,
    ListUserNotificationsResult
)
from src.notification_bc.in_app_notification.application.queries.get_unread_count_query import (
    GetUnreadCountQuery
)
from src.notification_bc.in_app_notification.application.commands.mark_notification_as_read_command import (
    MarkNotificationAsReadCommand
)
from src.notification_bc.in_app_notification.application.commands.mark_all_notifications_as_read_command import (
    MarkAllNotificationsAsReadCommand
)
from src.notification_bc.in_app_notification.application.commands.delete_notification_command import (
    DeleteNotificationCommand
)
from adapters.http.company_app.notification.schemas.notification_schemas import (
    NotificationListResponse,
    UnreadCountResponse
)
from adapters.http.company_app.notification.mappers.notification_mapper import (
    InAppNotificationMapper
)


class NotificationController:
    """Controller for in-app notification operations"""

    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def list_notifications(
        self,
        user_id: str,
        company_id: str,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False
    ) -> NotificationListResponse:
        """List notifications for the current user"""
        result: ListUserNotificationsResult = self.query_bus.query(
            ListUserNotificationsQuery(
                user_id=user_id,
                company_id=company_id,
                limit=limit,
                offset=offset,
                unread_only=unread_only
            )
        )
        return InAppNotificationMapper.dto_list_to_response(result)

    def get_unread_count(self, user_id: str, company_id: str) -> UnreadCountResponse:
        """Get unread notification count"""
        count: int = self.query_bus.query(
            GetUnreadCountQuery(
                user_id=user_id,
                company_id=company_id
            )
        )
        return UnreadCountResponse(unread_count=count)

    def mark_as_read(self, notification_id: str, user_id: str, company_id: str) -> None:
        """Mark a notification as read"""
        self.command_bus.execute(
            MarkNotificationAsReadCommand(
                notification_id=InAppNotificationId(notification_id),
                user_id=user_id,
                company_id=company_id
            )
        )

    def mark_all_as_read(self, user_id: str, company_id: str) -> None:
        """Mark all notifications as read"""
        self.command_bus.execute(
            MarkAllNotificationsAsReadCommand(
                user_id=user_id,
                company_id=company_id
            )
        )

    def delete_notification(self, notification_id: str, user_id: str, company_id: str) -> None:
        """Delete a notification"""
        self.command_bus.execute(
            DeleteNotificationCommand(
                notification_id=InAppNotificationId(notification_id),
                user_id=user_id,
                company_id=company_id
            )
        )
