"""Position stage assignment SQLAlchemy model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB

from core.database import Base


class PositionStageAssignmentModel(Base):
    """Position stage assignment database model"""
    __tablename__ = "position_stage_assignments"

    id = Column(String, primary_key=True, index=True)
    position_id = Column(String, ForeignKey("job_positions.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_id = Column(String, ForeignKey("workflow_stages.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_user_ids = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    updated_at = Column(DateTime, nullable=False, server_default=text("now()"))

    def __repr__(self) -> str:
        return f"<PositionStageAssignmentModel(id={self.id}, position_id={self.position_id}, stage_id={self.stage_id})>"
