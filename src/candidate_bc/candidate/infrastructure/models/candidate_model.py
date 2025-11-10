from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, List, Any

from sqlalchemy import String, Integer, Boolean, JSON, Enum, DateTime, Date, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.candidate_bc.candidate.domain.enums.candidate_enums import CandidateStatusEnum, CandidateTypeEnum
from src.framework.domain.entities.base import generate_id
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class CandidateModel(Base):
    __tablename__ = "candidates"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    name: Mapped[str] = mapped_column(String, index=True)
    date_of_birth: Mapped[date] = mapped_column(Date)
    city: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[CandidateStatusEnum] = mapped_column(Enum(CandidateStatusEnum), default=CandidateStatusEnum.DRAFT)
    job_category: Mapped[JobCategoryEnum] = mapped_column(Enum(JobCategoryEnum), default=JobCategoryEnum.OTHER)
    candidate_type: Mapped[CandidateTypeEnum] = mapped_column(Enum(CandidateTypeEnum), default=CandidateTypeEnum.BASIC)
    expected_annual_salary: Mapped[Optional[int]] = mapped_column(Integer)
    current_annual_salary: Mapped[Optional[int]] = mapped_column(Integer)
    currency: Mapped[Optional[str]] = mapped_column(String, default='EUR')
    relocation: Mapped[Optional[bool]] = mapped_column(Boolean)
    work_modality: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of WorkModalityEnum values
    languages: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)  # Dict of LanguageEnum -> LanguageLevelEnum
    other_languages: Mapped[Optional[str]] = mapped_column(String)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String)
    data_consent: Mapped[Optional[bool]] = mapped_column(Boolean)
    data_consent_on: Mapped[Optional[date]] = mapped_column(Date)
    current_roles: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of PositionLevelEnum values
    expected_roles: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of PositionLevelEnum values
    skills: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of strings
    created_on: Mapped[date] = mapped_column(Date, default=func.current_date())
    updated_on: Mapped[date] = mapped_column(Date, default=func.current_date(), onupdate=func.current_date())
    timezone: Mapped[Optional[str]] = mapped_column(String)
    candidate_notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    experiences: Mapped[List["CandidateExperienceModel"]] = relationship(back_populates="candidate")  # type: ignore # noqa: F821
    educations: Mapped[List["CandidateEducationModel"]] = relationship(back_populates="candidate")  # type: ignore # noqa: F821
    projects: Mapped[List["CandidateProjectModel"]] = relationship(back_populates="candidate")  # type: ignore # noqa: F821
    applications: Mapped[List["CandidateApplicationModel"]] = relationship(back_populates="candidate")  # type: ignore # noqa: F821
    file_attachments: Mapped[List["FileAttachmentModel"]] = relationship(back_populates="candidate")  # type: ignore # noqa: F821
