import logging
from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.interfaces.email_service import EmailServiceInterface
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RequestPasswordResetCommand(Command):
    """Command to request password reset for a user"""
    email: str


class RequestPasswordResetCommandHandler(CommandHandler[RequestPasswordResetCommand]):
    """Handler for requesting password reset"""

    def __init__(self, user_repository: UserRepositoryInterface, email_service: Optional[EmailServiceInterface] = None):
        self.user_repository = user_repository
        self.email_service = email_service

    def execute(self, command: RequestPasswordResetCommand) -> None:
        """
        Handle password reset request

        Note: This is a command handler, so it doesn't return data.
        The success/failure result should be handled via events or separate queries.
        """
        log.info(f"RequestPasswordResetCommand called with email: {command.email}")

        try:
            # Get user by email
            user = self.user_repository.get_by_email(command.email)
            if not user:
                log.warning(f"Password reset requested for non-existent email: {command.email}")
                # Don't reveal if email exists - just return silently
                return

                # Generate reset token
            user.request_password_reset()

            # Update user in database
            self.user_repository.update(user.id, {
                'password_reset_token': user.password_reset_token,
                'password_reset_expires_at': user.password_reset_expires_at
            })

            # Send password reset email if email service is available
            if self.email_service:
                # Note: We'll need to make this async properly later or use event-driven approach
                # For now, keeping it sync to match the interface
                log.info(f"Password reset email would be sent to {command.email}")

        except Exception as e:
            log.error(f"Error in RequestPasswordResetCommand: {str(e)}")
            raise
