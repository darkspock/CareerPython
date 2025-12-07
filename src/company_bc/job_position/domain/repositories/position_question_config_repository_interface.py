from abc import abstractmethod, ABC
from typing import Optional, List

from src.company_bc.job_position.domain.entities.position_question_config import (
    PositionQuestionConfig
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.position_question_config_id import (
    PositionQuestionConfigId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


class PositionQuestionConfigRepositoryInterface(ABC):
    """Repository interface for PositionQuestionConfig entity."""

    @abstractmethod
    def get_by_id(self, config_id: PositionQuestionConfigId) -> Optional[PositionQuestionConfig]:
        """Get a position question config by ID."""
        pass

    @abstractmethod
    def get_by_position_and_question(
        self,
        position_id: JobPositionId,
        question_id: ApplicationQuestionId
    ) -> Optional[PositionQuestionConfig]:
        """Get config for a specific position and question combination."""
        pass

    @abstractmethod
    def list_by_position(
        self,
        position_id: JobPositionId,
        enabled_only: bool = False
    ) -> List[PositionQuestionConfig]:
        """List all question configs for a position."""
        pass

    @abstractmethod
    def save(self, config: PositionQuestionConfig) -> None:
        """Save a position question config (insert or update)."""
        pass

    @abstractmethod
    def delete(self, config_id: PositionQuestionConfigId) -> None:
        """Delete a position question config."""
        pass

    @abstractmethod
    def delete_by_position(self, position_id: JobPositionId) -> int:
        """Delete all configs for a position. Returns count of deleted records."""
        pass

    @abstractmethod
    def delete_by_question(self, question_id: ApplicationQuestionId) -> int:
        """Delete all configs for a question. Returns count of deleted records."""
        pass
