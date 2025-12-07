from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.notification_bc.in_app_notification.domain.entities.in_app_notification import InAppNotificationId
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)
from src.notification_bc.in_app_notification.domain.exceptions.notification_exceptions import (
    InAppNotificationNotFoundException
)


@dataclass
class DeleteNotificationCommand(Command):
    """Command to delete a notification"""
    notification_id: InAppNotificationId
    user_id: str
    company_id: str


class DeleteNotificationCommandHandler(CommandHandler[DeleteNotificationCommand]):
    """Handler for DeleteNotificationCommand"""

    def __init__(self, repository: InAppNotificationRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteNotificationCommand) -> None:
        notification = self.repository.get_by_id(command.notification_id)

        if not notification:
            raise InAppNotificationNotFoundException(str(command.notification_id.value))

        # Verify ownership
        if notification.user_id != command.user_id or notification.company_id != command.company_id:
            raise InAppNotificationNotFoundException(str(command.notification_id.value))

        self.repository.delete(command.notification_id)
