from sqlalchemy import Column, String, Boolean, DateTime, Text, Index, JSON
from core.database import Base
from datetime import datetime


class InAppNotificationModel(Base):
    """SQLAlchemy model for in-app notifications"""

    __tablename__ = "in_app_notifications"

    id = Column(String(26), primary_key=True)  # ULID
    user_id = Column(String(26), nullable=False, index=True)
    company_id = Column(String(26), nullable=False, index=True)
    notification_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False, default="NORMAL")
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    link = Column(String(500), nullable=True)
    notification_metadata = Column("metadata", JSON, nullable=True)

    # Composite index for efficient user notification queries
    __table_args__ = (
        Index('ix_in_app_notifications_user_company', 'user_id', 'company_id'),
        Index('ix_in_app_notifications_user_unread', 'user_id', 'company_id', 'is_read'),
        Index('ix_in_app_notifications_created', 'user_id', 'company_id', 'created_at'),
    )
