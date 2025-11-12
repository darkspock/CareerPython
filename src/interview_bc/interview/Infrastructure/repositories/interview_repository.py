"""Interview repository implementation"""
from datetime import datetime
from typing import Optional, List

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.interview_bc.interview.Infrastructure.models.interview_model import InterviewModel
from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.enums.interview_enums import InterviewStatusEnum, InterviewTypeEnum
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyInterviewRepository(InterviewRepositoryInterface):
    """SQLAlchemy implementation of Interview repository"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, InterviewModel)

    def _to_domain(self, model: InterviewModel) -> Interview:
        """Convert model to domain entity"""
        job_position_id = None
        if model.job_position_id:
            job_position_id = JobPositionId.from_string(model.job_position_id)

        application_id = None
        if model.application_id:
            application_id = CandidateApplicationId.from_string(model.application_id)

        interview_template_id = None
        if model.interview_template_id:
            interview_template_id = InterviewTemplateId.from_string(model.interview_template_id)

        workflow_stage_id = None
        if model.workflow_stage_id:
            workflow_stage_id = WorkflowStageId.from_string(model.workflow_stage_id)

        interviewers_list = model.interviewers or []

        return Interview(
            id=InterviewId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            workflow_stage_id=workflow_stage_id,
            interview_type=model.interview_type,
            interview_mode=model.interview_mode,
            status=model.status,
            title=model.title,
            description=model.description,
            scheduled_at=model.scheduled_at,
            started_at=model.started_at,
            finished_at=model.finished_at,
            duration_minutes=model.duration_minutes,
            interviewers=interviewers_list,
            interviewer_notes=model.interviewer_notes,
            candidate_notes=model.candidate_notes,
            score=model.score,
            feedback=model.feedback,
            free_answers=model.free_answers,
            link_token=model.link_token,
            link_expires_at=model.link_expires_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, domain: Interview) -> InterviewModel:
        """Convert domain entity to model"""
        job_position_id = None
        if domain.job_position_id:
            job_position_id = domain.job_position_id.value

        application_id = None
        if domain.application_id:
            application_id = domain.application_id.value

        interview_template_id = None
        if domain.interview_template_id:
            interview_template_id = domain.interview_template_id.value

        workflow_stage_id = None
        if domain.workflow_stage_id:
            workflow_stage_id = str(domain.workflow_stage_id)

        return InterviewModel(
            id=domain.id.value,
            candidate_id=domain.candidate_id.value,
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            workflow_stage_id=workflow_stage_id,
            interview_type=domain.interview_type,
            interview_mode=domain.interview_mode,
            status=domain.status,
            title=domain.title,
            description=domain.description,
            scheduled_at=domain.scheduled_at,
            started_at=domain.started_at,
            finished_at=domain.finished_at,
            duration_minutes=domain.duration_minutes,
            interviewers=domain.interviewers,
            interviewer_notes=domain.interviewer_notes,
            candidate_notes=domain.candidate_notes,
            score=domain.score,
            feedback=domain.feedback,
            free_answers=domain.free_answers,
            link_token=domain.link_token,
            link_expires_at=domain.link_expires_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    def create(self, interview: Interview) -> Interview:
        """Create a new interview"""
        model = self._to_model(interview)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, interview_id: str) -> Optional[Interview]:
        """Get interview by ID"""
        with self.database.get_session() as session:
            model = session.query(InterviewModel).filter(InterviewModel.id == interview_id).first()
            if model:
                return self._to_domain(model)
            return None

    def update(self, interview: Interview) -> Interview:
        """Update an existing interview"""
        with self.database.get_session() as session:
            model = session.query(InterviewModel).filter(InterviewModel.id == interview.id.value).first()
            if model:
                # Update all fields from the entity
                model.candidate_id = interview.candidate_id.value
                model.job_position_id = interview.job_position_id.value if interview.job_position_id else None
                model.application_id = interview.application_id.value if interview.application_id else None
                model.interview_template_id = interview.interview_template_id.value if interview.interview_template_id else None
                model.workflow_stage_id = str(interview.workflow_stage_id) if interview.workflow_stage_id else None
                model.interview_type = interview.interview_type
                model.status = interview.status
                model.title = interview.title
                model.description = interview.description
                model.scheduled_at = interview.scheduled_at
                model.started_at = interview.started_at
                model.finished_at = interview.finished_at
                model.duration_minutes = interview.duration_minutes
                model.interviewers = interview.interviewers
                model.interviewer_notes = interview.interviewer_notes
                model.candidate_notes = interview.candidate_notes
                model.score = interview.score
                model.feedback = interview.feedback
                model.free_answers = interview.free_answers
                model.link_token = interview.link_token
                model.link_expires_at = interview.link_expires_at
                model.updated_at = interview.updated_at or datetime.now()
                model.updated_by = interview.updated_by

                session.commit()
                session.refresh(model)
                return self._to_domain(model)
            raise ValueError(f"Interview with id {interview.id.value} not found")

    def delete(self, id: InterviewId) -> bool:
        """Delete an interview"""
        return self.base_repo.delete(id)

    def get_by_candidate_id(self, candidate_id: str) -> List[Interview]:
        """Get all interviews for a candidate"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_job_position_id(self, job_position_id: str) -> List[Interview]:
        """Get all interviews for a job position"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.job_position_id == job_position_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_application_id(self, application_id: str) -> List[Interview]:
        """Get all interviews for a candidate application"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.application_id == application_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_status(self, status: InterviewStatusEnum) -> List[Interview]:
        """Get interviews by status"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.status == status
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_interview_type(self, interview_type: InterviewTypeEnum) -> List[Interview]:
        """Get interviews by type"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.interview_type == interview_type
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_scheduled_interviews(self, from_date: datetime, to_date: datetime) -> List[Interview]:
        """Get scheduled interviews within date range"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.scheduled_at.between(from_date, to_date)
            ).order_by(InterviewModel.scheduled_at).all()
            return [self._to_domain(model) for model in models]

    def get_interviews_by_candidate_and_job_position(
            self,
            candidate_id: str,
            job_position_id: str
    ) -> List[Interview]:
        """Get interviews for specific candidate and job position"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id,
                InterviewModel.job_position_id == job_position_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def find_by_filters(
            self,
            candidate_id: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            limit: int = 50,
            offset: int = 0
    ) -> List[Interview]:
        """Find interviews by multiple filters"""
        with self.database.get_session() as session:
            query = session.query(InterviewModel)

            if candidate_id:
                query = query.filter(InterviewModel.candidate_id == candidate_id)
            if job_position_id:
                query = query.filter(InterviewModel.job_position_id == job_position_id)
            if interview_type:
                query = query.filter(InterviewModel.interview_type == interview_type)
            if status:
                query = query.filter(InterviewModel.status == status)
            if created_by:
                query = query.filter(InterviewModel.created_by == created_by)
            if from_date:
                query = query.filter(InterviewModel.created_at >= from_date)
            if to_date:
                query = query.filter(InterviewModel.created_at <= to_date)

            query = query.order_by(InterviewModel.created_at.desc())
            query = query.offset(offset).limit(limit)

            models = query.all()
            return [self._to_domain(model) for model in models]

    def count_by_status(self, status: InterviewStatusEnum) -> int:
        """Count interviews by status"""
        with self.database.get_session() as session:
            return session.query(InterviewModel).filter(InterviewModel.status == status).count()

    def count_by_candidate(self, candidate_id: str) -> int:
        """Count interviews for a candidate"""
        with self.database.get_session() as session:
            return session.query(InterviewModel).filter(InterviewModel.candidate_id == candidate_id).count()

    def get_pending_interviews_by_candidate_and_stage(
            self,
            candidate_id: str,
            workflow_stage_id: str
    ) -> List[Interview]:
        """Get pending interviews for a candidate in a specific workflow stage"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id,
                InterviewModel.workflow_stage_id == workflow_stage_id,
                InterviewModel.status == InterviewStatusEnum.ENABLED  # ENABLED = "PENDING" (see enum definition)
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_token(self, interview_id: str, token: str) -> Optional[Interview]:
        """Get interview by ID and token for secure link access"""
        with self.database.get_session() as session:
            model = session.query(InterviewModel).filter(
                InterviewModel.id == interview_id,
                InterviewModel.link_token == token
            ).first()
            if not model:
                return None
            interview = self._to_domain(model)
            # Validate that the link is still valid
            if not interview.is_link_valid():
                return None
            return interview
