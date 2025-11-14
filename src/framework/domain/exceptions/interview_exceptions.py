"""
Interview-related domain exceptions
"""
from typing import Optional, List, Any

from .base import DomainException


class InterviewException(DomainException):
    """Base exception for interview-related errors"""

    def __init__(
            self,
            message: str,
            interview_id: Optional[str] = None,
            candidate_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if interview_id:
            self.details.update({"interview_id": interview_id})
        if candidate_id:
            self.details.update({"candidate_id": candidate_id})


class InterviewNotFoundException(InterviewException):
    """Raised when interview is not found"""

    def __init__(
            self,
            interview_id: str,
            **kwargs: Any
    ):
        message = f"Interview with id {interview_id} not found"
        super().__init__(message, interview_id=interview_id, **kwargs)


class InvalidInterviewStateException(InterviewException):
    """Raised when interview operation is invalid for current state"""

    def __init__(
            self,
            message: str,
            current_state: Optional[str] = None,
            required_state: Optional[str] = None,
            operation: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if current_state:
            self.details.update({"current_state": current_state})
        if required_state:
            self.details.update({"required_state": required_state})
        if operation:
            self.details.update({"operation": operation})


class InterviewAlreadyCompletedException(InvalidInterviewStateException):
    """Raised when trying to modify a completed interview"""

    def __init__(
            self,
            message: str = "Interview is already completed",
            completed_at: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(
            message,
            current_state="COMPLETED",
            required_state="IN_PROGRESS",
            **kwargs
        )
        if completed_at:
            self.details.update({"completed_at": completed_at})


class InterviewNotStartedException(InvalidInterviewStateException):
    """Raised when trying to access interview that hasn't started"""

    def __init__(
            self,
            message: str = "Interview has not been started",
            **kwargs: Any
    ):
        super().__init__(
            message,
            current_state="NOT_STARTED",
            required_state="IN_PROGRESS",
            **kwargs
        )


class InterviewTemplateException(InterviewException):
    """Base exception for interview template errors"""

    def __init__(
            self,
            message: str,
            template_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if template_id:
            self.details.update({"template_id": template_id})


class InterviewTemplateNotFoundException(InterviewTemplateException):
    """Raised when interview template is not found"""

    def __init__(
            self,
            template_id: str,
            **kwargs: Any
    ):
        message = f"Interview template with id {template_id} not found"
        super().__init__(message, template_id=template_id, **kwargs)


class InterviewQuestionException(InterviewException):
    """Base exception for interview question errors"""

    def __init__(
            self,
            message: str,
            question_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if question_id:
            self.details.update({"question_id": question_id})


class InterviewQuestionNotFoundException(InterviewQuestionException):
    """Raised when interview question is not found"""

    def __init__(
            self,
            question_id: str,
            **kwargs: Any
    ):
        message = f"Interview question with id {question_id} not found"
        super().__init__(message, question_id=question_id, **kwargs)


class InterviewAnswerException(InterviewException):
    """Base exception for interview answer errors"""

    def __init__(
            self,
            message: str,
            answer_id: Optional[str] = None,
            question_id: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if answer_id:
            self.details.update({"answer_id": answer_id})
        if question_id:
            self.details.update({"question_id": question_id})


class InterviewAnswerValidationException(InterviewAnswerException):
    """Raised when interview answer validation fails"""

    def __init__(
            self,
            message: str,
            validation_rules: Optional[List[str]] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if validation_rules:
            self.details.update({"validation_rules": validation_rules})


class InterviewProgressException(InterviewException):
    """Raised when interview progress tracking fails"""

    def __init__(
            self,
            message: str,
            current_section: Optional[str] = None,
            progress_percentage: Optional[float] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if current_section:
            self.details.update({"current_section": current_section})
        if progress_percentage is not None:
            self.details.update({"progress_percentage": progress_percentage})


class InterviewSectionException(InterviewException):
    """Raised when interview section operations fail"""

    def __init__(
            self,
            message: str,
            section_name: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if section_name:
            self.details.update({"section_name": section_name})


class InterviewTimeoutException(InterviewException):
    """Raised when interview session times out"""

    def __init__(
            self,
            message: str = "Interview session has timed out",
            timeout_duration: Optional[int] = None,
            last_activity: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if timeout_duration:
            self.details.update({"timeout_duration": timeout_duration})
        if last_activity:
            self.details.update({"last_activity": last_activity})


class InterviewConcurrencyException(InterviewException):
    """Raised when concurrent interview operations conflict"""

    def __init__(
            self,
            message: str = "Concurrent interview operation detected",
            conflicting_operation: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if conflicting_operation:
            self.details.update({"conflicting_operation": conflicting_operation})


class InterviewDataInconsistencyException(InterviewException):
    """Raised when interview data is inconsistent"""

    def __init__(
            self,
            message: str,
            inconsistency_type: Optional[str] = None,
            **kwargs: Any
    ):
        super().__init__(message, **kwargs)
        if inconsistency_type:
            self.details.update({"inconsistency_type": inconsistency_type})
