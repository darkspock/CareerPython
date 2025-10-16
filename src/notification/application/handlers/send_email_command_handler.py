import logging

from src.notification.application.commands.send_email_command import SendEmailCommand
from src.notification.domain.entities.email_notification import EmailNotification, NotificationId
from src.notification.domain.exceptions.notification_exceptions import EmailSendingException
from src.notification.infrastructure.services.mailgun_service import MailgunService
from src.shared.application.command_bus import CommandHandler
from src.shared.domain.entities.base import generate_id


class SendEmailCommandHandler(CommandHandler[SendEmailCommand]):
    """Handler para enviar emails"""

    def __init__(self, mailgun_service: MailgunService):
        self.mailgun_service = mailgun_service
        self.logger = logging.getLogger(__name__)

    def execute(self, command: SendEmailCommand) -> None:
        """Ejecutar comando de enviar email"""
        try:
            # Create notification entity for tracking
            notification_id = NotificationId(generate_id())
            notification = EmailNotification.create(
                id=notification_id,
                recipient_email=command.recipient_email,
                subject=command.subject,
                template_name=command.template_name,
                notification_type=command.notification_type,
                template_data=command.template_data
            )

            # Send email using Mailgun service
            success = self.mailgun_service.send_template_email(
                recipient_email=command.recipient_email,
                subject=command.subject,
                template_name=command.template_name,
                template_data=command.template_data
            )

            if success:
                notification.mark_as_sent()
                self.logger.info(f"Email sent successfully to {command.recipient_email}")
            else:
                notification.mark_as_failed("Failed to send email")
                self.logger.error(f"Failed to send email to {command.recipient_email}")

        except EmailSendingException as e:
            self.logger.error(f"Email sending failed: {str(e)}")
            # In a full implementation, you might want to save this to a repository
            # for retry logic or audit purposes
        except Exception as e:
            self.logger.error(f"Unexpected error sending email: {str(e)}")
            raise
