import logging
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Tuple, Any

from src.candidate.application.commands.create_candidate import CreateCandidateCommand
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_application.application.commands.create_candidate_application import \
    CreateCandidateApplicationCommand
from src.notification.application.commands.send_email_command import SendEmailCommand
from src.notification.domain.enums.notification_type import NotificationTypeEnum
from src.resume.application.commands.analyze_pdf_resume_command import AnalyzePDFResumeCommand
from src.shared.application.command_bus import Command
from src.shared.application.command_bus import CommandHandler, CommandBus
from src.shared.domain.entities.async_job import AsyncJobId
from src.shared.domain.entities.base import generate_id
from src.user.domain.entities.user import User
from src.user.domain.entities.user_asset import UserAsset
from src.user.domain.enums.asset_enums import AssetTypeEnum
from src.user.domain.repositories.user_asset_repository_interface import UserAssetRepositoryInterface
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.user.domain.services.password_service import PasswordService
from src.user.domain.value_objects.UserId import UserId
from src.user.domain.value_objects.user_asset_id import UserAssetId
from src.user.infrastructure.services.pdf_processing_service import PDFProcessingService


@dataclass
class CreateUserFromLandingCommand(Command):
    """Command to create user from landing page"""
    email: str
    pdf_file: Optional[bytes] = None
    pdf_filename: Optional[str] = None
    job_position_id: Optional[str] = None  # NEW FIELD for job application

    # Fields populated during execution
    user_asset_id: Optional[str] = None
    candidate_id: Optional[str] = None


