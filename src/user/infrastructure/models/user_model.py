from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.shared.domain.entities.base import generate_id


@dataclass
class UserModel(Base):
    """Modelo de SQLAlchemy para usuarios"""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    subscription_tier: Mapped[str] = mapped_column(String(20), nullable=False, default='FREE')
    subscription_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    password_reset_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password_reset_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(5), nullable=False, default='es')
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())

    # Relationships - DISABLED
    # assets: Mapped[List["UserAssetModel"]] = relationship("UserAssetModel", back_populates="user")
