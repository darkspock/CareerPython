import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

import requests

from core.config import settings
from src.shared.domain.interfaces.email_service import EmailServiceInterface
from src.notification.domain.exceptions.notification_exceptions import EmailSendingException


class MailgunService(EmailServiceInterface):
    """Service for sending emails through Mailgun (Production)"""

    def __init__(self) -> None:
        self.api_key = settings.MAILGUN_API_KEY
        self.domain = settings.MAILGUN_DOMAIN
        self.api_url = settings.MAILGUN_API_URL
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
        # Mailgun has its own retry mechanism
        self.logger.info("Mailgun handles email retries automatically")
        return 0

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get email delivery statistics from Mailgun"""
        try:
            if not self.api_key or not self.domain:
                return {"error": "Mailgun not configured"}

            url = f"{self.api_url}/{self.domain}/stats/total"
            response = requests.get(
                url,
                auth=("api", self.api_key),
                params={"event": ["accepted", "delivered", "failed"]},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                return dict(data) if isinstance(data, dict) else {"error": "Invalid response format"}
            else:
                return {"error": f"Failed to get stats: {response.status_code}"}

        except Exception as e:
            self.logger.error(f"Error getting delivery stats: {str(e)}")
            return {"error": str(e)}

    def get_failed_emails(self) -> List[Dict[str, Any]]:
        """Get list of failed email attempts from Mailgun"""
        try:
            if not self.api_key or not self.domain:
                return []

            url = f"{self.api_url}/{self.domain}/events"
            response = requests.get(
                url,
                auth=("api", self.api_key),
                params={"event": "failed"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                return list(items) if isinstance(items, list) else []
            else:
                self.logger.error(f"Failed to get failed emails: {response.status_code}")
                return []

        except Exception as e:
            self.logger.error(f"Error getting failed emails: {str(e)}")
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

    def _send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None) -> bool:
        """Send email through Mailgun API"""
        try:
            if not self.api_key or not self.domain:
                self.logger.warning("Mailgun not configured, skipping email send")
                return True  # Return True for dev environments

            url = f"{self.api_url}/{self.domain}/messages"

            data = {
                "from": f"CareerPython <noreply@{self.domain}>",
                "to": to_email,
                "subject": subject,
                "html": html_content
            }

            if text_content:
                data["text"] = text_content

            response = requests.post(
                url,
                auth=("api", self.api_key),
                data=data,
                timeout=30
            )

            if response.status_code == 200:
                self.logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                error_msg = f"Mailgun API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise EmailSendingException(error_msg)

        except requests.RequestException as e:
            error_msg = f"Network error sending email: {str(e)}"
            self.logger.error(error_msg)
            raise EmailSendingException(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error sending email: {str(e)}"
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
