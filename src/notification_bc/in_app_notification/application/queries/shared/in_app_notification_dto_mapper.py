from src.notification_bc.in_app_notification.domain.entities.in_app_notification import InAppNotification
from src.notification_bc.in_app_notification.application.queries.shared.in_app_notification_dto import (
    InAppNotificationDto
)


class InAppNotificationDtoMapper:
    """Mapper for converting InAppNotification entity to DTO"""

    @staticmethod
    def from_entity(entity: InAppNotification) -> InAppNotificationDto:
        """Convert entity to DTO"""
        return InAppNotificationDto(
            id=entity.id,
            user_id=entity.user_id,
            company_id=entity.company_id,
            notification_type=entity.notification_type,
            title=entity.title,
            message=entity.message,
            priority=entity.priority,
            is_read=entity.is_read,
            created_at=entity.created_at,
            read_at=entity.read_at,
            link=entity.link,
            metadata=entity.metadata
        )
