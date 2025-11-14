from enum import Enum


class CommentReviewStatus(str, Enum):
    """Review status of a comment"""
    REVIEWED = "reviewed"  # Comment has been reviewed
    PENDING = "pending"  # Comment is pending review
