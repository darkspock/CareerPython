"""
Email Template SQLAlchemy Model
Phase 7: Database model for email templates
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql import func

from core.database import Base


class EmailTemplateModel(Base):
    """SQLAlchemy model for email_templates table"""

    __tablename__ = 'email_templates'

    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('company_workflows.id', ondelete='CASCADE'), nullable=False)
    stage_id = Column(String, ForeignKey('workflow_stages.id', ondelete='CASCADE'), nullable=True)
    template_name = Column(String(200), nullable=False)
    template_key = Column(String(100), nullable=False)
    subject = Column(String(500), nullable=False)
    body_html = Column(Text, nullable=False)
    body_text = Column(Text, nullable=True)
    available_variables = Column(JSON, nullable=False)
    trigger_event = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Indexes
    __table_args__ = (
        Index('ix_email_templates_workflow_id', 'workflow_id'),
        Index('ix_email_templates_stage_id', 'stage_id'),
        Index('ix_email_templates_trigger_event', 'trigger_event'),
        UniqueConstraint('workflow_id', 'stage_id', 'trigger_event', name='uq_email_templates_workflow_stage_trigger'),
    )
