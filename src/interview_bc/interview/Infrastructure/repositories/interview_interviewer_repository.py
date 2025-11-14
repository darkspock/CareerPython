"""Interview Interviewer repository implementation"""
from typing import Optional, List

from core.database import DatabaseInterface
from src.interview_bc.interview.domain.entities.interview_interviewer import InterviewInterviewer
from src.interview_bc.interview.domain.infrastructure.interview_interviewer_repository_interface import \
    InterviewInterviewerRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.interview_bc.interview.Infrastructure.models.interview_interviewer_model import InterviewInterviewerModel
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyInterviewInterviewerRepository(InterviewInterviewerRepositoryInterface):
    """SQLAlchemy implementation of Interview Interviewer repository"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, InterviewInterviewerModel)

    def _to_domain(self, model: InterviewInterviewerModel) -> InterviewInterviewer:
        """Convert model to domain entity"""
        return InterviewInterviewer(
            id=InterviewInterviewerId.from_string(model.id),
            interview_id=InterviewId.from_string(model.interview_id),
            user_id=UserId.from_string(model.user_id),
            name=model.name,
            is_external=model.is_external,
            invited_at=model.invited_at,
            accepted_at=model.accepted_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by
        )

    def _to_model(self, domain: InterviewInterviewer) -> InterviewInterviewerModel:
        """Convert domain entity to model"""
        return InterviewInterviewerModel(
            id=domain.id.value,
            interview_id=domain.interview_id.value,
            user_id=domain.user_id.value,
            name=domain.name,
            is_external=domain.is_external,
            invited_at=domain.invited_at,
            accepted_at=domain.accepted_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            created_by=domain.created_by,
            updated_by=domain.updated_by
        )

    def create(self, interview_interviewer: InterviewInterviewer) -> InterviewInterviewer:
        """Create a new interview-interviewer relationship"""
        model = self._to_model(interview_interviewer)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, interviewer_id: str) -> Optional[InterviewInterviewer]:
        """Get interview interviewer by ID"""
        interviewer_id_vo = InterviewInterviewerId.from_string(interviewer_id)
        model = self.base_repo.get_by_id(interviewer_id_vo)
        if model:
            return self._to_domain(model)
        return None

    def update(self, interview_interviewer: InterviewInterviewer) -> InterviewInterviewer:
        """Update an existing interview interviewer"""
        model = self._to_model(interview_interviewer)
        with self.database.get_session() as session:
            db_entity = session.query(InterviewInterviewerModel).filter(
                InterviewInterviewerModel.id == interview_interviewer.id.value
            ).first()
            if db_entity:
                for key, value in model.__dict__.items():
                    if not key.startswith('_'):
                        setattr(db_entity, key, value)
                session.commit()
                session.refresh(db_entity)
                return self._to_domain(db_entity)
            raise ValueError(f"Interview interviewer with id {interview_interviewer.id.value} not found")

    def delete(self, interviewer_id: InterviewInterviewerId) -> bool:
        """Delete an interview interviewer relationship"""
        return self.base_repo.delete(interviewer_id)

    def get_by_interview_id(self, interview_id: str) -> List[InterviewInterviewer]:
        """Get all interviewers for a specific interview"""
        with self.database.get_session() as session:
            models = session.query(InterviewInterviewerModel).filter(
                InterviewInterviewerModel.interview_id == interview_id
            ).all()
            return [self._to_domain(model) for model in models]

    def get_by_user_id(self, user_id: str) -> List[InterviewInterviewer]:
        """Get all interviews where a user is an interviewer"""
        with self.database.get_session() as session:
            models = session.query(InterviewInterviewerModel).filter(
                InterviewInterviewerModel.user_id == user_id
            ).all()
            return [self._to_domain(model) for model in models]

    def get_by_interview_and_user(
        self,
        interview_id: str,
        user_id: str
    ) -> Optional[InterviewInterviewer]:
        """Get specific interviewer relationship by interview and user"""
        with self.database.get_session() as session:
            model = session.query(InterviewInterviewerModel).filter(
                InterviewInterviewerModel.interview_id == interview_id,
                InterviewInterviewerModel.user_id == user_id
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def count_by_interview(self, interview_id: str) -> int:
        """Count interviewers for an interview"""
        with self.database.get_session() as session:
            return session.query(InterviewInterviewerModel).filter(
                InterviewInterviewerModel.interview_id == interview_id
            ).count()

    def is_user_interviewer(self, interview_id: str, user_id: str) -> bool:
        """Check if a user is an interviewer for an interview"""
        interviewer = self.get_by_interview_and_user(interview_id, user_id)
        return interviewer is not None and interviewer.is_accepted()

