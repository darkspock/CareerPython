from enum import Enum


class InvitationStatus(str, Enum):
    """Status of a candidate invitation"""
    PENDING = "pending"  # Invitation sent, awaiting response
    ACCEPTED = "accepted"  # User accepted the invitation
    REJECTED = "rejected"  # User rejected the invitation
    EXPIRED = "expired"  # Invitation expired
