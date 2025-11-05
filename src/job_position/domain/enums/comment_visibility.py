from enum import Enum


class CommentVisibilityEnum(str, Enum):
    """Visibility level of a comment on a job position"""
    PRIVATE = "private"  # Only visible to the comment creator
    SHARED = "shared"    # Visible to all team members with access to the position

