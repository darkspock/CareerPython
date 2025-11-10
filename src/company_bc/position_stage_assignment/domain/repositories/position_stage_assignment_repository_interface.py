"""Position stage assignment repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.company_bc.position_stage_assignment.domain.entities import PositionStageAssignment
from src.company_bc.position_stage_assignment.domain.value_objects import PositionStageAssignmentId


class PositionStageAssignmentRepositoryInterface(ABC):
    """Repository interface for position stage assignments"""

    @abstractmethod
    def save(self, assignment: PositionStageAssignment) -> PositionStageAssignment:
        """Save or update a position stage assignment"""
        pass

    @abstractmethod
    def get_by_id(self, id: PositionStageAssignmentId) -> Optional[PositionStageAssignment]:
        """Get assignment by ID"""
        pass

    @abstractmethod
    def get_by_position_and_stage(self, position_id: str, stage_id: str) -> Optional[PositionStageAssignment]:
        """Get assignment for a specific position and stage"""
        pass

    @abstractmethod
    def list_by_position(self, position_id: str) -> List[PositionStageAssignment]:
        """Get all assignments for a position"""
        pass

    @abstractmethod
    def list_by_stage(self, stage_id: str) -> List[PositionStageAssignment]:
        """Get all assignments for a stage"""
        pass

    @abstractmethod
    def get_assigned_users(self, position_id: str, stage_id: str) -> List[str]:
        """Get assigned user IDs for a position-stage combination"""
        pass

    @abstractmethod
    def list_by_user(self, user_id: str) -> List[PositionStageAssignment]:
        """Get all assignments where a user is assigned"""
        pass

    @abstractmethod
    def delete(self, id: PositionStageAssignmentId) -> bool:
        """Delete an assignment"""
        pass

    @abstractmethod
    def delete_by_position(self, position_id: str) -> int:
        """Delete all assignments for a position - returns count deleted"""
        pass

    @abstractmethod
    def delete_by_stage(self, stage_id: str) -> int:
        """Delete all assignments for a stage - returns count deleted"""
        pass
