"""
Send Bulk Email Command
Sends emails to multiple recipients using a template
"""
from dataclasses import dataclass
from typing import Dict, Any, List

from src.framework.application.command_bus import Command


@dataclass
class BulkEmailRecipient:
    """A recipient for bulk email"""
    email: str
    name: str
    template_data: Dict[str, Any]


@dataclass
class SendBulkEmailCommand(Command):
    """Command to send bulk emails to multiple recipients"""
    template_id: str
    recipients: List[BulkEmailRecipient]
    company_id: str
    sent_by_user_id: str
