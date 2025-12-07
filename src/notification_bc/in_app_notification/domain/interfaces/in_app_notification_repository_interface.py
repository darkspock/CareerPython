from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from src.notification_bc.in_app_notification.domain.entities.in_app_notification import (
    InAppNotification,
    InAppNotificationId
)


class InAppNotificationRepositoryInterface(ABC):
    """Repository interface for in-app notifications"""

    @abstractmethod
    def get_by_id(self, notification_id: InAppNotificationId) -> Optional[InAppNotification]:
        """Get notification by ID"""
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: str,
        company_id: str,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False
    ) -> Tuple[List[InAppNotification], int]:
        """List notifications for a user with pagination. Returns (notifications, total_count)"""
        pass

    @abstractmethod
    def get_unread_count(self, user_id: str, company_id: str) -> int:
        """Get count of unread notifications for a user"""
        pass

    @abstractmethod
    def save(self, notification: InAppNotification) -> None:
        """Save a notification"""
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: InAppNotificationId) -> None:
        """Mark a notification as read"""
        pass

    @abstractmethod
    def mark_all_as_read(self, user_id: str, company_id: str) -> int:
        """Mark all notifications as read for a user. Returns count of updated notifications"""
        pass

    @abstractmethod
    def delete(self, notification_id: InAppNotificationId) -> None:
        """Delete a notification"""
        pass

    @abstractmethod
    def delete_old_notifications(self, user_id: str, company_id: str, days: int = 30) -> int:
        """Delete notifications older than specified days. Returns count of deleted notifications"""
        pass
