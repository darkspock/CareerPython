"""JobPositionStage repository implementation"""
from typing import List, Optional

from sqlalchemy.orm import Session

from core.database import SQLAlchemyDatabase
from src.company_bc.job_position.domain.entities.job_position_stage import JobPositionStage
from src.company_bc.job_position.domain.infrastructure.job_position_stage_repository_interface import \
    JobPositionStageRepositoryInterface
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_stage_id import JobPositionStageId
from src.company_bc.job_position.infrastructure.models.job_position_stage_model import JobPositionStageModel
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


class JobPositionStageRepository(JobPositionStageRepositoryInterface):
    """SQLAlchemy implementation of JobPositionStageRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def save(self, job_position_stage: JobPositionStage) -> None:
        """Save a job position stage"""
        session = self._get_session()
        model = session.query(JobPositionStageModel).filter_by(id=job_position_stage.id.value).first()

        if model:
            # Update existing
            model.job_position_id = job_position_stage.job_position_id.value
            model.phase_id = job_position_stage.phase_id.value if job_position_stage.phase_id else None
            model.workflow_id = job_position_stage.workflow_id.value if job_position_stage.workflow_id else None
            model.stage_id = job_position_stage.stage_id.value if job_position_stage.stage_id else None
            model.started_at = job_position_stage.started_at
            model.completed_at = job_position_stage.completed_at
            model.deadline = job_position_stage.deadline
            model.estimated_cost = job_position_stage.estimated_cost
            model.actual_cost = job_position_stage.actual_cost
            model.comments = job_position_stage.comments
            model.data = job_position_stage.data
            model.updated_at = job_position_stage.updated_at
        else:
            # Create new
            model = JobPositionStageModel(
                id=job_position_stage.id.value,
                job_position_id=job_position_stage.job_position_id.value,
                phase_id=job_position_stage.phase_id.value if job_position_stage.phase_id else None,
                workflow_id=job_position_stage.workflow_id.value if job_position_stage.workflow_id else None,
                stage_id=job_position_stage.stage_id.value if job_position_stage.stage_id else None,
                started_at=job_position_stage.started_at,
                completed_at=job_position_stage.completed_at,
                deadline=job_position_stage.deadline,
                estimated_cost=job_position_stage.estimated_cost,
                actual_cost=job_position_stage.actual_cost,
                comments=job_position_stage.comments,
                data=job_position_stage.data,
                created_at=job_position_stage.created_at,
                updated_at=job_position_stage.updated_at
            )
            session.add(model)

        session.commit()

    def get_by_id(self, id: JobPositionStageId) -> Optional[JobPositionStage]:
        """Get job position stage by ID"""
        session = self._get_session()
        model = session.query(JobPositionStageModel).filter_by(id=id.value).first()
        return self._to_domain(model) if model else None

    def list_by_job_position(
            self,
            job_position_id: JobPositionId
    ) -> List[JobPositionStage]:
        """Get all stages for a job position, ordered by started_at"""
        session = self._get_session()
        models = (
            session.query(JobPositionStageModel)
            .filter_by(job_position_id=job_position_id.value)
            .order_by(JobPositionStageModel.started_at.asc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def list_by_phase(self, phase_id: PhaseId) -> List[JobPositionStage]:
        """Get all stages for a specific phase"""
        session = self._get_session()
        models = (
            session.query(JobPositionStageModel)
            .filter_by(phase_id=phase_id.value)
            .order_by(JobPositionStageModel.started_at.desc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def get_current_by_job_position(
            self,
            job_position_id: JobPositionId
    ) -> Optional[JobPositionStage]:
        """Get the current (most recent uncompleted) stage for a job position"""
        session = self._get_session()
        model = (
            session.query(JobPositionStageModel)
            .filter_by(
                job_position_id=job_position_id.value,
                completed_at=None
            )
            .order_by(JobPositionStageModel.started_at.desc())
            .first()
        )
        return self._to_domain(model) if model else None

    def delete(self, id: JobPositionStageId) -> None:
        """Delete a job position stage"""
        session = self._get_session()
        model = session.query(JobPositionStageModel).filter_by(id=id.value).first()
        if model:
            session.delete(model)
            session.commit()

    def _to_domain(self, model: JobPositionStageModel) -> JobPositionStage:
        """Convert model to domain entity"""
        from src.company_bc.job_position.domain.value_objects.job_position_stage_id import JobPositionStageId
        from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
        from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
        from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
        from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId

        return JobPositionStage(
            id=JobPositionStageId.from_string(model.id),
            job_position_id=JobPositionId.from_string(model.job_position_id),
            phase_id=PhaseId.from_string(model.phase_id) if model.phase_id else None,
            workflow_id=WorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            stage_id=WorkflowStageId.from_string(model.stage_id) if model.stage_id else None,
            started_at=model.started_at,
            completed_at=model.completed_at,
            deadline=model.deadline,
            estimated_cost=model.estimated_cost,
            actual_cost=model.actual_cost,
            comments=model.comments,
            data=model.data,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
