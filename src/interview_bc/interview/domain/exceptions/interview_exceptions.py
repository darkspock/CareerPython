"""Interview domain exceptions"""


class InterviewDomainException(Exception):
    """Base exception for Interview domain"""
    pass


class InterviewValidationError(InterviewDomainException):
    """Raised when interview data validation fails"""
    pass


class InterviewNotFoundException(InterviewDomainException):
    """Raised when interview is not found"""
    pass


class InterviewStateTransitionError(InterviewDomainException):
    """Raised when invalid state transition is attempted"""
    pass


class InterviewSchedulingError(InterviewDomainException):
    """Raised when interview scheduling fails"""
    pass


class InterviewAccessDeniedError(InterviewDomainException):
    """Raised when access to interview is denied"""
    pass


class InterviewAlreadyFinishedError(InterviewDomainException):
    """Raised when trying to modify a finished interview"""
    pass


class InterviewNotStartedError(InterviewDomainException):
    """Raised when trying to perform actions on non-started interview"""
    pass
