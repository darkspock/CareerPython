from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from src.notification_bc.in_app_notification.domain.entities.in_app_notification import InAppNotificationId
from src.notification_bc.in_app_notification.domain.enums.notification_enums import (
    InAppNotificationType,
    InAppNotificationPriority
)


@dataclass
class InAppNotificationDto:
    """DTO for in-app notification data"""
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
