"""Interview Answer repository implementation"""
from typing import Optional, List

from core.database import DatabaseInterface
from src.interview_bc.interview.Infrastructure.models.interview_answer_model import InterviewAnswerModel
from src.interview_bc.interview.domain.entities.interview_answer import InterviewAnswer
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_answer_id import InterviewAnswerId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyInterviewAnswerRepository(InterviewAnswerRepositoryInterface):
    """SQLAlchemy implementation of Interview Answer repository"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, InterviewAnswerModel)

    def _to_domain(self, model: InterviewAnswerModel) -> InterviewAnswer:
        """Convert model to domain entity"""
        return InterviewAnswer(
            id=InterviewAnswerId.from_string(model.id),
            interview_id=InterviewId.from_string(model.interview_id),
            question_id=InterviewTemplateQuestionId.from_string(model.question_id),
            question_text=model.question_text,
            answer_text=model.answer_text,
            score=model.score,
            feedback=model.feedback,
            answered_at=model.answered_at,
            scored_at=model.scored_at,
            scored_by=model.scored_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by
        )

    def _to_model(self, domain: InterviewAnswer) -> InterviewAnswerModel:
        """Convert domain entity to model"""
        return InterviewAnswerModel(
            id=domain.id.value,
            interview_id=domain.interview_id.value,
            question_id=domain.question_id.value,
            question_text=domain.question_text,
            answer_text=domain.answer_text,
            score=domain.score,
            feedback=domain.feedback,
            answered_at=domain.answered_at,
            scored_at=domain.scored_at,
            scored_by=domain.scored_by,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            created_by=domain.created_by,
            updated_by=domain.updated_by
        )

    def create(self, interview_answer: InterviewAnswer) -> InterviewAnswer:
        """Create a new interview answer"""
        model = self._to_model(interview_answer)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, answer_id: str) -> Optional[InterviewAnswer]:
        """Get interview answer by ID"""
        with self.database.get_session() as session:
            model = session.query(InterviewAnswerModel).filter(InterviewAnswerModel.id == answer_id).first()
            if model:
                return self._to_domain(model)
            return None

    def update(self, interview_answer: InterviewAnswer) -> InterviewAnswer:
        """Update an existing interview answer"""
        with self.database.get_session() as session:
            model = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.id == interview_answer.id.value).first()
            if model:
                # Update all fields from the entity
                model.interview_id = interview_answer.interview_id.value
                model.question_id = interview_answer.question_id.value
                model.question_text = interview_answer.question_text
                model.answer_text = interview_answer.answer_text
                model.score = interview_answer.score
                model.feedback = interview_answer.feedback
                model.answered_at = interview_answer.answered_at
                model.scored_at = interview_answer.scored_at
                model.scored_by = interview_answer.scored_by
                model.updated_at = interview_answer.updated_at
                model.updated_by = interview_answer.updated_by

                session.commit()
                session.refresh(model)
                return self._to_domain(model)
            raise ValueError(f"Interview answer with id {interview_answer.id.value} not found")

    def delete(self, id: InterviewAnswerId) -> bool:
        """Delete an interview answer"""
        return self.base_repo.delete(id)

    def get_by_interview_id(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all answers for an interview"""
        with self.database.get_session() as session:
            models = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id
            ).order_by(InterviewAnswerModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def get_by_question_id(self, question_id: str) -> List[InterviewAnswer]:
        """Get all answers for a specific question"""
        with self.database.get_session() as session:
            models = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.question_id == question_id
            ).order_by(InterviewAnswerModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def get_by_interview_and_question(self, interview_id: str, question_id: str) -> Optional[InterviewAnswer]:
        """Get answer for specific interview and question"""
        with self.database.get_session() as session:
            model = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id,
                InterviewAnswerModel.question_id == question_id
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def get_scored_answers_by_interview(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all scored answers for an interview"""
        with self.database.get_session() as session:
            models = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id,
                InterviewAnswerModel.score.is_not(None)
            ).order_by(InterviewAnswerModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def get_unscored_answers_by_interview(self, interview_id: str) -> List[InterviewAnswer]:
        """Get all unscored answers for an interview"""
        with self.database.get_session() as session:
            models = session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id,
                InterviewAnswerModel.score.is_(None)
            ).order_by(InterviewAnswerModel.created_at).all()
            return [self._to_domain(model) for model in models]

    def count_by_interview(self, interview_id: str) -> int:
        """Count answers for an interview"""
        with self.database.get_session() as session:
            return session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id
            ).count()

    def count_scored_by_interview(self, interview_id: str) -> int:
        """Count scored answers for an interview"""
        with self.database.get_session() as session:
            return session.query(InterviewAnswerModel).filter(
                InterviewAnswerModel.interview_id == interview_id,
                InterviewAnswerModel.score.is_not(None)
            ).count()

    def get_average_score_by_interview(self, interview_id: str) -> Optional[float]:
        """Get average score for an interview"""
        with self.database.get_session() as session:
            from sqlalchemy.sql import func
            result = session.query(func.avg(InterviewAnswerModel.score)).filter(
                InterviewAnswerModel.interview_id == interview_id,
                InterviewAnswerModel.score.is_not(None)
            ).scalar()
            return float(result) if result is not None else None
