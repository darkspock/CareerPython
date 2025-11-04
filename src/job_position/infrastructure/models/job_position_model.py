from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, List, Any

from sqlalchemy import String, JSON, Enum, DateTime, Integer, Boolean, Date, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.job_position.domain.enums import JobPositionStatusEnum, ContractTypeEnum, WorkLocationTypeEnum
from src.job_position.domain.enums.employment_type import EmploymentType
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.shared.domain.entities.base import generate_id
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionModel(Base):
    """SQLAlchemy model for job positions"""
    __tablename__ = "job_positions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    company_id: Mapped[str] = mapped_column(String, index=True)  # Removed ForeignKey
    workflow_id: Mapped[Optional[str]] = mapped_column(String, index=True)  # Legacy/default workflow
    phase_workflows: Mapped[Optional[Dict[str, str]]] = mapped_column(JSON)  # Phase 12.8: phase_id -> workflow_id mapping
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)  # Job description
    location: Mapped[Optional[str]] = mapped_column(String)  # Work location
    employment_type: Mapped[Optional[EmploymentType]] = mapped_column(Enum(EmploymentType))  # Employment type
    work_location_type: Mapped[WorkLocationTypeEnum] = mapped_column(Enum(WorkLocationTypeEnum),
                                                                     default=WorkLocationTypeEnum.ON_SITE)
    salary_range: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)  # {min_salary, max_salary, currency}
    contract_type: Mapped[ContractTypeEnum] = mapped_column(Enum(ContractTypeEnum), default=ContractTypeEnum.FULL_TIME)
    requirements: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON)  # Technical, soft skills, cultural requirements
    job_category: Mapped[JobCategoryEnum] = mapped_column(Enum(JobCategoryEnum), default=JobCategoryEnum.OTHER)
    position_level: Mapped[Optional[JobPositionLevelEnum]] = mapped_column(
        Enum(JobPositionLevelEnum))  # JobPositionLevelEnum
    application_deadline: Mapped[Optional[date]] = mapped_column(Date)
    number_of_openings: Mapped[int] = mapped_column(Integer, default=1)
    application_instructions: Mapped[Optional[str]] = mapped_column(Text)
    benefits: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of strings
    working_hours: Mapped[Optional[str]] = mapped_column(String)  # e.g., "40h/week", "flexible"
    travel_required: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)  # Whether travel is required
    languages_required: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON)  # Dict of LanguageEnum -> LanguageLevelEnum
    visa_sponsorship: Mapped[bool] = mapped_column(Boolean, default=False)
    contact_person: Mapped[Optional[str]] = mapped_column(String)
    department: Mapped[Optional[str]] = mapped_column(String)
    reports_to: Mapped[Optional[str]] = mapped_column(String)
    desired_roles: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of PositionRoleEnum values
    open_at: Mapped[Optional[datetime]] = mapped_column(DateTime)  # When the position will be opened
    skills: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of skill strings
    application_url: Mapped[Optional[str]] = mapped_column(String)  # URL to apply
    application_email: Mapped[Optional[str]] = mapped_column(String)  # Email to apply
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, index=True)  # Whether position is publicly visible
    public_slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)  # SEO-friendly URL slug
    status: Mapped[JobPositionStatusEnum] = mapped_column(
        Enum(JobPositionStatusEnum, values_callable=lambda x: [e.value for e in x]),
        default=JobPositionStatusEnum.DRAFT
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships - DISABLED
    # company: Mapped["CompanyModel"] = relationship(back_populates="job_positions")  # type: ignore
    applications: Mapped[List["CandidateApplicationModel"]] = relationship(
        back_populates="job_position")

    def __repr__(self) -> str:
        return f"<JobPositionModel(id={self.id}, title={self.title}, status={self.status})>"
