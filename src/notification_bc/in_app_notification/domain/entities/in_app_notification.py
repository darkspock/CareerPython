from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.framework.domain.value_objects.base_id import BaseId
from src.notification_bc.in_app_notification.domain.enums.notification_enums import (
    InAppNotificationType,
    InAppNotificationPriority
)


@dataclass(frozen=True)
class InAppNotificationId(BaseId):
    """Value object for in-app notification ID"""
    pass


@dataclass
class InAppNotification:
    """Domain entity for in-app notifications"""
    id: InAppNotificationId
    user_id: str
    company_id: str
    notification_type: InAppNotificationType
    title: str
    message: str
    priority: InAppNotificationPriority
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime]
    link: Optional[str]
    metadata: Optional[Dict[str, Any]]

    def mark_as_read(self) -> None:
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()

    def mark_as_unread(self) -> None:
        """Mark notification as unread"""
        self.is_read = False
        self.read_at = None

    @staticmethod
    def create(
        id: InAppNotificationId,
        user_id: str,
        company_id: str,
        notification_type: InAppNotificationType,
        title: str,
        message: str,
        priority: InAppNotificationPriority = InAppNotificationPriority.NORMAL,
        link: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> 'InAppNotification':
        """Factory method for creating a new in-app notification"""
        return InAppNotification(
            id=id,
            user_id=user_id,
            company_id=company_id,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            is_read=False,
            created_at=datetime.utcnow(),
            read_at=None,
            link=link,
            metadata=metadata
        )
