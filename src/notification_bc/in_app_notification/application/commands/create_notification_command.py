from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.framework.application.command_bus import Command, CommandHandler
from src.notification_bc.in_app_notification.domain.entities.in_app_notification import (
    InAppNotification,
    InAppNotificationId
)
from src.notification_bc.in_app_notification.domain.enums.notification_enums import (
    InAppNotificationType,
    InAppNotificationPriority
)
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)


@dataclass
class CreateNotificationCommand(Command):
    """Command to create a new in-app notification"""
    id: InAppNotificationId
    user_id: str
    company_id: str
    notification_type: InAppNotificationType
    title: str
    message: str
    priority: InAppNotificationPriority = InAppNotificationPriority.NORMAL
    link: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CreateNotificationCommandHandler(CommandHandler[CreateNotificationCommand]):
    """Handler for CreateNotificationCommand"""

    def __init__(self, repository: InAppNotificationRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateNotificationCommand) -> None:
        notification = InAppNotification.create(
            id=command.id,
            user_id=command.user_id,
            company_id=command.company_id,
            notification_type=command.notification_type,
            title=command.title,
            message=command.message,
            priority=command.priority,
            link=command.link,
            metadata=command.metadata
        )

        self.repository.save(notification)
