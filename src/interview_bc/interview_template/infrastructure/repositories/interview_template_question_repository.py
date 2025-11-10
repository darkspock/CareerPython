from typing import List, Optional

from core.database import DatabaseInterface
from src.interview.interview_template.domain.entities.interview_template_question import InterviewTemplateQuestion
from src.interview.interview_template.domain.enums import InterviewTemplateQuestionStatusEnum
from src.interview.interview_template.domain.infrastructure.interview_template_question_repository_interface import \
    InterviewTemplateQuestionRepositoryInterface
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.models.interview_template_question import \
    InterviewTemplateQuestionModel
from src.framework.infrastructure.repositories.base import BaseRepository


class InterviewTemplateQuestionRepository(InterviewTemplateQuestionRepositoryInterface):
    """Implementación de repositorio de preguntas de plantillas de entrevistas con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, InterviewTemplateQuestionModel)

    def _to_domain(self, model: InterviewTemplateQuestionModel) -> InterviewTemplateQuestion:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
            InterviewTemplateQuestionId
        from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
            InterviewTemplateSectionId

        return InterviewTemplateQuestion(
            id=InterviewTemplateQuestionId.from_string(str(model.id)),
            interview_template_section_id=InterviewTemplateSectionId.from_string(
                str(model.interview_template_section_id)),
            sort_order=model.sort_order or 0,
            name=str(model.name),
            description=str(model.description) if model.description else "",
            status=model.status,
            data_type=model.data_type,
            scope=model.scope,
            code=str(model.code),
            allow_ai_followup=model.allow_ai_followup,
            legal_notice=model.legal_notice
        )

    def _to_model(self, domain: InterviewTemplateQuestion) -> InterviewTemplateQuestionModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        return InterviewTemplateQuestionModel(
            id=domain.id.value,
            interview_template_section_id=domain.interview_template_section_id.value,
            sort_order=domain.sort_order,
            name=domain.name,
            description=domain.description,
            status=domain.status,
            data_type=domain.data_type,
            scope=domain.scope,
            code=domain.code,
            allow_ai_followup=domain.allow_ai_followup,
            legal_notice=domain.legal_notice
        )

    def create(self, interview_template_question: InterviewTemplateQuestion) -> InterviewTemplateQuestion:
        model = self._to_model(interview_template_question)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, id: InterviewTemplateQuestionId) -> Optional[InterviewTemplateQuestion]:
        model = self.base_repo.get_by_id(id)
        if model:
            return self._to_domain(model)
        return None

    def get_all(self, interview_template_section_id: Optional[InterviewTemplateSectionId] = None,
                status: Optional[InterviewTemplateQuestionStatusEnum] = None) -> List[InterviewTemplateQuestion]:
        with self.database.get_session() as session:
            query = session.query(InterviewTemplateQuestionModel)
            if interview_template_section_id:
                query = query.filter(
                    InterviewTemplateQuestionModel.interview_template_section_id == interview_template_section_id.value)
            if status:
                query = query.filter(InterviewTemplateQuestionModel.status == status)
            models = query.all()
            return [self._to_domain(model) for model in models]

    def update(self, question: InterviewTemplateQuestion) -> None:
        """Update question - same pattern as InterviewTemplateRepository"""
        with self.database.get_session() as session:
            db_question = session.query(InterviewTemplateQuestionModel).filter(
                InterviewTemplateQuestionModel.id == question.id.value,
            ).first()

            if not db_question:
                raise ValueError(f"Question {question.id.value} not found")

            # Update fields
            db_question.interview_template_section_id = question.interview_template_section_id.value
            db_question.sort_order = question.sort_order
            db_question.name = question.name
            db_question.description = question.description
            db_question.status = question.status
            db_question.data_type = question.data_type
            db_question.scope = question.scope
            db_question.code = question.code
            db_question.allow_ai_followup = question.allow_ai_followup
            db_question.legal_notice = question.legal_notice

            session.commit()

    def update_entity(self, question: InterviewTemplateQuestion) -> None:
        """Update a question entity (same as update method)"""
        self.update(question)

    def get_by_section_id(self, section_id: InterviewTemplateSectionId) -> List[InterviewTemplateQuestion]:
        """Get all questions for a specific section"""
        with self.database.get_session() as session:
            models = session.query(InterviewTemplateQuestionModel).filter(
                InterviewTemplateQuestionModel.interview_template_section_id == section_id.value
            ).all()
            return [self._to_domain(model) for model in models]

    def delete(self, id: InterviewTemplateQuestionId) -> bool:
        return self.base_repo.delete(id)
