"""Enums for CompanyCandidate domain"""
from .company_candidate_status import CompanyCandidateStatus
from .ownership_status import OwnershipStatus
from .invitation_status import InvitationStatus
from .candidate_priority import CandidatePriority
from .comment_visibility import CommentVisibility
from .access_action import AccessAction
from .comment_review_status import CommentReviewStatus

__all__ = [
    "CompanyCandidateStatus",
    "OwnershipStatus",
    "InvitationStatus",
    "CandidatePriority",
    "CommentVisibility",
    "AccessAction",
    "CommentReviewStatus",
]
