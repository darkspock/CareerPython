from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, Enum, DateTime, Text, Integer, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.framework.domain.entities.base import generate_id
from src.auth_bc.user.domain.enums.asset_enums import AssetTypeEnum, ProcessingStatusEnum


@dataclass
class UserAssetModel(Base):
    """Modelo de SQLAlchemy para assets de usuario"""
    __tablename__ = "user_assets"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)  # Removed ForeignKey
    asset_type: Mapped[AssetTypeEnum] = mapped_column(Enum(AssetTypeEnum), nullable=False, index=True)
    content: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    file_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    processing_status: Mapped[ProcessingStatusEnum] = mapped_column(
        Enum(ProcessingStatusEnum),
        nullable=False,
        default=ProcessingStatusEnum.PENDING,
        index=True
    )
    processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Relationships - DISABLED
    # user: Mapped["UserModel"] = relationship("UserModel", back_populates="assets")
