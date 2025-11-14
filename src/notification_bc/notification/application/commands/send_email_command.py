from dataclasses import dataclass
from typing import Dict, Any

from src.notification_bc.notification.domain.enums.notification_type import NotificationTypeEnum
from src.framework.application.command_bus import Command


@dataclass
class SendEmailCommand(Command):
    """Comando para enviar un email"""
    recipient_email: str
    subject: str
    template_name: str
    notification_type: NotificationTypeEnum
    template_data: Dict[str, Any]
