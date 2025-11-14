from dataclasses import dataclass

from src.framework.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class CandidateReviewId(BaseId):
    """Value object for CandidateReview ID"""
    value: str
