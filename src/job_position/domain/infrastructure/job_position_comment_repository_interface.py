"""Job Position Comment Repository Interface."""
from abc import ABC, abstractmethod
from typing import Optional, List

from src.job_position.domain.entities.job_position_comment import JobPositionComment
from src.job_position.domain.value_objects import JobPositionCommentId, JobPositionId


class JobPositionCommentRepositoryInterface(ABC):
    """Job Position Comment repository interface"""

    @abstractmethod
    def save(self, comment: JobPositionComment) -> None:
        """
        Save or update a comment
        
        Args:
            comment: JobPositionComment entity to save
        """
        pass

    @abstractmethod
    def get_by_id(self, comment_id: JobPositionCommentId) -> Optional[JobPositionComment]:
        """
        Get a comment by ID
        
        Args:
            comment_id: ID of the comment to retrieve
            
        Returns:
            Optional[JobPositionComment]: Comment if found, None otherwise
        """
        pass

    @abstractmethod
    def list_by_job_position(
        self,
        job_position_id: JobPositionId
    ) -> List[JobPositionComment]:
        """
        List all comments for a job position
        
        Args:
            job_position_id: ID of the job position
            
        Returns:
            List[JobPositionComment]: All comments for the job position (ordered by created_at DESC)
        """
        pass

    @abstractmethod
    def list_by_stage_and_global(
        self,
        job_position_id: JobPositionId,
        stage_id: Optional[str]
    ) -> List[JobPositionComment]:
        """
        List comments for a job position in a specific stage PLUS all global comments
        
        This is the key method for displaying "current comments" - it returns:
        - Comments where stage_id matches the provided stage_id
        - Comments where stage_id is NULL (global comments)
        
        SQL equivalent:
        WHERE job_position_id = ? AND (stage_id = ? OR stage_id IS NULL)
        
        Args:
            job_position_id: ID of the job position
            stage_id: ID of the stage (can be None to get only global comments)
            
        Returns:
            List[JobPositionComment]: Stage-specific + global comments (ordered by created_at DESC)
        """
        pass

    @abstractmethod
    def list_global_only(
        self,
        job_position_id: JobPositionId
    ) -> List[JobPositionComment]:
        """
        List only global comments for a job position
        
        Global comments are those where stage_id is NULL
        
        Args:
            job_position_id: ID of the job position
            
        Returns:
            List[JobPositionComment]: Only global comments (ordered by created_at DESC)
        """
        pass

    @abstractmethod
    def delete(self, comment_id: JobPositionCommentId) -> None:
        """
        Delete a comment
        
        Args:
            comment_id: ID of the comment to delete
        """
        pass

    @abstractmethod
    def count_pending_by_job_position(
        self,
        job_position_id: JobPositionId
    ) -> int:
        """
        Count pending comments for a job position
        
        SQL equivalent:
        WHERE job_position_id = ? AND review_status = 'pending'
        
        Args:
            job_position_id: ID of the job position
            
        Returns:
            int: Number of pending comments
        """
        pass

