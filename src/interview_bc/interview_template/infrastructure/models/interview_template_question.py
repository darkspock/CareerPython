from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Integer, Enum, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.interview.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionDataTypeEnum, \
    InterviewTemplateQuestionStatusEnum, InterviewTemplateQuestionScopeEnum
from src.framework.domain.entities.base import generate_id

# Forward reference for mypy
if TYPE_CHECKING:
    from .interview_template_section import InterviewTemplateSectionModel


@dataclass
class InterviewTemplateQuestionModel(Base):
    """Modelo de SQLAlchemy para preguntas de plantillas de entrevistas"""
    __tablename__ = "interview_template_questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    interview_template_section_id: Mapped[str] = mapped_column(String, ForeignKey("interview_template_sections.id"),
                                                               nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[InterviewTemplateQuestionStatusEnum] = mapped_column(Enum(InterviewTemplateQuestionStatusEnum),
                                                                        nullable=False,
                                                                        default=InterviewTemplateQuestionStatusEnum.DRAFT,
                                                                        index=True)
    data_type: Mapped[InterviewTemplateQuestionDataTypeEnum] = mapped_column(
        Enum(InterviewTemplateQuestionDataTypeEnum))
    scope: Mapped[InterviewTemplateQuestionScopeEnum] = mapped_column(Enum(InterviewTemplateQuestionScopeEnum))
    code: Mapped[str] = mapped_column(String)
    allow_ai_followup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # Allow AI to generate follow-up questions
    legal_notice: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Legal text for this question

    section: Mapped["InterviewTemplateSectionModel"] = relationship("InterviewTemplateSectionModel",
                                                                    back_populates="questions")
