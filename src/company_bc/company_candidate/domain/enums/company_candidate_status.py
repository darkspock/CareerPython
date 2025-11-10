from enum import Enum


class CompanyCandidateStatus(str, Enum):
    """Status of the company-candidate relationship"""
    PENDING_INVITATION = "pending_invitation"  # Invitation sent, awaiting response
    PENDING_CONFIRMATION = "pending_confirmation"  # User exists, awaiting confirmation
    ACTIVE = "active"  # Active relationship
    REJECTED = "rejected"  # User rejected the invitation
    ARCHIVED = "archived"  # Relationship archived
