"""
Candidate and resume-related domain exceptions
"""
from typing import Optional, List, Any

from .base import DomainException, ValidationException, BusinessRuleException


class CandidateException(DomainException):
    """Base exception for candidate-related errors"""

    def __init__(
            self,
            message: str,
            candidate_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if candidate_id:
            self.details.update({"candidate_id": candidate_id})


class CandidateNotFoundException(CandidateException):
    """Raised when candidate is not found"""

    def __init__(
            self,
            candidate_id: str,
            **kwargs: Any
    ):
        message = f"Candidate with id {candidate_id} not found"
        super().__init__(message, candidate_id=candidate_id, **kwargs)


class CandidateValidationException(ValidationException):
    """Raised when candidate data validation fails"""

    def __init__(
            self,
            message: str,
            validation_errors: Optional[List[str]] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_errors:
            self.details.update({"validation_errors": validation_errors})


class ResumeException(CandidateException):
    """Base exception for resume-related errors"""

    def __init__(
            self,
            message: str,
            resume_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if resume_id:
            self.details.update({"resume_id": resume_id})


class ResumeUploadException(ResumeException):
    """Raised when resume upload fails"""

    def __init__(
            self,
            message: str,
            file_name: Optional[str] = None,
            file_size: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if file_name:
            self.details.update({"file_name": file_name})
        if file_size:
            self.details.update({"file_size": file_size})


class InvalidResumeFormatException(ResumeUploadException):
    """Raised when resume format is not supported"""

    def __init__(
            self,
            message: str = "Resume format is not supported",
            file_format: Optional[str] = None,
            supported_formats: Optional[List[str]] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if file_format:
            self.details.update({"file_format": file_format})
        if supported_formats:
            self.details.update({"supported_formats": supported_formats})


class ResumeSizeExceededException(ResumeUploadException):
    """Raised when resume file size exceeds limit"""

    def __init__(
            self,
            message: str = "Resume file size exceeds limit",
            file_size: Optional[int] = None,
            max_size: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, file_size=file_size, **kwargs)
        if max_size:
            self.details.update({"max_size": max_size})


class ResumeExtractionException(ResumeException):
    """Raised when resume data extraction fails"""

    def __init__(
            self,
            message: str = "Failed to extract data from resume",
            extraction_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if extraction_stage:
            self.details.update({"extraction_stage": extraction_stage})


class ResumeGenerationException(ResumeException):
    """Raised when resume generation fails"""

    def __init__(
            self,
            message: str = "Failed to generate resume",
            template_type: Optional[str] = None,
            generation_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if template_type:
            self.details.update({"template_type": template_type})
        if generation_stage:
            self.details.update({"generation_stage": generation_stage})


class ResumeDownloadException(ResumeException):
    """Raised when resume download fails"""

    def __init__(
            self,
            message: str = "Failed to download resume",
            download_format: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if download_format:
            self.details.update({"download_format": download_format})


class ExperienceException(CandidateException):
    """Base exception for experience-related errors"""

    def __init__(
            self,
            message: str,
            experience_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if experience_id:
            self.details.update({"experience_id": experience_id})


class ExperienceValidationException(ExperienceException):
    """Raised when experience data validation fails"""

    def __init__(
            self,
            message: str,
            validation_field: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_field:
            self.details.update({"validation_field": validation_field})


class EducationException(CandidateException):
    """Base exception for education-related errors"""

    def __init__(
            self,
            message: str,
            education_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if education_id:
            self.details.update({"education_id": education_id})


class EducationValidationException(EducationException):
    """Raised when education data validation fails"""

    def __init__(
            self,
            message: str,
            validation_field: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_field:
            self.details.update({"validation_field": validation_field})


class ProjectException(CandidateException):
    """Base exception for project-related errors"""

    def __init__(
            self,
            message: str,
            project_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if project_id:
            self.details.update({"project_id": project_id})


class ProjectValidationException(ProjectException):
    """Raised when project data validation fails"""

    def __init__(
            self,
            message: str,
            validation_field: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_field:
            self.details.update({"validation_field": validation_field})


class ProfileSectionException(CandidateException):
    """Raised when profile section operations fail"""

    def __init__(
            self,
            message: str,
            section_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if section_type:
            self.details.update({"section_type": section_type})


class ProfileIncompleteException(BusinessRuleException):
    """Raised when profile is incomplete for operation"""

    def __init__(
            self,
            message: str = "Profile is incomplete",
            missing_sections: Optional[List[str]] = None,
            completion_percentage: Optional[float] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if missing_sections:
            self.details.update({"missing_sections": missing_sections})
        if completion_percentage is not None:
            self.details.update({"completion_percentage": completion_percentage})
