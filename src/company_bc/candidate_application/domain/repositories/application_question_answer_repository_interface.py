from abc import abstractmethod, ABC
from typing import Optional, List, Dict, Any

from src.company_bc.candidate_application.domain.entities.application_question_answer import (
    ApplicationQuestionAnswer
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


class ApplicationQuestionAnswerRepositoryInterface(ABC):
    """Repository interface for ApplicationQuestionAnswer entity."""

    @abstractmethod
    def get_by_id(self, answer_id: ApplicationQuestionAnswerId) -> Optional[ApplicationQuestionAnswer]:
        """Get an answer by ID."""
        pass

    @abstractmethod
    def get_by_application_and_question(
        self,
        application_id: CandidateApplicationId,
        question_id: ApplicationQuestionId
    ) -> Optional[ApplicationQuestionAnswer]:
        """Get the answer for a specific application and question combination."""
        pass

    @abstractmethod
    def list_by_application(
        self,
        application_id: CandidateApplicationId
    ) -> List[ApplicationQuestionAnswer]:
        """List all answers for an application."""
        pass

    @abstractmethod
    def get_answers_as_dict(
        self,
        application_id: CandidateApplicationId
    ) -> Dict[str, Any]:
        """
        Get all answers for an application as a dictionary.

        Returns a dict mapping question field_key to answer_value.
        This format is useful for JsonLogic evaluation.
        """
        pass

    @abstractmethod
    def save(self, answer: ApplicationQuestionAnswer) -> None:
        """Save an answer (insert or update)."""
        pass

    @abstractmethod
    def save_many(self, answers: List[ApplicationQuestionAnswer]) -> None:
        """Save multiple answers at once."""
        pass

    @abstractmethod
    def delete(self, answer_id: ApplicationQuestionAnswerId) -> None:
        """Delete an answer."""
        pass

    @abstractmethod
    def delete_by_application(self, application_id: CandidateApplicationId) -> int:
        """Delete all answers for an application. Returns count of deleted records."""
        pass
