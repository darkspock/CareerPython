from enum import Enum


class CommentVisibility(str, Enum):
    """Visibility level of a comment on a candidate"""
    PRIVATE = "private"  # Only visible to company users
    SHARED_WITH_CANDIDATE = "shared_with_candidate"  # Visible to candidate
