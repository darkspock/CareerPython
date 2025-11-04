from enum import Enum


class CommentVisibilityEnum(str, Enum):
    """Visibility level of a comment on a job position"""
    PRIVATE = "private"  # Only visible to company users
    SHARED_WITH_CANDIDATE = "shared_with_candidate"  # Visible to candidate (optional for JobPosition)

