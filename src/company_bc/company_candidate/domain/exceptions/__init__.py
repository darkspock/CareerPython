"""Exceptions for CompanyCandidate domain"""
from .company_candidate_exceptions import (
    CompanyCandidateError,
    CompanyCandidateNotFoundError,
    CompanyCandidateValidationError,
    CompanyCandidateAlreadyExistsError,
    InvitationExpiredError,
    InvitationAlreadyProcessedError,
    InvalidOwnershipTransitionError,
)

__all__ = [
    "CompanyCandidateError",
    "CompanyCandidateNotFoundError",
    "CompanyCandidateValidationError",
    "CompanyCandidateAlreadyExistsError",
    "InvitationExpiredError",
    "InvitationAlreadyProcessedError",
    "InvalidOwnershipTransitionError",
]
