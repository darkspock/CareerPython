"""Activity Type Enum for Job Position activities."""
from enum import Enum


class ActivityTypeEnum(str, Enum):
    """
    Enum for different types of activities that can be performed on a job position.

    Each value represents a specific type of interaction or change.
    """
    CREATED = "created"
    EDITED = "edited"
    STAGE_MOVED = "stage_moved"
    STATUS_CHANGED = "status_changed"
    COMMENT_ADDED = "comment_added"
