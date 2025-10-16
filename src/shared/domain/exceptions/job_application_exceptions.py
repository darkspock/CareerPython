"""
Job application-related domain exceptions
"""
from typing import Optional, List, Any

from .base import DomainException, BusinessRuleException


class JobApplicationException(DomainException):
    """Base exception for job application-related errors"""

    def __init__(
            self,
            message: str,
            application_id: Optional[str] = None,
            job_id: Optional[str] = None,
            candidate_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if application_id:
            self.details.update({"application_id": application_id})
        if job_id:
            self.details.update({"job_id": job_id})
        if candidate_id:
            self.details.update({"candidate_id": candidate_id})


class JobApplicationNotFoundException(JobApplicationException):
    """Raised when job application is not found"""

    def __init__(
            self,
            application_id: str,
            **kwargs: Any
    ):
        message = f"Job application with id {application_id} not found"
        super().__init__(message, application_id=application_id, **kwargs)


class JobApplicationLimitExceededException(BusinessRuleException):
    """Raised when job application limits are exceeded"""

    def __init__(
            self,
            message: str,
            current_count: int,
            limit: int,
            period: str,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        self.current_count = current_count
        self.limit = limit
        self.period = period
        self.details.update({
            "current_count": current_count,
            "limit": limit,
            "period": period
        })


class JobDescriptionException(JobApplicationException):
    """Base exception for job description-related errors"""

    def __init__(
            self,
            message: str,
            job_description_length: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if job_description_length:
            self.details.update({"job_description_length": job_description_length})


class JobDescriptionValidationException(JobDescriptionException):
    """Raised when job description validation fails"""

    def __init__(
            self,
            message: str,
            validation_errors: Optional[List[str]] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_errors:
            self.details.update({"validation_errors": validation_errors})


class JobDescriptionTooShortException(JobDescriptionValidationException):
    """Raised when job description is too short for analysis"""

    def __init__(
            self,
            message: str = "Job description is too short for meaningful analysis",
            min_length: Optional[int] = None,
            actual_length: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if min_length:
            self.details.update({"min_length": min_length})
        if actual_length:
            self.details.update({"actual_length": actual_length})


class JobDescriptionTooLongException(JobDescriptionValidationException):
    """Raised when job description exceeds maximum length"""

    def __init__(
            self,
            message: str = "Job description exceeds maximum length",
            max_length: Optional[int] = None,
            actual_length: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if max_length:
            self.details.update({"max_length": max_length})
        if actual_length:
            self.details.update({"actual_length": actual_length})


class JobAnalysisException(JobApplicationException):
    """Raised when job analysis fails"""

    def __init__(
            self,
            message: str = "Failed to analyze job description",
            analysis_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if analysis_stage:
            self.details.update({"analysis_stage": analysis_stage})


class JobMatchingException(JobApplicationException):
    """Raised when job matching fails"""

    def __init__(
            self,
            message: str = "Failed to match candidate to job",
            matching_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if matching_stage:
            self.details.update({"matching_stage": matching_stage})


class CoverLetterGenerationException(JobApplicationException):
    """Raised when cover letter generation fails"""

    def __init__(
            self,
            message: str = "Failed to generate cover letter",
            generation_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if generation_stage:
            self.details.update({"generation_stage": generation_stage})


class ResumeCustomizationException(JobApplicationException):
    """Raised when resume customization fails"""

    def __init__(
            self,
            message: str = "Failed to customize resume for job",
            customization_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if customization_stage:
            self.details.update({"customization_stage": customization_stage})


class ApplicationHistoryException(JobApplicationException):
    """Raised when application history operations fail"""

    def __init__(
            self,
            message: str,
            history_operation: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if history_operation:
            self.details.update({"history_operation": history_operation})


class DuplicateApplicationException(JobApplicationException):
    """Raised when duplicate job application is detected"""

    def __init__(
            self,
            message: str = "Duplicate job application detected",
            existing_application_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if existing_application_id:
            self.details.update({"existing_application_id": existing_application_id})


class ApplicationStatusException(JobApplicationException):
    """Raised when application status operations fail"""

    def __init__(
            self,
            message: str,
            current_status: Optional[str] = None,
            target_status: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if current_status:
            self.details.update({"current_status": current_status})
        if target_status:
            self.details.update({"target_status": target_status})
