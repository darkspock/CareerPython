"""Exception classes for CompanyCandidate domain"""


class CompanyCandidateError(Exception):
    """Base exception for CompanyCandidate domain"""
    pass


class CompanyCandidateNotFoundError(CompanyCandidateError):
    """Raised when a company candidate is not found"""
    pass


class CompanyCandidateValidationError(CompanyCandidateError):
    """Raised when validation fails"""
    pass


class CompanyCandidateAlreadyExistsError(CompanyCandidateError):
    """Raised when trying to create a duplicate company-candidate relationship"""
    pass


class InvitationExpiredError(CompanyCandidateError):
    """Raised when attempting to use an expired invitation"""
    pass


class InvitationAlreadyProcessedError(CompanyCandidateError):
    """Raised when attempting to process an invitation that was already accepted/rejected"""
    pass


class InvalidOwnershipTransitionError(CompanyCandidateError):
    """Raised when attempting an invalid ownership status transition"""
    pass
