import logging
from dataclasses import dataclass

from src.shared.application.command_bus import Command, CommandHandler
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.user.domain.services.password_service import PasswordService

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResetPasswordWithTokenCommand(Command):
    """Command to reset password using a reset token"""
    reset_token: str
    new_password: str


class ResetPasswordWithTokenCommandHandler(CommandHandler[ResetPasswordWithTokenCommand]):
    """Handler for resetting password with token"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, command: ResetPasswordWithTokenCommand) -> None:
        """
        Handle password reset with token

        Note: This is a command handler, so it doesn't return data.
        The success/failure result should be handled via events or separate queries.
        """
        log.info("ResetPasswordWithTokenCommand called")

        try:
            # Get user by reset token
            user = self.user_repository.get_by_reset_token(command.reset_token)
            if not user:
                log.warning("Invalid reset token provided")
                # For security, don't reveal if token is invalid - just return silently
                return

            # Hash the new password
            new_hashed_password = PasswordService.hash_password(command.new_password)

            # Validate token and reset password
            if user.reset_password(new_hashed_password, command.reset_token):
                # Update user in database
                self.user_repository.update(user.id, {
                    'hashed_password': user.hashed_password,
                    'password_reset_token': None,
                    'password_reset_expires_at': None
                })
                log.info(f"Password reset successful for user: {user.id}")
            else:
                log.warning("Password reset failed - invalid or expired token")

        except Exception as e:
            log.error(f"Error in ResetPasswordWithTokenCommand: {str(e)}")
            raise