class CreateUserFromLandingCommandHandler(CommandHandler[CreateUserFromLandingCommand]):
    """Handler to create user from landing page"""

    def __init__(
            self,
            user_repository: UserRepositoryInterface,
            user_asset_repository: UserAssetRepositoryInterface,
            pdf_processing_service: PDFProcessingService,
            command_bus: CommandBus
    ):
        self.user_repository = user_repository
        self.user_asset_repository = user_asset_repository
        self.pdf_processing_service = pdf_processing_service
        self.command_bus = command_bus
        self.logger = logging.getLogger(__name__)
        # Remove instance variable - we'll store in command instead

    def execute(self, command: CreateUserFromLandingCommand) -> None:
        """Execute command to create user from landing"""
        try:
            # 1. Check if user exists
            existing_user = self.user_repository.get_by_email(command.email)
            user_id = None
            candidate_id = None

            if existing_user:
                self.logger.info(f"User {command.email} already exists, using existing user")
                user_id = existing_user.id
                # Try to find existing candidate
                # TODO: Get candidate by user_id when we have that query
                candidate_id = CandidateId(generate_id())  # For now, generate new
            else:
                # 2. Create new user with random password
                user_id = UserId(generate_id())
                candidate_id = CandidateId(generate_id())  # Generate candidate_id for new users

                plain_password = User.generate_random_password()
                hashed_password = PasswordService.hash_password(plain_password)

                user = User(
                    id=user_id,
                    email=command.email,
                    hashed_password=hashed_password,
                    is_active=True
                )
                self.user_repository.create(user)
                self.logger.info(f"Created new user {command.email}")

            # 3. Process PDF if provided
            extracted_data: Optional[Dict[str, str]] = None
            if command.pdf_file and command.pdf_filename:
                pdf_result = self._process_pdf(user_id, command.pdf_file, command.pdf_filename)
                extracted_data, user_asset_id = pdf_result
                command.user_asset_id = str(user_asset_id) if user_asset_id else None

            # 4. Create candidate if not exists
            if not existing_user:  # Only create candidate for new users
                candidate_command = CreateCandidateCommand(
                    id=candidate_id,
                    name=extracted_data.get("full_name", "New Candidate") if extracted_data else "New Candidate",
                    email=command.email,
                    user_id=user_id,
                    # Set minimal required fields - user will complete later
                    date_of_birth=date(1970, 1, 1),  # Default date, will be updated in onboarding
                    city="",
                    country="",
                    phone=extracted_data.get("phone", "") if extracted_data else "",
                    linkedin_url=extracted_data.get("linkedin_url", "") if extracted_data else "",
                )
                self.command_bus.dispatch(candidate_command)
                self.logger.info(f"Created candidate for user {command.email}")

            # Store candidate_id in command for later use
            command.candidate_id = str(candidate_id) if candidate_id else None

            # 5. Phase 10: Create job application if job_position_id provided
            if command.job_position_id and candidate_id:
                application_command = CreateCandidateApplicationCommand(
                    candidate_id=str(candidate_id),
                    job_position_id=command.job_position_id,
                    notes="Application created during onboarding process"
                )
                self.command_bus.dispatch(application_command)
                self.logger.info(f"Created job application for position {command.job_position_id}")

            # 6. Send password reset email for new users
            if not existing_user:
                self.logger.info(f"🔔 Starting password reset email process for new user: {command.email}")
                # Retrieve the user to generate reset token
                created_user: Optional[User] = self.user_repository.get_by_email(command.email)
                if created_user:
                    reset_token = created_user.request_password_reset()
                    self.user_repository.update_entity(created_user)
                    self._send_password_reset_email(command.email, reset_token, extracted_data)
                else:
                    self.logger.warning(f"❌ User {command.email} not found for password reset email")

        except Exception as e:
            self.logger.error(f"Error creating user from landing: {str(e)}")
            raise

    def _process_pdf(self, user_id: UserId, pdf_bytes: bytes, filename: str) -> Tuple[
        Optional[Dict[str, str]], Optional[UserAssetId]]:
        """Process PDF and extract information"""
        try:
            # Validate PDF
            if not self.pdf_processing_service.validate_pdf_file(pdf_bytes):
                self.logger.warning(f"Invalid PDF file: {filename}")
                return None, None

            # Extract text
            extraction_result = self.pdf_processing_service.extract_text_from_pdf(pdf_bytes)

            # Create UserAsset
            asset_id = UserAssetId(generate_id())
            content_dict: Dict[str, Any] = {"original_filename": filename}
            user_asset = UserAsset.create(
                id=asset_id,
                user_id=user_id,
                asset_type=AssetTypeEnum.PDF_RESUME,
                content=content_dict,
                file_name=filename,
                file_size=len(pdf_bytes),
                content_type="application/pdf"
            )

            # Set extracted text and processing result
            if extraction_result["status"] == "completed":
                user_asset.set_extracted_text(extraction_result["text"])
                user_asset.add_metadata("extraction_metadata", extraction_result["metadata"])
            else:
                user_asset.set_processing_status(
                    extraction_result["status"],
                    extraction_result.get("error")
                )

            # Save asset
            self.user_asset_repository.save(user_asset)

            # Don't start analysis here - let the controller handle it to get job_id
            # analysis_job_id = None
            # if candidate_id and user_asset.text_content:
            #     analysis_job_id = self._start_pdf_analysis(asset_id, candidate_id)

            # Extract data using regex (name, phone, LinkedIn)
            extracted_data: Optional[Dict[str, str]] = None
            if user_asset.text_content:
                extracted_data = user_asset.extract_pdf_data()
                if extracted_data:
                    self.logger.info(f"Extracted data: {extracted_data}")

            return extracted_data, asset_id

        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")

        return None, None

    def _start_pdf_analysis(self, user_asset_id: UserAssetId, candidate_id: CandidateId) -> Optional[str]:
        """Start automatic PDF analysis with AI and return job_id"""
        try:
            # Generate job ID
            job_id = AsyncJobId(generate_id())

            # Create PDF analysis command
            analysis_command = AnalyzePDFResumeCommand(
                job_id=job_id,
                user_asset_id=user_asset_id,
                candidate_id=candidate_id,
                timeout_seconds=30
            )

            # Execute command - this will start the Dramatiq actor
            self.command_bus.dispatch(analysis_command)

            self.logger.info(
                f"Started PDF analysis job {job_id} for candidate {candidate_id} and asset {user_asset_id}")
            return str(job_id)

        except Exception as e:
            self.logger.error(f"Failed to start PDF analysis: {str(e)}")
            # Don't raise - PDF analysis failure shouldn't break user creation
            return None

    def _send_password_reset_email(self, email: str, reset_token: str,
                                   extracted_data: Optional[Dict[str, str]]) -> None:
        """Send password reset email to new user"""
        try:
            name = "User"
            if extracted_data:
                name = extracted_data.get("first_name", "User")

            email_command = SendEmailCommand(
                recipient_email=email,
                subject="Set Your Password - CareerPython",
                template_name="password_reset",
                notification_type=NotificationTypeEnum.PASSWORD_RESET,
                template_data={
                    "name": name,
                    "reset_token": reset_token
                }
            )

            self.command_bus.dispatch(email_command)

        except Exception as e:
            self.logger.error(f"❌ Error sending password reset email: {str(e)}", exc_info=True)
            # Don't raise - email failure shouldn't break user creation
