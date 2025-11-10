from enum import Enum


class ReviewStatusEnum(str, Enum):
    """Review status of a candidate review"""
    PENDING = "pending"  # Review is pending
    REVIEWED = "reviewed"  # Review has been reviewed

