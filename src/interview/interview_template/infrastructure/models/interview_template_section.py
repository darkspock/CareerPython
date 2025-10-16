from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Enum, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.interview.interview_template.domain.enums import InterviewTemplateSectionEnum
from src.interview.interview_template.domain.enums.interview_template_section import InterviewTemplateSectionStatusEnum
from src.shared.domain.entities.base import generate_id

# Forward reference for mypy
if TYPE_CHECKING:
    from .interview_template import InterviewTemplateModel
    from .interview_template_question import InterviewTemplateQuestionModel


@dataclass
class InterviewTemplateSectionModel(Base):
    """SQLAlchemy model for interview template sections"""
    __tablename__ = "interview_template_sections"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    interview_template_id: Mapped[str] = mapped_column(String, ForeignKey("interview_templates.id"), nullable=False,
                                                       index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    intro: Mapped[str] = mapped_column(Text, nullable=False)  # Short introduction for section
    prompt: Mapped[str] = mapped_column(Text, nullable=False)  # Instructions for the interviewer
    goal: Mapped[str] = mapped_column(Text, nullable=False)  # What to achieve with this section
    section: Mapped[Optional[InterviewTemplateSectionEnum]] = mapped_column(Enum(InterviewTemplateSectionEnum),
                                                                            nullable=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    status: Mapped[InterviewTemplateSectionStatusEnum] = mapped_column(Enum(InterviewTemplateSectionStatusEnum),
                                                                       nullable=False,
                                                                       default=InterviewTemplateSectionStatusEnum.DRAFT,
                                                                       index=True)

    # Relationships
    interview_template: Mapped["InterviewTemplateModel"] = relationship("InterviewTemplateModel",
                                                                        back_populates="sections")
    questions: Mapped[List["InterviewTemplateQuestionModel"]] = relationship("InterviewTemplateQuestionModel",
                                                                             back_populates="section",
                                                                             cascade="all, delete-orphan")
