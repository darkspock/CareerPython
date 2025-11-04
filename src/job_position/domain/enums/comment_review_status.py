from enum import Enum


class CommentReviewStatusEnum(str, Enum):
    """Review status of a comment on a job position"""
    REVIEWED = "reviewed"  # Comment has been reviewed
    PENDING = "pending"  # Comment is pending review

