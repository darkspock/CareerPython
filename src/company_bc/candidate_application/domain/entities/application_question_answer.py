from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from src.company_bc.candidate_application.domain.value_objects.application_question_answer_id import (
    ApplicationQuestionAnswerId
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import (
    CandidateApplicationId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class ApplicationQuestionAnswer:
    """
    Application Question Answer entity - stores a candidate's answer to a screening question.

    This entity captures the answer provided by a candidate when applying to a job position.
    The answer_value is stored as a flexible type to accommodate different question types
    (text, number, date, select options, etc.).
    """
    id: ApplicationQuestionAnswerId
    application_id: CandidateApplicationId
    question_id: ApplicationQuestionId
    answer_value: Any  # Can be str, int, float, bool, list (for multiselect), etc.
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: ApplicationQuestionAnswerId,
        application_id: CandidateApplicationId,
        question_id: ApplicationQuestionId,
        answer_value: Any
    ) -> "ApplicationQuestionAnswer":
        """Factory method to create a new application question answer."""
        now = datetime.utcnow()
        return cls(
            id=id,
            application_id=application_id,
            question_id=question_id,
            answer_value=answer_value,
            created_at=now,
            updated_at=now
        )

    def update_answer(self, answer_value: Any) -> None:
        """Update the answer value."""
        self.answer_value = answer_value
        self.updated_at = datetime.utcnow()
