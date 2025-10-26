"""Position stage assignment domain entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.position_stage_assignment.domain.value_objects import PositionStageAssignmentId
from src.position_stage_assignment.domain.exceptions import PositionStageAssignmentValidationError


@dataclass
class PositionStageAssignment:
    """Position stage assignment entity - assigns users to specific stages for a position"""
    id: PositionStageAssignmentId
    position_id: str
    stage_id: str
    assigned_user_ids: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def add_user(self, user_id: str) -> None:
        """Add a user to this stage assignment"""
        if not user_id or not user_id.strip():
            raise PositionStageAssignmentValidationError("User ID cannot be empty")

        user_id_clean = user_id.strip()
        if user_id_clean not in self.assigned_user_ids:
            self.assigned_user_ids.append(user_id_clean)
            self.updated_at = datetime.utcnow()

    def remove_user(self, user_id: str) -> None:
        """Remove a user from this stage assignment"""
        if user_id in self.assigned_user_ids:
            self.assigned_user_ids.remove(user_id)
            self.updated_at = datetime.utcnow()

    def replace_users(self, user_ids: List[str]) -> None:
        """Replace all assigned users with a new list"""
        # Validate all user IDs
        cleaned_ids = []
        for user_id in user_ids:
            if not user_id or not user_id.strip():
                raise PositionStageAssignmentValidationError("User ID cannot be empty")
            cleaned_id = user_id.strip()
            if cleaned_id not in cleaned_ids:  # Remove duplicates
                cleaned_ids.append(cleaned_id)

        self.assigned_user_ids = cleaned_ids
        self.updated_at = datetime.utcnow()

    def has_user(self, user_id: str) -> bool:
        """Check if a user is assigned to this stage"""
        return user_id in self.assigned_user_ids

    def get_user_count(self) -> int:
        """Get the number of assigned users"""
        return len(self.assigned_user_ids)

    @staticmethod
    def create(
            id: PositionStageAssignmentId,
            position_id: str,
            stage_id: str,
            assigned_user_ids: Optional[List[str]] = None
    ) -> 'PositionStageAssignment':
        """Create a new position stage assignment"""
        # Validate required fields
        if not position_id or not position_id.strip():
            raise PositionStageAssignmentValidationError("Position ID is required")

        if not stage_id or not stage_id.strip():
            raise PositionStageAssignmentValidationError("Stage ID is required")

        # Clean and deduplicate user IDs
        cleaned_user_ids = []
        if assigned_user_ids:
            for user_id in assigned_user_ids:
                if user_id and user_id.strip():
                    cleaned_id = user_id.strip()
                    if cleaned_id not in cleaned_user_ids:
                        cleaned_user_ids.append(cleaned_id)

        now = datetime.utcnow()

        return PositionStageAssignment(
            id=id,
            position_id=position_id.strip(),
            stage_id=stage_id.strip(),
            assigned_user_ids=cleaned_user_ids,
            created_at=now,
            updated_at=now
        )

    @classmethod
    def _from_repository(
            cls,
            id: PositionStageAssignmentId,
            position_id: str,
            stage_id: str,
            assigned_user_ids: List[str],
            created_at: datetime,
            updated_at: datetime
    ) -> 'PositionStageAssignment':
        """Create from repository - only for repositories to use"""
        return cls(
            id=id,
            position_id=position_id,
            stage_id=stage_id,
            assigned_user_ids=assigned_user_ids or [],
            created_at=created_at,
            updated_at=updated_at
        )
