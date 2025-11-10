"""Position stage assignment repository implementation"""
from typing import List, Optional

from core.database import DatabaseInterface
from src.company_bc.position_stage_assignment.domain import (
    PositionStageAssignment,
    PositionStageAssignmentId,
    PositionStageAssignmentRepositoryInterface
)
from src.company_bc.position_stage_assignment.infrastructure.models import PositionStageAssignmentModel


class PositionStageAssignmentRepository(PositionStageAssignmentRepositoryInterface):
    """Repository implementation for position stage assignments"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, assignment: PositionStageAssignment) -> PositionStageAssignment:
        """Save or update a position stage assignment"""
        with self.database.get_session() as session:
            model = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.id == assignment.id.value
            ).first()

            if model:
                # Update existing
                self._update_model_from_entity(model, assignment)
            else:
                # Create new
                model = self._create_model_from_entity(assignment)
                session.add(model)

            session.commit()
            session.refresh(model)

            return self._create_entity_from_model(model)

    def get_by_id(self, id: PositionStageAssignmentId) -> Optional[PositionStageAssignment]:
        """Get assignment by ID"""
        with self.database.get_session() as session:
            model = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.id == id.value
            ).first()

            if not model:
                return None

            return self._create_entity_from_model(model)

    def get_by_position_and_stage(self, position_id: str, stage_id: str) -> Optional[PositionStageAssignment]:
        """Get assignment for a specific position and stage"""
        with self.database.get_session() as session:
            model = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.position_id == position_id,
                PositionStageAssignmentModel.stage_id == stage_id
            ).first()

            if not model:
                return None

            return self._create_entity_from_model(model)

    def list_by_position(self, position_id: str) -> List[PositionStageAssignment]:
        """Get all assignments for a position"""
        with self.database.get_session() as session:
            models = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.position_id == position_id
            ).all()

            return [self._create_entity_from_model(model) for model in models]

    def list_by_stage(self, stage_id: str) -> List[PositionStageAssignment]:
        """Get all assignments for a stage"""
        with self.database.get_session() as session:
            models = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.stage_id == stage_id
            ).all()

            return [self._create_entity_from_model(model) for model in models]

    def get_assigned_users(self, position_id: str, stage_id: str) -> List[str]:
        """Get assigned user IDs for a position-stage combination"""
        assignment = self.get_by_position_and_stage(position_id, stage_id)
        if assignment:
            return [uid.value for uid in assignment.assigned_user_ids]
        return []

    def list_by_user(self, user_id: str) -> List[PositionStageAssignment]:
        """Get all assignments where a user is assigned"""
        with self.database.get_session() as session:
            # Query all assignments where the user_id is in the assigned_user_ids array
            models = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.assigned_user_ids.contains([user_id])
            ).all()

            return [self._create_entity_from_model(model) for model in models]

    def delete(self, id: PositionStageAssignmentId) -> bool:
        """Delete an assignment"""
        with self.database.get_session() as session:
            model = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.id == id.value
            ).first()

            if not model:
                return False

            session.delete(model)
            session.commit()
            return True

    def delete_by_position(self, position_id: str) -> int:
        """Delete all assignments for a position - returns count deleted"""
        with self.database.get_session() as session:
            count = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.position_id == position_id
            ).delete()
            session.commit()
            return count

    def delete_by_stage(self, stage_id: str) -> int:
        """Delete all assignments for a stage - returns count deleted"""
        with self.database.get_session() as session:
            count = session.query(PositionStageAssignmentModel).filter(
                PositionStageAssignmentModel.stage_id == stage_id
            ).delete()
            session.commit()
            return count

    def _create_entity_from_model(self, model: PositionStageAssignmentModel) -> PositionStageAssignment:
        """Convert model to entity"""
        from datetime import datetime
        return PositionStageAssignment._from_repository(
            id=PositionStageAssignmentId.from_string(model.id or ""),
            position_id=model.position_id or "",
            stage_id=model.stage_id or "",
            assigned_user_ids=model.assigned_user_ids or [],
            created_at=model.created_at or datetime.utcnow(),
            updated_at=model.updated_at or datetime.utcnow()
        )

    def _create_model_from_entity(self, assignment: PositionStageAssignment) -> PositionStageAssignmentModel:
        """Create model from entity"""
        return PositionStageAssignmentModel(
            id=assignment.id.value,
            position_id=assignment.position_id.value,
            stage_id=assignment.stage_id.value,
            assigned_user_ids=[uid.value for uid in assignment.assigned_user_ids],
            created_at=assignment.created_at,
            updated_at=assignment.updated_at
        )

    def _update_model_from_entity(self, model: PositionStageAssignmentModel, assignment: PositionStageAssignment) -> None:
        """Update model with entity data"""
        model.assigned_user_ids = [uid.value for uid in assignment.assigned_user_ids]
        model.updated_at = assignment.updated_at
