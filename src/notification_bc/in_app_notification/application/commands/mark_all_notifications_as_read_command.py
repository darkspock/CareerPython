from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.notification_bc.in_app_notification.domain.interfaces.in_app_notification_repository_interface import (
    InAppNotificationRepositoryInterface
)


@dataclass
class MarkAllNotificationsAsReadCommand(Command):
    """Command to mark all notifications as read for a user"""
    user_id: str
    company_id: str


class MarkAllNotificationsAsReadCommandHandler(CommandHandler[MarkAllNotificationsAsReadCommand]):
    """Handler for MarkAllNotificationsAsReadCommand"""

    def __init__(self, repository: InAppNotificationRepositoryInterface):
        self.repository = repository

    def execute(self, command: MarkAllNotificationsAsReadCommand) -> None:
        self.repository.mark_all_as_read(
            user_id=command.user_id,
            company_id=command.company_id
        )
