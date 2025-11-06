"""Phase domain entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.enums.phase_status_enum import PhaseStatus
from src.phase.domain.value_objects.phase_id import PhaseId
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum


@dataclass
class Phase:
    id: PhaseId
    workflow_type: WorkflowTypeEnum
    company_id: CompanyId
    name: str
    sort_order: int
    default_view: DefaultView
    status: PhaseStatus
    objective: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            id: PhaseId,
            workflow_type: WorkflowTypeEnum,
            company_id: CompanyId,
            name: str,
            sort_order: int,
            default_view: DefaultView,
            objective: Optional[str] = None,
            status: PhaseStatus = PhaseStatus.ACTIVE
    ) -> 'Phase':
        """Create a new Phase"""
        if not name or name.strip() == "":
            raise ValueError("Phase name is required")

        if sort_order < 0:
            raise ValueError("Sort order must be non-negative")

        now = datetime.utcnow()

        return Phase(
            id=id,
            workflow_type=workflow_type,
            company_id=company_id,
            name=name.strip(),
            sort_order=sort_order,
            default_view=default_view,
            status=status,
            objective=objective,
            created_at=now,
            updated_at=now
        )

    def update_details(
            self,
            name: str,
            sort_order: int,
            default_view: DefaultView,
            objective: Optional[str] = None
    ) -> None:
        """Update phase details"""
        if not name or name.strip() == "":
            raise ValueError("Phase name is required")

        if sort_order < 0:
            raise ValueError("Sort order must be non-negative")

        self.name = name.strip()
        self.sort_order = sort_order
        self.default_view = default_view
        self.objective = objective
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive this phase (soft delete)"""
        if self.status == PhaseStatus.ARCHIVED:
            raise ValueError("Phase is already archived")
        self.status = PhaseStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate this phase"""
        if self.status == PhaseStatus.ACTIVE:
            raise ValueError("Phase is already active")
        self.status = PhaseStatus.ACTIVE
        self.updated_at = datetime.utcnow()

    def set_draft(self) -> None:
        """Set phase to draft status"""
        if self.status == PhaseStatus.DRAFT:
            raise ValueError("Phase is already in draft status")
        self.status = PhaseStatus.DRAFT
        self.updated_at = datetime.utcnow()
