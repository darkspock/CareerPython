"""Repository interface for CandidateReview"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.candidate_review.domain.entities.candidate_review import CandidateReview
from src.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class CandidateReviewRepositoryInterface(ABC):
    """Interface for CandidateReview repository"""

    @abstractmethod
    def get_by_id(self, review_id: CandidateReviewId) -> Optional[CandidateReview]:
        """Get a review by ID"""
        pass

    @abstractmethod
    def get_by_company_candidate(
        self, 
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateReview]:
        """Get all reviews for a company candidate"""
        pass

    @abstractmethod
    def get_by_stage(
        self, 
        company_candidate_id: CompanyCandidateId, 
        stage_id: WorkflowStageId
    ) -> List[CandidateReview]:
        """Get all reviews for a specific stage"""
        pass

    @abstractmethod
    def get_global_reviews(
        self, 
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateReview]:
        """Get all global reviews (stage_id is None)"""
        pass

    @abstractmethod
    def create(self, review: CandidateReview) -> None:
        """Create a new review"""
        pass

    @abstractmethod
    def update(self, review: CandidateReview) -> None:
        """Update an existing review"""
        pass

    @abstractmethod
    def delete(self, review_id: CandidateReviewId) -> None:
        """Delete a review"""
        pass

