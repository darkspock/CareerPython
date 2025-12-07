from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.position_question_config_id import (
    PositionQuestionConfigId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class PositionQuestionConfig:
    """
    Position Question Config entity - links job positions to application questions.

    This entity enables the hybrid approach where questions are defined at the
    workflow level but can be enabled/disabled per job position.
    """
    id: PositionQuestionConfigId
    position_id: JobPositionId
    question_id: ApplicationQuestionId
    enabled: bool  # Whether this question is shown for this position
    is_required_override: Optional[bool]  # Override the default required state (None = use default)
    sort_order_override: Optional[int]  # Override the display order (None = use default)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: PositionQuestionConfigId,
        position_id: JobPositionId,
        question_id: ApplicationQuestionId,
        enabled: bool = True,
        is_required_override: Optional[bool] = None,
        sort_order_override: Optional[int] = None
    ) -> "PositionQuestionConfig":
        """Factory method to create a new position question config."""
        now = datetime.utcnow()
        return cls(
            id=id,
            position_id=position_id,
            question_id=question_id,
            enabled=enabled,
            is_required_override=is_required_override,
            sort_order_override=sort_order_override,
            created_at=now,
            updated_at=now
        )

    def enable(self) -> None:
        """Enable this question for the position."""
        self.enabled = True
        self.updated_at = datetime.utcnow()

    def disable(self) -> None:
        """Disable this question for the position."""
        self.enabled = False
        self.updated_at = datetime.utcnow()

    def toggle(self) -> None:
        """Toggle the enabled state."""
        self.enabled = not self.enabled
        self.updated_at = datetime.utcnow()

    def set_required_override(self, is_required: Optional[bool]) -> None:
        """Set or clear the required override."""
        self.is_required_override = is_required
        self.updated_at = datetime.utcnow()

    def set_sort_order_override(self, sort_order: Optional[int]) -> None:
        """Set or clear the sort order override."""
        self.sort_order_override = sort_order
        self.updated_at = datetime.utcnow()

    def update(
        self,
        enabled: Optional[bool] = None,
        is_required_override: Optional[bool] = None,
        sort_order_override: Optional[int] = None
    ) -> None:
        """Update the config."""
        if enabled is not None:
            self.enabled = enabled
        # Note: These can be set to None intentionally to clear the override
        self.is_required_override = is_required_override
        self.sort_order_override = sort_order_override
        self.updated_at = datetime.utcnow()
