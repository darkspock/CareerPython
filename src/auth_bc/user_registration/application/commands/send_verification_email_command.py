import logging
from dataclasses import dataclass

from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId
from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.notification_bc.notification.application.commands.send_email_command import SendEmailCommand
from src.notification_bc.notification.domain.enums.notification_type import NotificationTypeEnum
from core.config import settings


@dataclass
class SendVerificationEmailCommand(Command):
    """Command to send verification email for registration"""
    registration_id: str


class SendVerificationEmailCommandHandler(CommandHandler[SendVerificationEmailCommand]):
    """Handler to send verification email"""

    def __init__(
            self,
            user_registration_repository: UserRegistrationRepositoryInterface,
            command_bus: CommandBus
    ):
        self.user_registration_repository = user_registration_repository
        self.command_bus = command_bus
        self.logger = logging.getLogger(__name__)

    def execute(self, command: SendVerificationEmailCommand) -> None:
        """Send verification email to user"""
        registration_id = UserRegistrationId(command.registration_id)

        try:
            # 1. Get registration
            registration = self.user_registration_repository.get_by_id(registration_id)
            if not registration:
                self.logger.error(f"Registration {registration_id} not found")
                return

            # 2. Check if already verified
            if registration.is_verified():
                self.logger.info(f"Registration {registration_id} already verified, skipping email")
                return

            # 3. Build verification URL
            base_url = settings.FRONTEND_URL
            verification_url = f"{base_url}/candidate/registration/verify/{registration.verification_token}"

            # 4. Send email
            email_command = SendEmailCommand(
                recipient_email=registration.email,
                subject="Verify Your Email - CareerPython",
                template_name="email_verification",
                notification_type=NotificationTypeEnum.EMAIL_VERIFICATION,
                template_data={
                    "verification_url": verification_url,
                    "token": registration.verification_token,
                    "expiration_hours": 24
                }
            )

            self.command_bus.dispatch(email_command)
            self.logger.info(f"Verification email sent to {registration.email}")

        except Exception as e:
            self.logger.error(f"Error sending verification email: {str(e)}")
            raise
