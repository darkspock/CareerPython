from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlalchemy import String, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.framework.domain.entities.base import generate_id
from src.company_bc.job_position.domain.enums import JobPositionWorkflowStatusEnum


@dataclass
class JobPositionWorkflowModel(Base):
    """SQLAlchemy model for job position workflows"""
    __tablename__ = "job_position_workflows"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    company_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    default_view: Mapped[str] = mapped_column(String(20), nullable=False, default="kanban")
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=JobPositionWorkflowStatusEnum.PUBLISHED.value,
        index=True
    )  # Status stored as string value (draft, published, deprecated)
    stages: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)  # List of WorkflowStage as JSON
    custom_fields_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<JobPositionWorkflowModel(id={self.id}, name={self.name})>"

