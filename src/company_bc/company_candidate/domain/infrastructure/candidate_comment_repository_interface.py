from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.candidate_comment import CandidateComment
from ..value_objects import CandidateCommentId, CompanyCandidateId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class CandidateCommentRepositoryInterface(ABC):
    """CandidateComment repository interface"""

    @abstractmethod
    def save(self, comment: CandidateComment) -> None:
        """Save or update a comment"""
        pass

    @abstractmethod
    def get_by_id(self, comment_id: CandidateCommentId) -> Optional[CandidateComment]:
        """Get a comment by ID"""
        pass

    @abstractmethod
    def list_by_company_candidate(
        self,
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateComment]:
        """List all comments for a company candidate"""
        pass

    @abstractmethod
    def list_by_stage(
        self,
        company_candidate_id: CompanyCandidateId,
        stage_id: WorkflowStageId
    ) -> List[CandidateComment]:
        """List all comments for a company candidate in a specific stage"""
        pass

    @abstractmethod
    def delete(self, comment_id: CandidateCommentId) -> None:
        """Delete a comment"""
        pass

    @abstractmethod
    def count_pending_by_company_candidate(
        self,
        company_candidate_id: CompanyCandidateId
    ) -> int:
        """Count pending comments for a company candidate"""
        pass

