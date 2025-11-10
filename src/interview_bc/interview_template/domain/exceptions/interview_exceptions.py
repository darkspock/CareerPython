from typing import Optional

from src.framework.domain.exceptions import DomainException


class InterviewException(DomainException):
    """Base exception for interview-related errors"""
    pass


# State Management Exceptions
class InvalidInterviewStateException(InterviewException):
    """Raised when interview operation is invalid for current state"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INVALID_INTERVIEW_STATE"


class InterviewNotActiveException(InterviewException):
    """Raised when trying to operate on a non-active interview"""

    def __init__(self, interview_id: str):
        super().__init__(f"Interview {interview_id} is not active")
        self.error_code = "INTERVIEW_NOT_ACTIVE"


class InterviewAlreadyCompletedException(InterviewException):
    """Raised when trying to operate on a completed interview"""

    def __init__(self, interview_id: str):
        super().__init__(f"Interview {interview_id} is already completed")
        self.error_code = "INTERVIEW_ALREADY_COMPLETED"


class InterviewCannotResumeException(InterviewException):
    """Raised when interview cannot be resumed"""

    def __init__(self, interview_id: str, reason: str):
        super().__init__(f"Interview {interview_id} cannot be resumed: {reason}")
        self.error_code = "INTERVIEW_CANNOT_RESUME"


# Session and Question Exceptions
class InterviewSessionNotFoundException(InterviewException):
    """Raised when interview session is not found"""

    def __init__(self, interview_id: str):
        super().__init__(f"Interview session {interview_id} not found")
        self.error_code = "INTERVIEW_SESSION_NOT_FOUND"


class InterviewQuestionMismatchException(InterviewException):
    """Raised when question ID doesn't match current question"""

    def __init__(self, expected_id: str, received_id: str):
        super().__init__(f"Question ID mismatch. Expected: {expected_id}, Received: {received_id}")
        self.error_code = "INTERVIEW_QUESTION_MISMATCH"


class InterviewQuestionNotFoundException(InterviewException):
    """Raised when interview question is not found"""

    def __init__(self, question_id: str, interview_id: str):
        super().__init__(f"Question {question_id} not found in interview {interview_id}")
        self.error_code = "INTERVIEW_QUESTION_NOT_FOUND"


class InterviewQuestionValidationException(InterviewException):
    """Raised when interview question validation fails"""

    def __init__(self, question_id: str, validation_errors: list):
        error_msg = f"Question {question_id} validation failed: {', '.join(validation_errors)}"
        super().__init__(error_msg)
        self.error_code = "INTERVIEW_QUESTION_VALIDATION_FAILED"
        self.validation_errors = validation_errors


# Response and Answer Exceptions
class InterviewResponseValidationException(InterviewException):
    """Raised when interview response validation fails"""

    def __init__(self, response_id: str, validation_errors: list):
        error_msg = f"Response {response_id} validation failed: {', '.join(validation_errors)}"
        super().__init__(error_msg)
        self.error_code = "INTERVIEW_RESPONSE_VALIDATION_FAILED"
        self.validation_errors = validation_errors


class InterviewResponseNotFoundException(InterviewException):
    """Raised when interview response is not found"""

    def __init__(self, response_id: str, interview_id: str):
        super().__init__(f"Response {response_id} not found in interview {interview_id}")
        self.error_code = "INTERVIEW_RESPONSE_NOT_FOUND"


class InterviewResponseIncompleteException(InterviewException):
    """Raised when trying to analyze incomplete response"""

    def __init__(self, response_id: str):
        super().__init__(f"Response {response_id} is incomplete and cannot be analyzed")
        self.error_code = "INTERVIEW_RESPONSE_INCOMPLETE"


# Membership and Access Control Exceptions
class InterviewMembershipAccessException(InterviewException):
    """Raised when membership level doesn't allow interview access"""

    def __init__(self, interview_type: str, required_level: str, current_level: str):
        super().__init__(
            f"Interview type '{interview_type}' requires '{required_level}' membership, but user has '{current_level}'")
        self.error_code = "INTERVIEW_MEMBERSHIP_ACCESS_DENIED"
        self.required_level = required_level
        self.current_level = current_level


class InterviewSessionLimitExceededException(InterviewException):
    """Raised when membership session limit is exceeded"""

    def __init__(self, membership_level: str, limit: int):
        super().__init__(f"Interview session limit ({limit}) exceeded for '{membership_level}' membership")
        self.error_code = "INTERVIEW_SESSION_LIMIT_EXCEEDED"
        self.limit = limit


class InterviewAIFeatureAccessException(InterviewException):
    """Raised when membership doesn't allow AI features"""

    def __init__(self, membership_level: str):
        super().__init__(f"AI features not available for '{membership_level}' membership")
        self.error_code = "INTERVIEW_AI_FEATURE_ACCESS_DENIED"


