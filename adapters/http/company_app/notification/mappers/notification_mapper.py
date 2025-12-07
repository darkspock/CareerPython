from typing import List

from src.notification_bc.in_app_notification.application.queries.shared.in_app_notification_dto import (
    InAppNotificationDto
)
from src.notification_bc.in_app_notification.application.queries.list_user_notifications_query import (
    ListUserNotificationsResult
)
from adapters.http.company_app.notification.schemas.notification_schemas import (
    InAppNotificationResponse,
    NotificationListResponse
)


class InAppNotificationMapper:
    """Mapper for DTO to Response conversion"""

    @staticmethod
    def dto_to_response(dto: InAppNotificationDto) -> InAppNotificationResponse:
        """Convert notification DTO to response"""
        return InAppNotificationResponse(
            id=str(dto.id.value),
            user_id=dto.user_id,
            company_id=dto.company_id,
            notification_type=dto.notification_type.value,
            title=dto.title,
            message=dto.message,
            priority=dto.priority.value,
            is_read=dto.is_read,
            created_at=dto.created_at.isoformat(),
            read_at=dto.read_at.isoformat() if dto.read_at else None,
            link=dto.link,
            metadata=dto.metadata
        )

    @staticmethod
    def dto_list_to_response(result: ListUserNotificationsResult) -> NotificationListResponse:
        """Convert notification list result to response"""
        return NotificationListResponse(
            notifications=[
                InAppNotificationMapper.dto_to_response(dto)
                for dto in result.notifications
            ],
            total_count=result.total_count,
            unread_count=result.unread_count
        )
