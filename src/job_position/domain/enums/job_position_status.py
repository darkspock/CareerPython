import enum


class JobPositionStatusEnum(enum.Enum):
    """Status enum for job positions"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"
