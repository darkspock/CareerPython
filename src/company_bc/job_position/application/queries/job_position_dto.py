"""Job position DTOs"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain import JobPosition
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionDto:
    """Simplified JobPosition DTO - removed fields are in custom_fields_values"""
    id: JobPositionId
    title: str
    company_id: CompanyId
    job_position_workflow_id: Optional[str]  # Workflow system
    stage_id: Optional[str]  # Current stage
    phase_workflows: Optional[Dict[str, str]]  # Phase 12.8: phase_id -> workflow_id mapping
    custom_fields_values: Dict[str, Any]  # Custom field values (contains all removed fields)
    description: Optional[str]
    job_category: JobCategoryEnum
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    visibility: str  # JobPositionVisibilityEnum value
    public_slug: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    pending_comments_count: int = 0  # Number of pending comments

    @staticmethod
    def from_entity(entity: JobPosition) -> 'JobPositionDto':
        """Create a JobPositionDto from a JobPosition entity"""
        return JobPositionDto(
            id=entity.id,
            company_id=entity.company_id,
            job_position_workflow_id=entity.job_position_workflow_id.value if entity.job_position_workflow_id else None,
            stage_id=entity.stage_id.value if entity.stage_id else None,
            phase_workflows=entity.phase_workflows,
            custom_fields_values=entity.custom_fields_values,
            title=entity.title,
            description=entity.description,
            job_category=entity.job_category,
            open_at=entity.open_at,
            application_deadline=entity.application_deadline,
            visibility=entity.visibility.value,
            public_slug=entity.public_slug,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


@dataclass
class JobPositionStatsDto:
    """Job position statistics data transfer object"""
    total_positions: int = 0
    active_positions: int = 0
    inactive_positions: int = 0
    positions_by_type: Optional[Dict[str, int]] = None
    positions_by_company: Optional[Dict[str, int]] = None


@dataclass
class JobPositionListDto:
    """Job position list data transfer object"""
    positions: List[JobPositionDto]
    total: int
    page: int
    page_size: int
    total_pages: int
