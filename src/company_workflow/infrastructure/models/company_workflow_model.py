from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus


@dataclass
class CompanyWorkflowModel(Base):
    """SQLAlchemy model for company workflow"""
    __tablename__ = "company_workflows"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    status: Mapped[str] = mapped_column(
        SQLEnum(WorkflowStatus, native_enum=False, length=20),
        nullable=False,
        default=WorkflowStatus.ACTIVE.value,
        index=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
