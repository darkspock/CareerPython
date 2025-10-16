"""
Comprehensive domain exceptions for the AI Resume Enhancement Platform
"""

# AI-specific exceptions
from .ai_exceptions import (
    AIProcessingException,
    AIServiceUnavailableException,
    AIResponseParsingException,
    AITimeoutException,
    AIQuotaExceededException,
    AIContentValidationException,
    ResumeProcessingException,
    InterviewGenerationException,
    JobMatchingException,
    ResumeGenerationException
)
# Base exceptions
from .base import (
    DomainException,
    ValidationException,
    BusinessRuleException,
    EntityNotFoundException,
    AuthenticationException,
    AuthorizationException,
    ConcurrencyException,
    ExternalServiceException,
    ConfigurationException
)
# Candidate and resume exceptions
from .candidate_exceptions import (
    CandidateException,
    CandidateNotFoundException,
    CandidateValidationException,
    ResumeException,
    ResumeUploadException,
    InvalidResumeFormatException,
    ResumeSizeExceededException,
    ResumeExtractionException,
    ResumeDownloadException,
    ExperienceException,
    ExperienceValidationException,
    EducationException,
    EducationValidationException,
    ProjectException,
    ProjectValidationException,
    ProfileSectionException,
    ProfileIncompleteException as CandidateProfileIncompleteException
)
# Interview exceptions
from .interview_exceptions import (
    InterviewException,
    InterviewNotFoundException,
    InvalidInterviewStateException,
    InterviewAlreadyCompletedException,
    InterviewNotStartedException,
    InterviewTemplateException,
    InterviewTemplateNotFoundException,
    InterviewQuestionException,
    InterviewQuestionNotFoundException,
    InterviewAnswerException,
    InterviewAnswerValidationException,
    InterviewProgressException,
    InterviewSectionException,
    InterviewTimeoutException,
    InterviewConcurrencyException,
    InterviewDataInconsistencyException
)
# Job application exceptions
from .job_application_exceptions import (
    JobApplicationException,
    JobApplicationNotFoundException,
    JobApplicationLimitExceededException,
    JobDescriptionException,
    JobDescriptionValidationException,
    JobDescriptionTooShortException,
    JobDescriptionTooLongException,
    JobAnalysisException,
    CoverLetterGenerationException,
    ResumeCustomizationException,
    ApplicationHistoryException,
    DuplicateApplicationException,
    ApplicationStatusException
)
# Subscription and payment exceptions
from .subscription_exceptions import (
    SubscriptionException,
    SubscriptionLimitExceededException,
    SubscriptionExpiredException,
    SubscriptionNotActiveException,
    InvalidSubscriptionTierException,
    PaymentException,
    PaymentProcessingException,
    PaymentValidationException,
    InsufficientFundsException,
    PaymentMethodException,
    RefundException
)
# User and authentication exceptions
from .user_exceptions import (
    UserException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
    InvalidCredentialsException,
    PasswordValidationException,
    EmailValidationException,
    TokenException,
    InvalidTokenException,
    ExpiredTokenException,
    PasswordResetException,
    AccountLockedException,
    ProfileIncompleteException as UserProfileIncompleteException
)

__all__ = [
    # Base exceptions
    "DomainException",
    "ValidationException",
    "BusinessRuleException",
    "EntityNotFoundException",
    "AuthenticationException",
    "AuthorizationException",
    "ConcurrencyException",
    "ExternalServiceException",
    "ConfigurationException",

    # AI exceptions
    "AIProcessingException",
    "AIServiceUnavailableException",
    "AIResponseParsingException",
    "AITimeoutException",
    "AIQuotaExceededException",
    "AIContentValidationException",
    "ResumeProcessingException",
    "InterviewGenerationException",
    "JobMatchingException",
    "ResumeGenerationException",

    # Subscription exceptions
    "SubscriptionException",
    "SubscriptionLimitExceededException",
    "SubscriptionExpiredException",
    "SubscriptionNotActiveException",
    "InvalidSubscriptionTierException",
    "PaymentException",
    "PaymentProcessingException",
    "PaymentValidationException",
    "InsufficientFundsException",
    "PaymentMethodException",
    "RefundException",

    # User exceptions
    "UserException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "UserNotActiveException",
    "InvalidCredentialsException",
    "PasswordValidationException",
    "EmailValidationException",
    "TokenException",
    "InvalidTokenException",
    "ExpiredTokenException",
    "PasswordResetException",
    "AccountLockedException",
    "UserProfileIncompleteException",

    # Candidate exceptions
    "CandidateException",
    "CandidateNotFoundException",
    "CandidateValidationException",
    "ResumeException",
    "ResumeUploadException",
    "InvalidResumeFormatException",
    "ResumeSizeExceededException",
    "ResumeExtractionException",
    "ResumeDownloadException",
    "ExperienceException",
    "ExperienceValidationException",
    "EducationException",
    "EducationValidationException",
    "ProjectException",
    "ProjectValidationException",
    "ProfileSectionException",
    "CandidateProfileIncompleteException",

    # Interview exceptions
    "InterviewException",
    "InterviewNotFoundException",
    "InvalidInterviewStateException",
    "InterviewAlreadyCompletedException",
    "InterviewNotStartedException",
    "InterviewTemplateException",
    "InterviewTemplateNotFoundException",
    "InterviewQuestionException",
    "InterviewQuestionNotFoundException",
    "InterviewAnswerException",
    "InterviewAnswerValidationException",
    "InterviewProgressException",
    "InterviewSectionException",
    "InterviewTimeoutException",
    "InterviewConcurrencyException",
    "InterviewDataInconsistencyException",

    # Job application exceptions
    "JobApplicationException",
    "JobApplicationNotFoundException",
    "JobApplicationLimitExceededException",
    "JobDescriptionException",
    "JobDescriptionValidationException",
    "JobDescriptionTooShortException",
    "JobDescriptionTooLongException",
    "JobAnalysisException",
    "CoverLetterGenerationException",
    "ResumeCustomizationException",
    "ApplicationHistoryException",
    "DuplicateApplicationException",
    "ApplicationStatusException",
]
