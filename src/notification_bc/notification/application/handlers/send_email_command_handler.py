import asyncio
import logging

from src.framework.application.command_bus import CommandHandler
from src.framework.domain.entities.base import generate_id
from src.framework.domain.interfaces.email_service import EmailServiceInterface
from src.notification_bc.notification.application.commands.send_email_command import SendEmailCommand
from src.notification_bc.notification.domain.entities.email_notification import EmailNotification, NotificationId
from src.notification_bc.notification.domain.enums.notification_type import NotificationTypeEnum
from src.notification_bc.notification.domain.exceptions.notification_exceptions import EmailSendingException


class SendEmailCommandHandler(CommandHandler[SendEmailCommand]):
    """Handler to send emails"""

    def __init__(self, email_service: EmailServiceInterface):
        self.email_service = email_service
        self.logger = logging.getLogger(__name__)

    def execute(self, command: SendEmailCommand) -> None:
        """Execute email sending command"""
        try:
            self.logger.info(f"📧 SendEmailCommandHandler.execute() called for {command.recipient_email}")

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

            success = self._send_email_sync(command)

            if success:
                notification.mark_as_sent()
                self.logger.info(f"✅ Email sent successfully to {command.recipient_email}")
            else:
                notification.mark_as_failed("Failed to send email")
                self.logger.error(f"❌ Failed to send email to {command.recipient_email}")

        except EmailSendingException as e:
            self.logger.error(f"❌ Email sending failed: {str(e)}", exc_info=True)
            # In a full implementation, you might want to save this to a repository
            # for retry logic or audit purposes
        except Exception as e:
            self.logger.error(f"❌ Unexpected error sending email: {str(e)}", exc_info=True)
            raise

    def _send_email_sync(self, command: SendEmailCommand) -> bool:
        """Synchronous wrapper for async email sending"""
        try:
            # Check if we're already in an event loop
            try:
                asyncio.get_running_loop()
                # We're in an event loop, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._send_email(command))
                    return future.result()
            except RuntimeError:
                # No event loop, we can use asyncio.run()
                return asyncio.run(self._send_email(command))
        except Exception as e:
            self.logger.error(f"❌ Error in _send_email_sync: {str(e)}", exc_info=True)
            return False

    async def _send_email(self, command: SendEmailCommand) -> bool:
        """Send email based on notification type"""
        notification_type = command.notification_type

        if notification_type == NotificationTypeEnum.PASSWORD_RESET:
            reset_token = command.template_data.get("reset_token", "")
            return await self.email_service.send_password_reset(
                command.recipient_email,
                reset_token
            )

        elif notification_type == NotificationTypeEnum.WELCOME_EMAIL:
            user_name = command.template_data.get("name", command.recipient_email.split("@")[0])
            return await self.email_service.send_welcome_email(
                command.recipient_email,
                user_name
            )

        elif notification_type == NotificationTypeEnum.SUBSCRIPTION_CONFIRMATION:
            return await self.email_service.send_subscription_confirmation(
                command.recipient_email,
                command.template_data
            )

        elif notification_type == NotificationTypeEnum.SUBSCRIPTION_RENEWAL_REMINDER:
            user_name = command.template_data.get("user_name", "")
            days_until_expiry = command.template_data.get("days_until_expiry", 0)
            tier = command.template_data.get("tier", "")
            return await self.email_service.send_subscription_renewal_reminder(
                command.recipient_email,
                user_name,
                days_until_expiry,
                tier
            )

        elif notification_type == NotificationTypeEnum.SUBSCRIPTION_EXPIRED:
            user_name = command.template_data.get("user_name", "")
            expired_tier = command.template_data.get("expired_tier", "")
            return await self.email_service.send_subscription_expired_notification(
                command.recipient_email,
                user_name,
                expired_tier
            )

        elif notification_type == NotificationTypeEnum.EMAIL_VERIFICATION:
            verification_url = command.template_data.get("verification_url", "")
            expiration_hours = command.template_data.get("expiration_hours", 24)

            subject = "Verify Your Email - CareerPython"
            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2563eb;">Verify Your Email</h1>
                    <p>Thank you for registering! Please click the button below to verify your email address:</p>
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}"
                           style="background-color: #2563eb; color: white; padding: 12px 30px;
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Verify Email
                        </a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #2563eb;">{verification_url}</p>
                    <p style="color: #666; font-size: 14px;">
                        This link will expire in {expiration_hours} hours.
                    </p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px;">
                        If you didn't request this verification, please ignore this email.
                    </p>
                </div>
            </body>
            </html>
            """

            return await self.email_service.send_template_email(
                command.recipient_email,
                subject,
                body_html,
                template_data=command.template_data
            )

        else:
            self.logger.warning(f"Unknown notification type: {notification_type}")
            return False
