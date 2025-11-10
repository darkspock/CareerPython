from enum import Enum


class CommentVisibility(str, Enum):
    """Visibility level of a comment on a candidate"""
    PRIVATE = "private"  # Only visible to the comment creator
    SHARED = "shared"    # Visible to all team members
    SHARED_WITH_CANDIDATE = "shared_with_candidate"  # Visible to candidate (future feature)
