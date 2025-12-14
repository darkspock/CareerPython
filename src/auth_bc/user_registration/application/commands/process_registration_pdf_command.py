import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.auth_bc.user.infrastructure.services.pdf_processing_service import PDFProcessingService
from src.auth_bc.user_registration.domain.enums import ProcessingStatusEnum
from src.auth_bc.user_registration.domain.repositories import UserRegistrationRepositoryInterface
from src.auth_bc.user_registration.domain.value_objects import UserRegistrationId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.interfaces.ai_service_interface import AIServiceInterface


@dataclass
class ProcessRegistrationPdfCommand(Command):
    """Command to process PDF for user registration"""
    registration_id: str
    pdf_bytes: bytes


class ProcessRegistrationPdfCommandHandler(CommandHandler[ProcessRegistrationPdfCommand]):
    """Handler to process PDF and extract content for registration"""

    def __init__(
            self,
            user_registration_repository: UserRegistrationRepositoryInterface,
            pdf_processing_service: PDFProcessingService,
            ai_service: AIServiceInterface
    ):
        self.user_registration_repository = user_registration_repository
        self.pdf_processing_service = pdf_processing_service
        self.ai_service = ai_service
        self.logger = logging.getLogger(__name__)

    def execute(self, command: ProcessRegistrationPdfCommand) -> None:
        """Execute PDF processing for registration"""
        registration_id = UserRegistrationId(command.registration_id)

        try:
            # 1. Get registration
            registration = self.user_registration_repository.get_by_id(registration_id)
            if not registration:
                self.logger.error(f"Registration {registration_id} not found")
                return

            # 2. Update status to processing
            registration.set_processing_status(ProcessingStatusEnum.PROCESSING)
            self.user_registration_repository.update(registration)

            # 3. Validate PDF
            if not self.pdf_processing_service.validate_pdf_file(command.pdf_bytes):
                self.logger.warning(f"Invalid PDF file for registration {registration_id}")
                registration.set_processing_status(ProcessingStatusEnum.FAILED)
                self.user_registration_repository.update(registration)
                return

            # 4. Extract text from PDF
            extraction_result = self.pdf_processing_service.extract_text_from_pdf(command.pdf_bytes)

            if extraction_result["status"] != "completed":
                self.logger.warning(f"PDF extraction failed for registration {registration_id}")
                registration.set_processing_status(ProcessingStatusEnum.FAILED)
                self.user_registration_repository.update(registration)
                return

            text_content = extraction_result["text"]

            # 5. Run AI analysis to extract structured data
            extracted_data = self._extract_structured_data(text_content)

            # 6. Update registration with extracted content
            registration.set_extracted_content(text_content, extracted_data)
            self.user_registration_repository.update(registration)

            self.logger.info(f"PDF processing completed for registration {registration_id}")

        except Exception as e:
            self.logger.error(f"Error processing PDF for registration {registration_id}: {str(e)}")
            # Try to update status to failed
            try:
                registration = self.user_registration_repository.get_by_id(registration_id)
                if registration:
                    registration.set_processing_status(ProcessingStatusEnum.FAILED)
                    self.user_registration_repository.update(registration)
            except Exception:
                pass
            raise

    def _extract_structured_data(self, text_content: str) -> Dict[str, Any]:
        """Extract structured data from PDF text using AI"""
        try:
            # Use AI service to analyze the resume
            analysis_result = self.ai_service.analyze_resume_pdf(text_content)

            if analysis_result and analysis_result.success:
                # Extract personal info from candidate_info dict
                candidate_info = analysis_result.candidate_info or {}
                return {
                    "personal_info": {
                        "full_name": candidate_info.get("full_name"),
                        "email": candidate_info.get("email"),
                        "phone": candidate_info.get("phone"),
                        "linkedin": candidate_info.get("linkedin"),
                        "location": candidate_info.get("location"),
                    },
                    "experience": analysis_result.experiences,
                    "education": analysis_result.educations,
                    "skills": analysis_result.skills,
                    "projects": analysis_result.projects,
                }

        except Exception as e:
            self.logger.warning(f"AI analysis failed, using basic extraction: {str(e)}")

        # Fallback to basic regex extraction
        return self._basic_extraction(text_content)

    def _basic_extraction(self, text_content: str) -> Dict[str, Any]:
        """Basic extraction using regex patterns"""
        import re

        data: Dict[str, Any] = {
            "personal_info": {},
            "experience": [],
            "education": [],
            "skills": [],
            "projects": []
        }

        # Extract email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text_content)
        if emails:
            data["personal_info"]["email"] = emails[0]

        # Extract phone (Spanish and international formats)
        phone_patterns = [
            r'(?:\+34|0034)?[\s.-]?[6789]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}',
            r'\+?\d{1,3}[\s.-]?\(?\d{2,3}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}'
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text_content)
            if phones:
                data["personal_info"]["phone"] = phones[0].strip()
                break

        # Extract LinkedIn
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin:?\s*)([a-zA-Z0-9_-]+)'
        linkedin = re.search(linkedin_pattern, text_content, re.IGNORECASE)
        if linkedin:
            data["personal_info"]["linkedin"] = f"https://linkedin.com/in/{linkedin.group(1)}"

        # Extract name (first line that looks like a name)
        lines = text_content.strip().split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line) < 50:
                # Check if it's not an email or URL
                if '@' not in line and 'http' not in line.lower():
                    data["personal_info"]["full_name"] = line
                    break

        return data
