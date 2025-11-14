import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, Any, List, Optional

from core.config import settings
from src.framework.domain.interfaces.email_service import EmailServiceInterface
from src.notification_bc.notification.domain.exceptions.notification_exceptions import EmailSendingException


class SMTPEmailService(EmailServiceInterface):
    """SMTP-based email service for development using Mailpit or any SMTP server"""

    def __init__(self) -> None:
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from_email = settings.SMTP_FROM_EMAIL
        self.smtp_use_tls = settings.SMTP_USE_TLS

        self.logger = logging.getLogger(__name__)
        # Go up 4 levels: services -> infrastructure -> notification -> src, then go to shared
        self.template_dir = Path(__file__).parent.parent.parent.parent / "shared" / "infrastructure" / "services" / "email_templates"

    async def send_password_reset(self, email: str, reset_token: str) -> bool:
        """Send password reset email to user"""
        try:
            reset_url = f"{settings.FRONTEND_URL}/candidate/reset-password?token={reset_token}"
            template_data = {
                "reset_url": reset_url,
                "reset_token": reset_token,
                "user_name": email.split("@")[0],
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("password_reset.html", template_data)
            subject = "Password Reset Request - CareerPython"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending password reset email: {str(e)}")
            raise EmailSendingException(f"Failed to send password reset email: {str(e)}")

    async def send_welcome_email(self, email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        try:
            template_data = {
                "user_name": user_name,
                "login_url": f"{settings.FRONTEND_URL}/login",
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("welcome.html", template_data)
            subject = f"Welcome to CareerPython, {user_name}!"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending welcome email: {str(e)}")
            raise EmailSendingException(f"Failed to send welcome email: {str(e)}")

    async def send_subscription_confirmation(self, email: str, subscription_details: dict) -> bool:
        """Send subscription confirmation email"""
        try:
            template_data = {
                "user_name": subscription_details.get("user_name", email.split("@")[0]),
                "tier": subscription_details.get("tier", "Premium"),
                "amount": subscription_details.get("amount", "0.00"),
                "billing_cycle": subscription_details.get("billing_cycle", "monthly"),
                "next_billing_date": subscription_details.get("next_billing_date", "N/A"),
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("subscription_confirmation.html", template_data)
            subject = "Subscription Confirmed - CareerPython"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending subscription confirmation email: {str(e)}")
            raise EmailSendingException(f"Failed to send subscription confirmation email: {str(e)}")

    async def send_subscription_renewal_reminder(
            self,
            email: str,
            user_name: str,
            days_until_expiry: int,
            tier: str
    ) -> bool:
        """Send subscription renewal reminder"""
        try:
            template_data = {
                "user_name": user_name,
                "days_until_expiry": days_until_expiry,
                "tier": tier,
                "renewal_url": f"{settings.FRONTEND_URL}/subscription/renew",
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("subscription_renewal_reminder.html", template_data)
            subject = f"Your {tier} subscription expires in {days_until_expiry} days"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending renewal reminder email: {str(e)}")
            raise EmailSendingException(f"Failed to send renewal reminder email: {str(e)}")

    async def send_subscription_expired_notification(
            self,
            email: str,
            user_name: str,
            expired_tier: str
    ) -> bool:
        """Send subscription expired notification"""
        try:
            template_data = {
                "user_name": user_name,
                "expired_tier": expired_tier,
                "renewal_url": f"{settings.FRONTEND_URL}/subscription/renew",
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("subscription_expired.html", template_data)
            subject = f"Your {expired_tier} subscription has expired"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending subscription expired email: {str(e)}")
            raise EmailSendingException(f"Failed to send subscription expired email: {str(e)}")

    async def retry_failed_emails(self) -> int:
        """Retry sending failed emails that are ready for retry"""
        # For development, we don't need retry logic
        self.logger.info("Retry failed emails not implemented for SMTP service")
        return 0

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get email delivery statistics"""
        # For development, return empty stats
        return {
            "total_sent": 0,
            "total_failed": 0,
            "success_rate": 100.0
        }

    def get_failed_emails(self) -> List[Dict[str, Any]]:
        """Get list of failed email attempts"""
        # For development, return empty list
        return []

    async def send_user_invitation(
        self,
        email: str,
        company_name: str,
        invitation_link: str,
        inviter_name: Optional[str] = None,
        custom_message: Optional[str] = None
    ) -> bool:
        """Send user invitation email to join a company"""
        try:
            # Build custom message section if provided
            custom_message_section = ""
            if custom_message:
                custom_message_section = f"""
            <div class="invitation-message">
                <p><strong>Message from {inviter_name or 'the team'}:</strong></p>
                <p class="custom-message">{custom_message}</p>
            </div>
            """
            
            template_data = {
                "company_name": company_name,
                "invitation_link": invitation_link,
                "inviter_name": inviter_name or "the team",
                "custom_message": custom_message or "",
                "custom_message_section": custom_message_section,
                "user_email": email.split("@")[0],
                "support_email": settings.SUPPORT_EMAIL
            }

            html_content = self._load_template("user_invitation.html", template_data)
            subject = f"You've been invited to join {company_name} on CareerPython"

            return self._send_email(email, subject, html_content)

        except Exception as e:
            self.logger.error(f"Error sending user invitation email: {str(e)}")
            raise EmailSendingException(f"Failed to send user invitation email: {str(e)}")

    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.smtp_from_email
            msg["To"] = to_email

            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Send email
            if self.smtp_use_tls:
                # Use STARTTLS
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                # Plain SMTP (for Mailpit in development)
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)

            self.logger.info(f"Email sent successfully to {to_email}: {subject}")
            return True

        except smtplib.SMTPException as e:
            error_msg = f"SMTP error sending email to {to_email}: {str(e)}"
            self.logger.error(error_msg)
            raise EmailSendingException(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error sending email to {to_email}: {str(e)}"
            self.logger.error(error_msg)
            raise EmailSendingException(error_msg)

    def _load_template(self, template_name: str, template_data: Dict[str, Any]) -> str:
        """Load and render email template"""
        try:
            template_path = self.template_dir / template_name

            if not template_path.exists():
                raise EmailSendingException(f"Template not found: {template_name}")

            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            # Simple template rendering using string replacement
            for key, value in template_data.items():
                placeholder = f"{{{{{key}}}}}"
                template_content = template_content.replace(placeholder, str(value))

            return template_content

        except FileNotFoundError:
            raise EmailSendingException(f"Template file not found: {template_name}")
        except Exception as e:
            raise EmailSendingException(f"Error loading template {template_name}: {str(e)}")
