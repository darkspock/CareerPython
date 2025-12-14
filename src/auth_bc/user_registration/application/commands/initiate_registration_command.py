import logging
from dataclasses import dataclass
from typing import Optional

from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user_registration.domain.entities import UserRegistration
from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId
from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.framework.domain.entities.base import generate_id


@dataclass
class InitiateRegistrationCommand(Command):
    """Command to initiate user registration from landing page"""
    email: str
    company_id: Optional[str] = None
    job_position_id: Optional[str] = None
    pdf_file: Optional[bytes] = None
    pdf_filename: Optional[str] = None
    pdf_content_type: Optional[str] = None

    # Output field - populated during execution
    registration_id: Optional[str] = None


class InitiateRegistrationCommandHandler(CommandHandler[InitiateRegistrationCommand]):
    """Handler to initiate user registration process"""

    def __init__(
            self,
            user_registration_repository: UserRegistrationRepositoryInterface,
            user_repository: UserRepositoryInterface,
            command_bus: CommandBus
    ):
        self.user_registration_repository = user_registration_repository
        self.user_repository = user_repository
        self.command_bus = command_bus
        self.logger = logging.getLogger(__name__)

    def execute(self, command: InitiateRegistrationCommand) -> None:
        """Execute registration initiation"""
        try:
            # 1. Check if there's already a pending registration for this email+job_position
            if command.job_position_id:
                existing_registration = self.user_registration_repository.get_by_email_and_job_position(
                    command.email, command.job_position_id
                )
                if existing_registration and not existing_registration.is_expired():
                    self.logger.info(f"Pending registration already exists for {command.email} and job {command.job_position_id}")
                    # Resend verification email
                    self._send_verification_email(existing_registration.id)
                    command.registration_id = str(existing_registration.id)
                    return

            # 2. Check if email belongs to existing user
            existing_user = self.user_repository.get_by_email(command.email)
            existing_user_id = str(existing_user.id) if existing_user else None

            # 3. Create new user_registration
            registration_id = UserRegistrationId(generate_id())

            file_size = len(command.pdf_file) if command.pdf_file else None

            registration = UserRegistration.create(
                id=registration_id,
                email=command.email,
                company_id=command.company_id,
                job_position_id=command.job_position_id,
                file_name=command.pdf_filename,
                file_size=file_size,
                content_type=command.pdf_content_type or "application/pdf",
                token_expiration_hours=24
            )

            # Link to existing user if found
            if existing_user_id:
                registration.link_to_existing_user(existing_user_id)
                self.logger.info(f"Registration linked to existing user {existing_user_id}")

            # 4. Save registration
            self.user_registration_repository.save(registration)
            self.logger.info(f"Created user_registration {registration_id} for {command.email}")

            # 5. Send verification email
            self._send_verification_email(registration_id)

            # 6. Start PDF processing if file provided
            if command.pdf_file:
                self._start_pdf_processing(registration_id, command.pdf_file)

            # Set output
            command.registration_id = str(registration_id)

        except Exception as e:
            self.logger.error(f"Error initiating registration: {str(e)}")
            raise

    def _send_verification_email(self, registration_id: UserRegistrationId) -> None:
        """Send verification email"""
        try:
            from src.auth_bc.user_registration.application.commands.send_verification_email_command import \
                SendVerificationEmailCommand

            email_command = SendVerificationEmailCommand(
                registration_id=str(registration_id)
            )
            self.command_bus.dispatch(email_command)
            self.logger.info(f"Dispatched verification email for registration {registration_id}")

        except Exception as e:
            self.logger.error(f"Error sending verification email: {str(e)}")
            # Don't raise - email failure shouldn't break registration

    def _start_pdf_processing(self, registration_id: UserRegistrationId, pdf_bytes: bytes) -> None:
        """Start async PDF processing"""
        try:
            from src.auth_bc.user_registration.application.commands.process_registration_pdf_command import \
                ProcessRegistrationPdfCommand

            process_command = ProcessRegistrationPdfCommand(
                registration_id=str(registration_id),
                pdf_bytes=pdf_bytes
            )
            self.command_bus.dispatch(process_command)
            self.logger.info(f"Dispatched PDF processing for registration {registration_id}")

        except Exception as e:
            self.logger.error(f"Error starting PDF processing: {str(e)}")
            # Don't raise - PDF processing failure shouldn't break registration