class InterviewExpertReviewAccessException(InterviewException):
    """Raised when membership doesn't allow expert review"""

    def __init__(self, membership_level: str):
        super().__init__(f"Expert review not available for '{membership_level}' membership")
        self.error_code = "INTERVIEW_EXPERT_REVIEW_ACCESS_DENIED"


# Template and Configuration Exceptions
class InterviewTemplateNotFoundException(InterviewException):
    """Raised when interview template is not found"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INTERVIEW_TEMPLATE_NOT_FOUND"


class InterviewTemplateQuestionNotFoundException(InterviewException):
    """Raised when interview template question is not found"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INTERVIEW_TEMPLATE_QUESTION_NOT_FOUND"


class InterviewTemplateSectionNotFoundException(InterviewException):
    """Raised when interview template section is not found"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INTERVIEW_TEMPLATE_SECTION_NOT_FOUND"


class InterviewTemplateNotFoundError(InterviewTemplateNotFoundException):
    """Alias for InterviewTemplateNotFoundException for backward compatibility"""
    pass


class InterviewTemplateValidationException(InterviewException):
    """Raised when interview template validation fails"""

    def __init__(self, template_id: str, validation_errors: list):
        error_msg = f"Template {template_id} validation failed: {', '.join(validation_errors)}"
        super().__init__(error_msg)
        self.error_code = "INTERVIEW_TEMPLATE_VALIDATION_FAILED"
        self.validation_errors = validation_errors


class InterviewTemplateValidationError(InterviewTemplateValidationException):
    """Alias for InterviewTemplateValidationException for backward compatibility"""
    pass


class InterviewTemplateInactiveException(InterviewException):
    """Raised when trying to use inactive template"""

    def __init__(self, template_id: str):
        super().__init__(f"Interview template {template_id} is inactive")
        self.error_code = "INTERVIEW_TEMPLATE_INACTIVE"


class InterviewTemplateDependencyError(InterviewException):
    """Raised when template dependency issues occur"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INTERVIEW_TEMPLATE_DEPENDENCY_ERROR"


class InvalidTemplateStateException(InterviewException):
    """Raised when template operation is invalid for current state"""

    def __init__(self, message: str):
        super().__init__(message)
        self.error_code = "INVALID_TEMPLATE_STATE"


class TemplateInUseException(InterviewException):
    """Raised when trying to delete a template that is in use"""

    def __init__(self, template_id: str, message: Optional[str] = None):
        default_message = f"Template {template_id} is currently in use and cannot be deleted"
        super().__init__(message or default_message)
        self.error_code = "TEMPLATE_IN_USE"
        self.template_id = template_id


# Business Rule Exceptions
class InterviewBusinessRuleViolationException(InterviewException):
    """Raised when interview business rule is violated"""

    def __init__(self, rule_name: str, violation_details: str):
        super().__init__(f"Business rule '{rule_name}' violated: {violation_details}")
        self.error_code = "INTERVIEW_BUSINESS_RULE_VIOLATION"
        self.rule_name = rule_name


class InterviewConcurrencyException(InterviewException):
    """Raised when interview concurrency rules are violated"""

    def __init__(self, candidate_id: str, active_interview_id: str):
        super().__init__(f"Candidate {candidate_id} already has active interview {active_interview_id}")
        self.error_code = "INTERVIEW_CONCURRENCY_VIOLATION"


class InterviewTimeoutException(InterviewException):
    """Raised when interview session times out"""

    def __init__(self, interview_id: str, timeout_minutes: int):
        super().__init__(f"Interview {interview_id} timed out after {timeout_minutes} minutes")
        self.error_code = "INTERVIEW_SESSION_TIMEOUT"


# EU Compliance Exceptions
class InterviewDataPrivacyException(InterviewException):
    """Raised when interview data privacy rules are violated"""

    def __init__(self, violation_type: str, details: str):
        super().__init__(f"Data privacy violation ({violation_type}): {details}")
        self.error_code = "INTERVIEW_DATA_PRIVACY_VIOLATION"


class InterviewGDPRComplianceException(InterviewException):
    """Raised when GDPR compliance rules are violated"""

    def __init__(self, compliance_issue: str):
        super().__init__(f"GDPR compliance issue: {compliance_issue}")
        self.error_code = "INTERVIEW_GDPR_COMPLIANCE_VIOLATION"


class InterviewConsentRequiredException(InterviewException):
    """Raised when user consent is required but not provided"""

    def __init__(self, consent_type: str):
        super().__init__(f"User consent required for: {consent_type}")
        self.error_code = "INTERVIEW_CONSENT_REQUIRED"
