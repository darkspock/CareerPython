"""Phase domain entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class Phase:
    """Phase domain entity - represents a high-level stage in the recruitment process"""
    id: PhaseId
    company_id: CompanyId
    name: str
    sort_order: int
    default_view: DefaultView
    objective: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        company_id: CompanyId,
        name: str,
        sort_order: int,
        default_view: DefaultView,
        objective: Optional[str] = None
    ) -> 'Phase':
        """Create a new Phase"""
        if not name or name.strip() == "":
            raise ValueError("Phase name is required")

        if sort_order < 0:
            raise ValueError("Sort order must be non-negative")

        now = datetime.utcnow()

        return Phase(
            id=PhaseId.generate(),
            company_id=company_id,
            name=name.strip(),
            sort_order=sort_order,
            default_view=default_view,
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

    @classmethod
    def _from_repository(
        cls,
        id: PhaseId,
        company_id: CompanyId,
        name: str,
        sort_order: int,
        default_view: DefaultView,
        objective: Optional[str],
        created_at: datetime,
        updated_at: datetime
    ) -> 'Phase':
        """Create Phase from repository data - only for repositories to use"""
        return cls(
            id=id,
            company_id=company_id,
            name=name,
            sort_order=sort_order,
            default_view=default_view,
            objective=objective,
            created_at=created_at,
            updated_at=updated_at
        )
