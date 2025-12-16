from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any, List

from sqlalchemy import String, JSON, Enum, DateTime, Date, Text, func, Numeric, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.company_bc.candidate_application.infrastructure.models.candidate_application_model import \
    CandidateApplicationModel
from src.company_bc.job_position.domain.enums import (
    JobPositionVisibilityEnum,
    JobPositionStatusEnum,
    EmploymentTypeEnum,
    ExperienceLevelEnum,
    WorkLocationTypeEnum,
    ClosedReasonEnum,
    SalaryPeriodEnum,
    ApplicationModeEnum,
)
from src.framework.domain.entities.base import generate_id
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionModel(Base):
    """SQLAlchemy model for job positions with publishing flow support"""
    __tablename__ = "job_positions"

    # Core identification
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    company_id: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String, index=True)

    # Workflow system - Publication (PO)
    job_position_workflow_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    phase_workflows: Mapped[Optional[Dict[str, str]]] = mapped_column(JSON, nullable=True)
    stage_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    stage_assignments: Mapped[Optional[Dict[str, list]]] = mapped_column(JSON, nullable=True)

    # Workflow system - Candidate Application (CA)
    candidate_application_workflow_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)

    # Content fields
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_category: Mapped[JobCategoryEnum] = mapped_column(Enum(JobCategoryEnum), default=JobCategoryEnum.OTHER)
    skills: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # List of skill tags
    languages: Mapped[Optional[List[Dict]]] = mapped_column(JSON, nullable=True)  # List of LanguageRequirement dicts

    # Standard fields
    department_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    experience_level: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    work_location_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    office_locations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    remote_restrictions: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    number_of_openings: Mapped[int] = mapped_column(Integer, default=1)
    requisition_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Financial fields
    salary_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)  # ISO 4217 currency code
    salary_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    salary_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    show_salary: Mapped[bool] = mapped_column(Boolean, default=False)
    budget_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)  # Internal limit - NEVER exposed
    approved_budget_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)  # Snapshot on approval
    financial_approver_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Ownership fields
    hiring_manager_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    recruiter_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Lifecycle / Publishing flow fields
    status: Mapped[str] = mapped_column(String(30), default=JobPositionStatusEnum.DRAFT.value, index=True)
    closed_reason: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Custom fields snapshot (copied from workflow at creation, frozen at publish)
    custom_fields_config: Mapped[Optional[List[Dict]]] = mapped_column(JSON, nullable=True)  # List of CustomFieldDefinition dicts
    custom_fields_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    source_workflow_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Pipeline references
    candidate_pipeline_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Screening reference
    screening_template_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Killer questions (simple inline questions stored as JSON)
    # Format: List[{name: str, description?: str, data_type: str, scoring_values?: List[{label, scoring}], is_killer?: bool}]
    killer_questions: Mapped[Optional[List[Dict]]] = mapped_column(JSON, nullable=True)

    # Application configuration
    application_mode: Mapped[str] = mapped_column(
        String(20),
        default=ApplicationModeEnum.SHORT.value,
        nullable=False
    )
    required_sections: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Visibility and publishing
    visibility: Mapped[str] = mapped_column(
        String(20),
        default=JobPositionVisibilityEnum.HIDDEN.value,
        index=True
    )
    public_slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    open_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    application_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    applications: Mapped[list["CandidateApplicationModel"]] = relationship(
        back_populates="job_position")

    def __repr__(self) -> str:
        return (
            f"<JobPositionModel(id={self.id}, title={self.title}, "
            f"status={self.status}, visibility={self.visibility})>"
        )
