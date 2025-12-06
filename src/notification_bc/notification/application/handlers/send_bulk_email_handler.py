"""
Send Bulk Email Command Handler
Handles sending emails to multiple recipients using a template
"""
import asyncio
import logging
from dataclasses import dataclass
from typing import List

from src.framework.application.command_bus import CommandHandler
from src.framework.domain.interfaces.email_service import EmailServiceInterface
from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import \
    EmailTemplateRepositoryInterface
from src.notification_bc.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.notification_bc.notification.application.commands.send_bulk_email_command import (
    SendBulkEmailCommand,
    BulkEmailRecipient
)


@dataclass
class BulkEmailResult:
    """Result of bulk email sending"""
    total: int
    successful: int
    failed: int
    failed_recipients: List[str]


class SendBulkEmailCommandHandler(CommandHandler[SendBulkEmailCommand]):
    """Handler to send bulk emails"""

    def __init__(
            self,
            email_service: EmailServiceInterface,
            email_template_repository: EmailTemplateRepositoryInterface
    ):
        self.email_service = email_service
        self.email_template_repository = email_template_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, command: SendBulkEmailCommand) -> None:
        """Execute bulk email sending command"""
        try:
            self.logger.info(
                f"📧 SendBulkEmailCommandHandler.execute() - Sending to {len(command.recipients)} recipients"
            )

            # Get the email template
            template_id = EmailTemplateId.from_string(command.template_id)
            template = self.email_template_repository.get_by_id(template_id)

            if not template:
                self.logger.error(f"❌ Email template not found: {command.template_id}")
                raise ValueError(f"Email template not found: {command.template_id}")

            if not template.is_active:
                self.logger.error(f"❌ Email template is not active: {command.template_id}")
                raise ValueError(f"Email template is not active: {command.template_id}")

            # Send emails to all recipients
            result = self._send_bulk_emails_sync(
                recipients=command.recipients,
                subject=template.subject,
                body_html=template.body_html,
                body_text=template.body_text
            )

            self.logger.info(
                f"✅ Bulk email completed: {result.successful}/{result.total} sent successfully"
            )

            if result.failed > 0:
                self.logger.warning(
                    f"⚠️ {result.failed} emails failed: {result.failed_recipients}"
                )

        except Exception as e:
            self.logger.error(f"❌ Bulk email sending failed: {str(e)}", exc_info=True)
            raise

    def _send_bulk_emails_sync(
            self,
            recipients: List[BulkEmailRecipient],
            subject: str,
            body_html: str,
            body_text: str | None
    ) -> BulkEmailResult:
        """Synchronous wrapper for async email sending"""
        try:
            # Check if we're already in an event loop
            try:
                asyncio.get_running_loop()
                # We're in an event loop, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run,
                        self._send_bulk_emails(recipients, subject, body_html, body_text)
                    )
                    return future.result()
            except RuntimeError:
                # No event loop, we can use asyncio.run()
                return asyncio.run(
                    self._send_bulk_emails(recipients, subject, body_html, body_text)
                )
        except Exception as e:
            self.logger.error(f"❌ Error in _send_bulk_emails_sync: {str(e)}", exc_info=True)
            return BulkEmailResult(
                total=len(recipients),
                successful=0,
                failed=len(recipients),
                failed_recipients=[r.email for r in recipients]
            )

    async def _send_bulk_emails(
            self,
            recipients: List[BulkEmailRecipient],
            subject: str,
            body_html: str,
            body_text: str | None
    ) -> BulkEmailResult:
        """Send emails to all recipients"""
        successful = 0
        failed = 0
        failed_recipients: List[str] = []

        for recipient in recipients:
            try:
                success = await self.email_service.send_template_email(
                    email=recipient.email,
                    subject=subject,
                    body_html=body_html,
                    body_text=body_text,
                    template_data=recipient.template_data
                )

                if success:
                    successful += 1
                    self.logger.debug(f"✅ Email sent to {recipient.email}")
                else:
                    failed += 1
                    failed_recipients.append(recipient.email)
                    self.logger.warning(f"❌ Failed to send email to {recipient.email}")

            except Exception as e:
                failed += 1
                failed_recipients.append(recipient.email)
                self.logger.error(f"❌ Error sending to {recipient.email}: {str(e)}")

        return BulkEmailResult(
            total=len(recipients),
            successful=successful,
            failed=failed,
            failed_recipients=failed_recipients
        )
