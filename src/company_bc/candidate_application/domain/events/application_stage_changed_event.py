"""
Application Stage Changed Event
Phase 7: Domain event triggered when an application moves to a new stage
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from src.framework.domain.events.domain_event import DomainEvent


@dataclass(frozen=True)
class ApplicationStageChangedEvent(DomainEvent):
    """Event published when a candidate application changes stage"""

    application_id: str
    candidate_id: str
    workflow_id: str
    previous_stage_id: Optional[str]
    new_stage_id: str
    new_stage_name: str
    candidate_email: str
    candidate_name: str
    position_title: str
    company_name: str
    changed_at: datetime
    changed_by_user_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate event data"""
        if not self.application_id:
            raise ValueError("application_id is required")
        if not self.candidate_id:
            raise ValueError("candidate_id is required")
        if not self.workflow_id:
            raise ValueError("workflow_id is required")
        if not self.new_stage_id:
            raise ValueError("new_stage_id is required")
        if not self.candidate_email:
            raise ValueError("candidate_email is required")
