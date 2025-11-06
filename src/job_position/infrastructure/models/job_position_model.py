from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

from sqlalchemy import String, JSON, Enum, DateTime, Date, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.job_position.domain.enums import JobPositionVisibilityEnum
from src.shared.domain.entities.base import generate_id
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionModel(Base):
    """SQLAlchemy model for job positions - simplified version"""
    __tablename__ = "job_positions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    company_id: Mapped[str] = mapped_column(String, index=True)  # Removed ForeignKey
    job_position_workflow_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)  # Workflow system
    stage_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)  # Current stage in workflow
    phase_workflows: Mapped[Optional[Dict[str, str]]] = mapped_column(JSON)  # Phase 12.8: phase_id -> workflow_id mapping
    stage_assignments: Mapped[Optional[Dict[str, list]]] = mapped_column(JSON, nullable=True)  # Stage assignments: stage_id -> [company_user_id, ...]
    custom_fields_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # Custom field values (JSON) - contains all removed fields
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)  # Job description
    job_category: Mapped[JobCategoryEnum] = mapped_column(Enum(JobCategoryEnum), default=JobCategoryEnum.OTHER)
    open_at: Mapped[Optional[datetime]] = mapped_column(DateTime)  # When the position will be opened
    application_deadline: Mapped[Optional[date]] = mapped_column(Date)
    visibility: Mapped[str] = mapped_column(
        String(20),
        default=JobPositionVisibilityEnum.HIDDEN.value,
        index=True
    )  # Visibility level (replaces is_public) - stored as string value (hidden, internal, public)
    public_slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)  # SEO-friendly URL slug
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    applications: Mapped[list["CandidateApplicationModel"]] = relationship(
        back_populates="job_position")

    def __repr__(self) -> str:
        return f"<JobPositionModel(id={self.id}, title={self.title}, job_position_workflow_id={self.job_position_workflow_id}, stage_id={self.stage_id}, visibility={self.visibility})>"
