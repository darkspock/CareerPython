"""
Command to clean up expired user registrations.

This command should be run periodically (e.g., daily via cron) to remove
expired pending registrations from the database.
"""
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.auth_bc.user_registration.domain.enums.registration_status import RegistrationStatusEnum
from src.auth_bc.user_registration.domain.repositories.user_registration_repository_interface import (
    UserRegistrationRepositoryInterface
)
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class CleanupExpiredRegistrationsCommand(Command):
    """
    Command to clean up expired user registrations.

    Args:
        max_age_days: Maximum age of PENDING/EXPIRED registrations to keep (default: 7 days).
                     Registrations older than this will be deleted.
        dry_run: If True, only log what would be deleted without actually deleting.
    """
    max_age_days: int = 7
    dry_run: bool = False


class CleanupExpiredRegistrationsCommandHandler(CommandHandler[CleanupExpiredRegistrationsCommand]):
    """
    Handler for cleaning up expired user registrations.

    Finds and deletes registrations that are:
    1. PENDING status with expired tokens (token_expires_at < now)
    2. EXPIRED status older than max_age_days

    This helps keep the database clean and prevents accumulation of
    abandoned registration attempts.
    """

    def __init__(self, repository: UserRegistrationRepositoryInterface):
        self.repository = repository
        self.logger = logging.getLogger(__name__)

    def execute(self, command: CleanupExpiredRegistrationsCommand) -> None:
        """Execute the cleanup command"""
        self.logger.info(
            f"Starting cleanup of expired registrations (max_age_days={command.max_age_days}, "
            f"dry_run={command.dry_run})"
        )

        try:
            # Find expired registrations
            expired_registrations = self.repository.find_expired_registrations()

            # Filter by max age
            cutoff_date = datetime.utcnow() - timedelta(days=command.max_age_days)
            registrations_to_delete = [
                reg for reg in expired_registrations
                if reg.created_at < cutoff_date
            ]

            self.logger.info(
                f"Found {len(expired_registrations)} expired registrations, "
                f"{len(registrations_to_delete)} older than {command.max_age_days} days"
            )

            if command.dry_run:
                self.logger.info("DRY RUN - Would delete the following registrations:")
                for reg in registrations_to_delete:
                    self.logger.info(
                        f"  - ID: {reg.id}, Email: {reg.email}, "
                        f"Created: {reg.created_at}, Status: {reg.status}"
                    )
                return

            # Delete expired registrations
            deleted_count = 0
            for registration in registrations_to_delete:
                try:
                    self.repository.delete(registration.id)
                    deleted_count += 1
                    self.logger.debug(
                        f"Deleted expired registration: {registration.id} ({registration.email})"
                    )
                except Exception as e:
                    self.logger.error(
                        f"Failed to delete registration {registration.id}: {str(e)}"
                    )

            self.logger.info(f"Cleanup completed. Deleted {deleted_count} expired registrations.")

        except Exception as e:
            self.logger.error(f"Error during registration cleanup: {str(e)}")
            raise
