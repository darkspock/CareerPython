from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Index
from core.database import Base
from datetime import datetime


class ApplicationQuestionAnswerModel(Base):
    """SQLAlchemy model for application question answers"""

    __tablename__ = "application_question_answers"

    id = Column(String(26), primary_key=True)  # ULID
    application_id = Column(
        String(26),
        ForeignKey("candidate_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    question_id = Column(
        String(26),
        ForeignKey("application_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    answer_value = Column(JSON, nullable=True)  # JSON to support various types
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        # Unique constraint: one answer per question per application
        Index(
            'uq_application_question_answer',
            'application_id',
            'question_id',
            unique=True
        ),
        # Composite index for efficient lookups
        Index('ix_application_answers_app_question', 'application_id', 'question_id'),
    )
