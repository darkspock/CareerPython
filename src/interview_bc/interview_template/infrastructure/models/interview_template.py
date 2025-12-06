from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING

from sqlalchemy import String, Enum, Text, DateTime, Index, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.framework.domain.entities.base import generate_id
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateTypeEnum,
    InterviewTemplateStatusEnum,
    ScoringModeEnum
)

# Forward reference for mypy
if TYPE_CHECKING:
    from .interview_template_section import InterviewTemplateSectionModel


@dataclass
class InterviewTemplateModel(Base):
    """SQLAlchemy model for interview templates with versioning support"""
    __tablename__ = "interview_templates"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    intro: Mapped[str] = mapped_column(Text, nullable=False)  # Short introduction for interview
    prompt: Mapped[str] = mapped_column(Text, nullable=False)  # Instructions for the interviewer
    goal: Mapped[str] = mapped_column(Text, nullable=False)  # What to achieve with this template
    type: Mapped[InterviewTemplateTypeEnum] = mapped_column(Enum(InterviewTemplateTypeEnum), nullable=False, index=True)
    status: Mapped[InterviewTemplateStatusEnum] = mapped_column(Enum(InterviewTemplateStatusEnum), nullable=False,
                                                                default=InterviewTemplateStatusEnum.DRAFT, index=True)
    job_category: Mapped[Optional[JobCategoryEnum]] = mapped_column(Enum(JobCategoryEnum), nullable=True, index=True)
    allow_ai_questions: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                                     default=False)  # Allow AI to generate additional questions
    use_conversational_mode: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                                          default=False)  # Use chat-style AI conversation
    scoring_mode: Mapped[Optional[ScoringModeEnum]] = mapped_column(Enum(ScoringModeEnum), nullable=True,
                                                                    index=True)  # Scoring mode: DISTANCE or ABSOLUTE
    legal_notice: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Legal text for compliance

    # Extended metadata
    created_by: Mapped[Optional[str]] = mapped_column(String, nullable=True,
                                                      index=True)  # User who created this template
    company_id: Mapped[Optional[str]] = mapped_column(String, nullable=True,
                                                      index=True)  # Company that owns this template
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # List of tags for categorization
    template_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # Additional metadata

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                                                 nullable=False)

    # Relationships
    sections: Mapped[List["InterviewTemplateSectionModel"]] = relationship("InterviewTemplateSectionModel",
                                                                           back_populates="interview_template",
                                                                           cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_status_type', 'status', 'type'),
        Index('idx_job_category_status', 'job_category', 'status'),
        Index('idx_type', 'type'),
        Index('idx_created_by_status', 'created_by', 'status'),
        Index('idx_company_id_status', 'company_id', 'status'),  # Composite index for company filtering
    )
