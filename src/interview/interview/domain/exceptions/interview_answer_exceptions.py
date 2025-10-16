"""Interview Answer domain exceptions"""


class InterviewAnswerDomainException(Exception):
    """Base exception for interview answer domain"""
    pass


class InterviewAnswerNotFoundException(InterviewAnswerDomainException):
    """Exception raised when an interview answer is not found"""
    pass


class InterviewAnswerAlreadyScoredException(InterviewAnswerDomainException):
    """Exception raised when trying to modify an already scored answer"""
    pass


class InterviewAnswerInvalidScoreException(InterviewAnswerDomainException):
    """Exception raised when an invalid score is provided"""
    pass


class InterviewAnswerEmptyAnswerException(InterviewAnswerDomainException):
    """Exception raised when trying to save an empty answer"""
    pass


class InterviewAnswerAlreadyAnsweredException(InterviewAnswerDomainException):
    """Exception raised when trying to answer an already answered question"""
    pass
