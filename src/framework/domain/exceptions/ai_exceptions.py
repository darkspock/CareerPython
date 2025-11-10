"""
AI-specific domain exceptions
"""
from typing import Optional, Any

from .base import ExternalServiceException, ValidationException


class AIProcessingException(ExternalServiceException):
    """Raised when AI service fails to process content"""

    def __init__(
            self,
            message: str,
            operation: Optional[str] = None,
            retry_count: int = 0,
            **kwargs: Any
    ):
        super().__init__(
            message=message,
            service_name="xAI",
            operation=operation,
            retry_count=retry_count,
            **kwargs
        )


class AIServiceUnavailableException(AIProcessingException):
    """Raised when AI service is unavailable or not configured"""

    def __init__(
            self,
            message: str = "AI service is currently unavailable",
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)


class AIResponseParsingException(AIProcessingException):
    """Raised when AI service response cannot be parsed"""

    def __init__(
            self,
            message: str = "Failed to parse AI service response",
            response_format: Optional[str] = None,
            expected_format: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if response_format:
            self.details.update({"response_format": response_format})
        if expected_format:
            self.details.update({"expected_format": expected_format})


class AITimeoutException(AIProcessingException):
    """Raised when AI service request times out"""

    def __init__(
            self,
            message: str = "AI service request timed out",
            timeout_duration: Optional[int] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if timeout_duration:
            self.details.update({"timeout_duration": timeout_duration})


class AIQuotaExceededException(AIProcessingException):
    """Raised when AI service quota is exceeded"""

    def __init__(
            self,
            message: str = "AI service quota exceeded",
            quota_type: Optional[str] = None,
            reset_time: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if quota_type:
            self.details.update({"quota_type": quota_type})
        if reset_time:
            self.details.update({"reset_time": reset_time})


class AIContentValidationException(ValidationException):
    """Raised when AI-generated content fails validation"""

    def __init__(
            self,
            message: str,
            content_type: Optional[str] = None,
            validation_rule: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if content_type:
            self.details.update({"content_type": content_type})
        if validation_rule:
            self.details.update({"validation_rule": validation_rule})


class ResumeProcessingException(AIProcessingException):
    """Raised when resume processing fails"""

    def __init__(
            self,
            message: str,
            processing_stage: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, operation="resume_processing", **kwargs)
        if processing_stage:
            self.details.update({"processing_stage": processing_stage})


class InterviewGenerationException(AIProcessingException):
    """Raised when interview question generation fails"""

    def __init__(
            self,
            message: str,
            interview_section: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, operation="interview_generation", **kwargs)
        if interview_section:
            self.details.update({"interview_section": interview_section})


class JobMatchingException(AIProcessingException):
    """Raised when job matching analysis fails"""

    def __init__(
            self,
            message: str,
            job_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, operation="job_matching", **kwargs)
        if job_id:
            self.details.update({"job_id": job_id})


class ResumeGenerationException(AIProcessingException):
    """Raised when resume generation fails"""

    def __init__(
            self,
            message: str,
            template_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, operation="resume_generation", **kwargs)
        if template_type:
            self.details.update({"template_type": template_type})
