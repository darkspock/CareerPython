from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, Integer, JSON, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.company.domain.enums import CompanyStatusEnum
from src.shared.domain.entities.base import generate_id


@dataclass
class CompanyModel(Base):
    """SQLAlchemy model for companies"""
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Remove FK constraint for now
    sector: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Number of employees
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Primary location
    website: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    culture: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # Values, mission, benefits
    external_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON,
                                                                    nullable=True)  # Enriched data (e.g., Glassdoor)
    status: Mapped[CompanyStatusEnum] = mapped_column(Enum(CompanyStatusEnum), nullable=False,
                                                      default=CompanyStatusEnum.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships - DISABLED
    # job_positions: Mapped[List["JobPositionModel"]] = relationship("JobPositionModel", back_populates="company")  # type: ignore

    def __repr__(self) -> str:
        return f"<CompanyModel(id={self.id}, name={self.name}, status={self.status})>"
