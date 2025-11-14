import enum


class JobPositionStatusEnum(enum.Enum):
    """Status enum for job positions"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
