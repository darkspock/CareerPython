import logging
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any

from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.entities.user_asset import UserAsset
from src.auth_bc.user.domain.enums.asset_enums import AssetTypeEnum
from src.auth_bc.user.domain.repositories.user_asset_repository_interface import UserAssetRepositoryInterface
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.auth_bc.user.domain.value_objects.user_asset_id import UserAssetId
from src.auth_bc.user_registration.domain.entities.user_registration import UserRegistration
from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.candidate_bc.candidate.application.commands.create_candidate import CreateCandidateCommand
from src.candidate_bc.candidate.application.queries.get_candidate_by_email import GetCandidateByEmailQuery
from src.candidate_bc.candidate.application.queries.get_candidate_by_user_id import GetCandidateByUserIdQuery
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.application.commands.create_candidate_application import \
    CreateCandidateApplicationCommand
from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.framework.application.query_bus import QueryBus
from src.framework.domain.entities.base import generate_id
from src.notification_bc.notification.application.commands.send_email_command import SendEmailCommand
from src.notification_bc.notification.domain.enums.notification_type import NotificationTypeEnum


@dataclass
class VerifyRegistrationCommand(Command):
    """Command to verify registration and create user"""
    verification_token: str

    # Output fields - populated during execution
    user_id: Optional[str] = None
    candidate_id: Optional[str] = None
    is_new_user: bool = False
    has_job_application: bool = False
    job_position_id: Optional[str] = None


