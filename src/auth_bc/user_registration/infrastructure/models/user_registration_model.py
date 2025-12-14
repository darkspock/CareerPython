from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, DateTime, Text, Integer, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.auth_bc.user_registration.domain.enums import RegistrationStatusEnum, ProcessingStatusEnum
from src.framework.domain.entities.base import generate_id


@dataclass
class UserRegistrationModel(Base):
    """SQLAlchemy model for user_registrations table"""
    __tablename__ = "user_registrations"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    verification_token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    token_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=RegistrationStatusEnum.PENDING.value,
        index=True
    )
    processing_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ProcessingStatusEnum.PENDING.value,
        index=True
    )

    # Optional references
    company_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    job_position_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    existing_user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)

    # PDF file data
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Extracted content
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extracted_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
