from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class EmailServiceInterface(ABC):
    """Interface for email service operations"""

    @abstractmethod
    async def send_password_reset(self, email: str, reset_token: str) -> bool:
        """Send password reset email to user"""
        pass

    @abstractmethod
    async def send_welcome_email(self, email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        pass

    @abstractmethod
    async def send_subscription_confirmation(self, email: str, subscription_details: dict) -> bool:
        """Send subscription confirmation email"""
        pass

    @abstractmethod
    async def send_subscription_renewal_reminder(
            self,
            email: str,
            user_name: str,
            days_until_expiry: int,
            tier: str
    ) -> bool:
        """Send subscription renewal reminder"""
        pass

    @abstractmethod
    async def send_subscription_expired_notification(
            self,
            email: str,
            user_name: str,
            expired_tier: str
    ) -> bool:
        """Send subscription expired notification"""
        pass

    @abstractmethod
    async def retry_failed_emails(self) -> int:
        """Retry sending failed emails that are ready for retry"""
        pass

    @abstractmethod
    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get email delivery statistics"""
        pass

    @abstractmethod
    def get_failed_emails(self) -> List[Dict[str, Any]]:
        """Get list of failed email attempts"""
        pass

    @abstractmethod
    async def send_user_invitation(
            self,
            email: str,
            company_name: str,
            invitation_link: str,
            inviter_name: Optional[str] = None,
            custom_message: Optional[str] = None
    ) -> bool:
        """Send user invitation email to join a company"""
        pass
