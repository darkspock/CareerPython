from enum import Enum


class InAppNotificationType(str, Enum):
    """Types of in-app notifications"""
    # Candidate related
    NEW_APPLICATION = "NEW_APPLICATION"
    APPLICATION_STATUS_CHANGED = "APPLICATION_STATUS_CHANGED"
    CANDIDATE_MOVED_STAGE = "CANDIDATE_MOVED_STAGE"

    # Interview related
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEW_REMINDER = "INTERVIEW_REMINDER"
    INTERVIEW_COMPLETED = "INTERVIEW_COMPLETED"
    INTERVIEW_CANCELLED = "INTERVIEW_CANCELLED"

    # Comment/Activity related
    NEW_COMMENT = "NEW_COMMENT"
    MENTION = "MENTION"

    # System related
    SYSTEM_ALERT = "SYSTEM_ALERT"
    TASK_ASSIGNED = "TASK_ASSIGNED"

    # Generic
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class InAppNotificationPriority(str, Enum):
    """Priority levels for notifications"""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"
