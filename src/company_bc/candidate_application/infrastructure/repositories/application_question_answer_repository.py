from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from src.company_bc.candidate_application.domain.entities.application_question_answer import (
    ApplicationQuestionAnswer
)
from src.company_bc.candidate_application.domain.repositories.application_question_answer_repository_interface import (
    ApplicationQuestionAnswerRepositoryInterface
)
from src.company_bc.candidate_application.domain.value_objects.application_question_answer_id import (
    ApplicationQuestionAnswerId
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import (
    CandidateApplicationId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)
from src.company_bc.candidate_application.infrastructure.models.application_question_answer_model import (
    ApplicationQuestionAnswerModel
)
from src.shared_bc.customization.workflow.infrastructure.models.application_question_model import (
    ApplicationQuestionModel
)


class ApplicationQuestionAnswerRepository(ApplicationQuestionAnswerRepositoryInterface):
    """SQLAlchemy implementation of ApplicationQuestionAnswerRepository."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, answer_id: ApplicationQuestionAnswerId) -> Optional[ApplicationQuestionAnswer]:
        model = self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.id == str(answer_id.value)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def get_by_application_and_question(
        self,
        application_id: CandidateApplicationId,
        question_id: ApplicationQuestionId
    ) -> Optional[ApplicationQuestionAnswer]:
        model = self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.application_id == str(application_id.value),
            ApplicationQuestionAnswerModel.question_id == str(question_id.value)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def list_by_application(
        self,
        application_id: CandidateApplicationId
    ) -> List[ApplicationQuestionAnswer]:
        models = self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.application_id == str(application_id.value)
        ).all()

        return [self._to_domain(m) for m in models]

    def get_answers_as_dict(
        self,
        application_id: CandidateApplicationId
    ) -> Dict[str, Any]:
        """
        Get all answers for an application as a dictionary.

        Returns a dict mapping question field_key to answer_value.
        This format is useful for JsonLogic evaluation.
        """
        # Join with application_questions to get the field_key
        results = self.session.query(
            ApplicationQuestionModel.field_key,
            ApplicationQuestionAnswerModel.answer_value
        ).join(
            ApplicationQuestionModel,
            ApplicationQuestionAnswerModel.question_id == ApplicationQuestionModel.id
        ).filter(
            ApplicationQuestionAnswerModel.application_id == str(application_id.value)
        ).all()

        return {row.field_key: row.answer_value for row in results}

    def save(self, answer: ApplicationQuestionAnswer) -> None:
        existing = self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.id == str(answer.id.value)
        ).first()

        if existing:
            # Update existing
            existing.answer_value = answer.answer_value
            existing.updated_at = answer.updated_at
        else:
            # Insert new
            model = self._to_model(answer)
            self.session.add(model)

        self.session.commit()

    def save_many(self, answers: List[ApplicationQuestionAnswer]) -> None:
        for answer in answers:
            existing = self.session.query(ApplicationQuestionAnswerModel).filter(
                ApplicationQuestionAnswerModel.id == str(answer.id.value)
            ).first()

            if existing:
                existing.answer_value = answer.answer_value
                existing.updated_at = answer.updated_at
            else:
                model = self._to_model(answer)
                self.session.add(model)

        self.session.commit()

    def delete(self, answer_id: ApplicationQuestionAnswerId) -> None:
        self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.id == str(answer_id.value)
        ).delete()
        self.session.commit()

    def delete_by_application(self, application_id: CandidateApplicationId) -> int:
        count: int = self.session.query(ApplicationQuestionAnswerModel).filter(
            ApplicationQuestionAnswerModel.application_id == str(application_id.value)
        ).delete()
        self.session.commit()
        return count

    def _to_domain(self, model: ApplicationQuestionAnswerModel) -> ApplicationQuestionAnswer:
        """Convert SQLAlchemy model to domain entity."""
        return ApplicationQuestionAnswer(
            id=ApplicationQuestionAnswerId(str(model.id)),
            application_id=CandidateApplicationId(str(model.application_id)),
            question_id=ApplicationQuestionId(str(model.question_id)),
            answer_value=model.answer_value,
            created_at=model.created_at,  # type: ignore[arg-type]
            updated_at=model.updated_at  # type: ignore[arg-type]
        )

    def _to_model(self, entity: ApplicationQuestionAnswer) -> ApplicationQuestionAnswerModel:
        """Convert domain entity to SQLAlchemy model."""
        return ApplicationQuestionAnswerModel(
            id=str(entity.id.value),
            application_id=str(entity.application_id.value),
            question_id=str(entity.question_id.value),
            answer_value=entity.answer_value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
