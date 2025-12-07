from abc import ABC, abstractmethod
from typing import Optional, List

from src.shared_bc.customization.workflow.domain.entities.application_question import (
    ApplicationQuestion
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


class ApplicationQuestionRepositoryInterface(ABC):
    """Repository interface for ApplicationQuestion entity."""

    @abstractmethod
    def get_by_id(self, question_id: ApplicationQuestionId) -> Optional[ApplicationQuestion]:
        """Get an application question by ID."""
        pass

    @abstractmethod
    def list_by_workflow(
        self,
        workflow_id: WorkflowId,
        active_only: bool = True
    ) -> List[ApplicationQuestion]:
        """List all application questions for a workflow."""
        pass

    @abstractmethod
    def get_by_field_key(
        self,
        workflow_id: WorkflowId,
        field_key: str
    ) -> Optional[ApplicationQuestion]:
        """Get an application question by field key within a workflow."""
        pass

    @abstractmethod
    def save(self, question: ApplicationQuestion) -> None:
        """Save an application question (insert or update)."""
        pass

    @abstractmethod
    def delete(self, question_id: ApplicationQuestionId) -> None:
        """Delete an application question."""
        pass
