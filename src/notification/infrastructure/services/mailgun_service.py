import logging
from typing import Dict, Any, Optional

import requests

from core.config import settings
from src.notification.domain.exceptions.notification_exceptions import EmailSendingException


class MailgunService:
    """Service for sending emails through Mailgun"""

    def __init__(self) -> None:
        self.api_key = settings.MAILGUN_API_KEY
        self.domain = settings.MAILGUN_DOMAIN
        self.api_url = settings.MAILGUN_API_URL
        self.logger = logging.getLogger(__name__)

    def send_email(
            self,
            recipient_email: str,
            subject: str,
            html_content: str,
            text_content: Optional[str] = None
    ) -> bool:
        """Send email through Mailgun"""
        try:
            if not self.api_key or not self.domain:
                self.logger.warning("Mailgun not configured, skipping email send")
                return True  # Return True for dev environments

            url = f"{self.api_url}/{self.domain}/messages"

            data = {
                "from": f"CareerPython <noreply@{self.domain}>",
                "to": recipient_email,
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
                self.logger.info(f"Email sent successfully to {recipient_email}")
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

    def send_template_email(
            self,
            recipient_email: str,
            subject: str,
            template_name: str,
            template_data: Dict[str, Any]
    ) -> bool:
        """Send email using a template"""
        try:
            # Simple template rendering - in production you might want to use Jinja2
            html_content = self._render_template(template_name, template_data)
            return self.send_email(recipient_email, subject, html_content)
        except Exception as e:
            error_msg = f"Error sending template email: {str(e)}"
            self.logger.error(error_msg)
            raise EmailSendingException(error_msg)

    def _render_template(self, template_name: str, template_data: Dict[str, Any]) -> str:
        """Render email template with data"""
        # Simple template rendering - replace with proper template engine in production
        templates = {
            "welcome_email": """
            <html>
                <body>
                    <h1>Welcome to CareerPython!</h1>
                    <p>Hello {name},</p>
                    <p>Your account has been successfully created.</p>
                    <p>To change your password, click on the following link:</p>
                    <a href="{reset_url}">Change password</a>
                    <p>Best regards,<br>The CareerPython team</p>
                </body>
            </html>
            """,
            "password_reset": """
            <html>
                <body>
                    <h1>Reset Password</h1>
                    <p>Hello {name},</p>
                    <p>You have requested to change your password.</p>
                    <p>Click on the following link to proceed:</p>
                    <a href="{reset_url}">Reset password</a>
                    <p>This link will expire in 24 hours.</p>
                    <p>Best regards,<br>The CareerPython team</p>
                </body>
            </html>
            """
        }

        template = templates.get(template_name)
        if not template:
            raise EmailSendingException(f"Template '{template_name}' not found")

        try:
            return template.format(**template_data)
        except KeyError as e:
            raise EmailSendingException(f"Missing template data: {e}")
        except Exception as e:
            raise EmailSendingException(f"Template rendering error: {e}")