class VerifyRegistrationCommandHandler(CommandHandler[VerifyRegistrationCommand]):
    """Handler to verify registration and create user/candidate"""

    def __init__(
            self,
            user_registration_repository: UserRegistrationRepositoryInterface,
            user_repository: UserRepositoryInterface,
            user_asset_repository: UserAssetRepositoryInterface,
            command_bus: CommandBus,
            query_bus: QueryBus
    ):
        self.user_registration_repository = user_registration_repository
        self.user_repository = user_repository
        self.user_asset_repository = user_asset_repository
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.logger = logging.getLogger(__name__)

    def execute(self, command: VerifyRegistrationCommand) -> None:
        """Execute registration verification"""
        try:
            # 1. Get registration by token
            registration = self.user_registration_repository.get_by_verification_token(
                command.verification_token
            )

            if not registration:
                raise ValueError("Invalid verification token")

            # 2. Check if already verified - return success with existing data
            if registration.is_verified():
                self.logger.info(f"Registration {registration.id} already verified, returning existing data")
                # Set output fields from registration data
                if registration.existing_user_id:
                    command.user_id = registration.existing_user_id
                    # Get candidate for this user
                    candidate = self._get_or_create_candidate_for_user(
                        UserId(registration.existing_user_id), registration
                    )
                    command.candidate_id = str(candidate)
                    command.is_new_user = False
                else:
                    # For new users who verified, we need to find their user/candidate
                    user = self.user_repository.get_by_email(registration.email)
                    if user:
                        command.user_id = str(user.id)
                        candidate = self._get_or_create_candidate_for_user(user.id, registration)
                        command.candidate_id = str(candidate)
                    command.is_new_user = False
                command.has_job_application = registration.job_position_id is not None
                command.job_position_id = registration.job_position_id
                return  # Exit successfully

            # 3. Check if expired
            if registration.is_expired():
                registration.expire()
                self.user_registration_repository.update(registration)
                raise ValueError("Verification token has expired")

            # 4. Handle existing user or create new one
            user_id: UserId
            candidate_id: CandidateId
            is_new_user = False

            if registration.existing_user_id:
                # Existing user - link to their account
                user_id = UserId(registration.existing_user_id)
                candidate_id = self._get_or_create_candidate_for_user(user_id, registration)
                self.logger.info(f"Linked registration to existing user {user_id}")
            else:
                # New user - create user and candidate
                user_id, candidate_id = self._create_new_user_and_candidate(registration)
                is_new_user = True
                self.logger.info(f"Created new user {user_id} and candidate {candidate_id}")

            # 5. Copy PDF to user_assets if exists
            if registration.has_pdf():
                self._copy_pdf_to_user_assets(user_id, registration)

            # 6. Create job application if job_position_id exists
            has_job_application = False
            if registration.job_position_id:
                self._create_job_application(candidate_id, registration.job_position_id)
                has_job_application = True

            # 7. Mark registration as verified
            registration.verify()
            self.user_registration_repository.update(registration)

            # 8. Send password reset email for new users
            if is_new_user:
                self._send_password_setup_email(registration.email, user_id)

            # Set output fields
            command.user_id = str(user_id)
            command.candidate_id = str(candidate_id)
            command.is_new_user = is_new_user
            command.job_position_id = registration.job_position_id
            command.has_job_application = has_job_application

            self.logger.info(f"Registration verified for {registration.email}")

        except Exception as e:
            self.logger.error(f"Error verifying registration: {str(e)}")
            raise

    def _create_new_user_and_candidate(self, registration: UserRegistration) -> tuple[UserId, CandidateId]:
        """Create new user and candidate from registration"""
        user_id = UserId(generate_id())
        candidate_id = CandidateId(generate_id())

        # Create user with random password
        plain_password = User.generate_random_password()
        hashed_password = PasswordService.hash_password(plain_password)

        user = User(
            id=user_id,
            email=registration.email,
            hashed_password=hashed_password,
            is_active=True
        )
        self.user_repository.create(user)

        # Extract personal info from registration data
        personal_info = self._get_personal_info(registration)

        # Create candidate
        candidate_command = CreateCandidateCommand(
            id=candidate_id,
            name=personal_info.get("full_name", "New Candidate"),
            email=registration.email,
            user_id=user_id,
            date_of_birth=date(1970, 1, 1),  # Default, will be updated in wizard
            city="",
            country="",
            phone=personal_info.get("phone", ""),
            linkedin_url=personal_info.get("linkedin", ""),
        )
        self.command_bus.dispatch(candidate_command)

        return user_id, candidate_id

    def _get_or_create_candidate_for_user(self, user_id: UserId, registration: UserRegistration) -> CandidateId:
        """Get existing candidate or create new one for existing user"""
        from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto

        # First, check if candidate already exists for this user by user_id
        query = GetCandidateByUserIdQuery(user_id=user_id)
        existing_candidate: Optional[CandidateDto] = self.query_bus.query(query)

        if existing_candidate:
            self.logger.info(f"Found existing candidate {existing_candidate.id} for user {user_id}")
            return existing_candidate.id

        # Fallback: check by email (candidate might exist but not linked to user)
        email_query = GetCandidateByEmailQuery(email=registration.email)
        existing_by_email: Optional[CandidateDto] = self.query_bus.query(email_query)

        if existing_by_email:
            self.logger.info(f"Found existing candidate {existing_by_email.id} by email {registration.email}")
            return existing_by_email.id

        # No existing candidate, create a new one
        candidate_id = CandidateId(generate_id())

        personal_info = self._get_personal_info(registration)

        candidate_command = CreateCandidateCommand(
            id=candidate_id,
            name=personal_info.get("full_name", "Existing User"),
            email=registration.email,
            user_id=user_id,
            date_of_birth=date(1970, 1, 1),
            city="",
            country="",
            phone=personal_info.get("phone", ""),
            linkedin_url=personal_info.get("linkedin", ""),
        )
        self.command_bus.dispatch(candidate_command)

        return candidate_id

    def _get_personal_info(self, registration: UserRegistration) -> Dict[str, Any]:
        """Extract personal info from registration extracted_data"""
        if not registration.extracted_data:
            return {}

        personal_info: Dict[str, Any] = registration.extracted_data.get("personal_info", {})
        return personal_info

    def _copy_pdf_to_user_assets(self, user_id: UserId, registration: UserRegistration) -> None:
        """Copy PDF data from registration to user_assets"""
        try:
            asset_id = UserAssetId(generate_id())

            content_dict: Dict[str, Any] = {
                "original_filename": registration.file_name,
                "source": "registration"
            }

            user_asset = UserAsset.create(
                id=asset_id,
                user_id=user_id,
                asset_type=AssetTypeEnum.PDF_RESUME,
                content=content_dict,
                file_name=registration.file_name,
                file_size=registration.file_size,
                content_type=registration.content_type or "application/pdf"
            )

            # Copy extracted text
            if registration.text_content:
                user_asset.set_extracted_text(registration.text_content)

            # Copy extracted data as metadata
            if registration.extracted_data:
                user_asset.add_metadata("extracted_data", registration.extracted_data)

            self.user_asset_repository.save(user_asset)
            self.logger.info(f"Copied PDF to user_assets for user {user_id}")

        except Exception as e:
            self.logger.error(f"Error copying PDF to user_assets: {str(e)}")
            # Don't raise - this shouldn't break verification

    def _create_job_application(self, candidate_id: CandidateId, job_position_id: str) -> None:
        """Create job application for candidate"""
        try:
            application_command = CreateCandidateApplicationCommand(
                candidate_id=str(candidate_id),
                job_position_id=job_position_id,
                notes="Application created during registration verification"
            )
            self.command_bus.dispatch(application_command)
            self.logger.info(f"Created job application for candidate {candidate_id} and position {job_position_id}")

        except Exception as e:
            self.logger.error(f"Error creating job application: {str(e)}")
            # Don't raise - application creation failure shouldn't break verification

    def _send_password_setup_email(self, email: str, user_id: UserId) -> None:
        """Send password setup email to new user"""
        try:
            # Get user to generate reset token
            user = self.user_repository.get_by_id(user_id)
            if not user:
                self.logger.warning(f"User {user_id} not found for password setup email")
                return

            reset_token = user.request_password_reset()
            self.user_repository.update_entity(user)

            email_command = SendEmailCommand(
                recipient_email=email,
                subject="Set Your Password - CareerPython",
                template_name="password_reset",
                notification_type=NotificationTypeEnum.PASSWORD_RESET,
                template_data={
                    "name": "User",
                    "reset_token": reset_token
                }
            )
            self.command_bus.dispatch(email_command)
            self.logger.info(f"Password setup email sent to {email}")

        except Exception as e:
            self.logger.error(f"Error sending password setup email: {str(e)}")
            # Don't raise - email failure shouldn't break verification
