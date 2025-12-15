import logging
from typing import Optional

from fastapi import UploadFile, HTTPException

from src.auth_bc.user.application import CreateAccessTokenQuery
from src.auth_bc.user.application.queries.dtos.auth_dto import TokenDto
from src.auth_bc.user_registration.application.commands import (
    InitiateRegistrationCommand,
    VerifyRegistrationCommand,
)
from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class RegistrationController:
    """Controller for user registration with email verification"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus,
            user_registration_repository: UserRegistrationRepositoryInterface
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.user_registration_repository = user_registration_repository
        self.logger = logging.getLogger(__name__)

    async def initiate_registration(
            self,
            email: str,
            company_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            resume_file: Optional[UploadFile] = None,
            gdpr_consent: bool = False
    ) -> dict:
        """Initiate registration process with email verification"""
        try:
            # Validate GDPR consent
            if not gdpr_consent:
                raise HTTPException(
                    status_code=400,
                    detail="GDPR consent is required"
                )

            # Process PDF file if provided
            pdf_bytes = None
            pdf_filename = None
            pdf_content_type = None

            if resume_file:
                # Validate file type
                if resume_file.content_type != "application/pdf":
                    raise HTTPException(status_code=400, detail="Only PDF files are allowed")

                # Read file content
                pdf_bytes = await resume_file.read()
                pdf_filename = resume_file.filename
                pdf_content_type = resume_file.content_type

                # Validate file size (max 10MB)
                if len(pdf_bytes) > 10 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="File size too large (max 10MB)")

            # Create and execute command
            command = InitiateRegistrationCommand(
                email=email,
                company_id=company_id,
                job_position_id=job_position_id,
                pdf_file=pdf_bytes,
                pdf_filename=pdf_filename,
                pdf_content_type=pdf_content_type
            )

            self.command_bus.dispatch(command)

            return {
                "success": True,
                "message": "Please check your email to verify your registration",
                "registration_id": command.registration_id
            }

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error initiating registration: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error. Please try again."
            )

    async def verify_registration(self, token: str) -> dict:
        """Verify registration and create user"""
        try:
            # Create and execute command
            command = VerifyRegistrationCommand(verification_token=token)
            self.command_bus.dispatch(command)

            # Generate access token
            access_token = None
            if command.user_id:
                try:
                    # Get user email from registration
                    registration = self.user_registration_repository.get_by_verification_token(token)
                    if registration:
                        token_data = {"sub": registration.email}
                        token_query = CreateAccessTokenQuery(data=token_data)
                        token_dto: TokenDto = self.query_bus.query(token_query)
                        access_token = token_dto.access_token
                except Exception as token_error:
                    self.logger.warning(f"Could not generate token: {str(token_error)}")

            # Determine redirect URL
            redirect_url = "/candidate/onboarding/complete-profile"
            if command.has_job_application:
                redirect_url = "/candidate/application/wizard"

            return {
                "success": True,
                "message": "Registration verified successfully",
                "user_id": command.user_id,
                "candidate_id": command.candidate_id,
                "is_new_user": command.is_new_user,
                "has_job_application": command.has_job_application,
                "job_position_id": command.job_position_id,
                "access_token": access_token,
                "redirect_url": redirect_url
            }

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            self.logger.error(f"Error verifying registration: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error. Please try again."
            )

    async def get_registration_status(self, registration_id: str) -> dict:
        """Get registration status and processing progress"""
        try:
            reg_id = UserRegistrationId(registration_id)
            registration = self.user_registration_repository.get_by_id(reg_id)

            if not registration:
                raise HTTPException(status_code=404, detail="Registration not found")

            # Extract preview data from extracted_data
            preview_data = None
            if registration.extracted_data:
                personal_info = registration.extracted_data.get("personal_info", {})
                preview_data = {
                    "name": personal_info.get("full_name"),
                    "email": personal_info.get("email"),
                    "phone": personal_info.get("phone"),
                }

            return {
                "registration_id": str(registration.id),
                "status": registration.status.value,
                "processing_status": registration.processing_status.value,
                "is_verified": registration.is_verified(),
                "is_expired": registration.is_expired(),
                "has_pdf": registration.has_pdf(),
                "preview_data": preview_data
            }

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error getting registration status: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
