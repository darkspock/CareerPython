from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import func

from core.database import DatabaseInterface
from src.company.domain.entities.company import Company
from src.company.domain.enums import CompanyStatusEnum, CompanyTypeEnum
from src.company.domain.value_objects import CompanyId, CompanySettings
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.infrastructure.models.company_model import CompanyModel


class CompanyRepository(CompanyRepositoryInterface):
    """Company repository implementation"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, company: Company) -> None:
        """Save or update a company"""
        model = self._to_model(company)
        with self.database.get_session() as session:
            session.merge(model)
            session.commit()

    def get_by_id(self, company_id: CompanyId) -> Optional[Company]:
        """Get a company by ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyModel).filter(
                CompanyModel.id == str(company_id)
            ).first()
            return self._to_domain(model) if model else None

    def get_by_domain(self, domain: str) -> Optional[Company]:
        """Get a company by domain"""
        with self.database.get_session() as session:
            model = session.query(CompanyModel).filter(
                CompanyModel.domain == domain.lower()
            ).first()
            return self._to_domain(model) if model else None

    def get_by_slug(self, slug: str) -> Optional[Company]:
        """Get a company by slug"""
        with self.database.get_session() as session:
            model = session.query(CompanyModel).filter(
                CompanyModel.slug == slug
            ).first()
            return self._to_domain(model) if model else None

    def list_all(self) -> List[Company]:
        """List all companies"""
        with self.database.get_session() as session:
            models = session.query(CompanyModel).all()
            return [self._to_domain(m) for m in models]

    def list_active(self) -> List[Company]:
        """List all active companies"""
        with self.database.get_session() as session:
            models = session.query(CompanyModel).filter(
                CompanyModel.status == CompanyStatusEnum.ACTIVE.value
            ).all()
            return [self._to_domain(m) for m in models]

    def delete(self, company_id: CompanyId) -> None:
        """Delete a company"""
        with self.database.get_session() as session:
            session.query(CompanyModel).filter(
                CompanyModel.id == str(company_id)
            ).delete()
            session.commit()

    def count_by_status(self, status: CompanyStatusEnum) -> int:
        """Count companies by status"""
        with self.database.get_session() as session:
            return session.query(func.count(CompanyModel.id)).filter(
                CompanyModel.status == status.value
            ).scalar() or 0

    def count_total(self) -> int:
        """Count total companies"""
        with self.database.get_session() as session:
            return session.query(func.count(CompanyModel.id)).scalar() or 0

    def count_recent(self, days: int = 30) -> int:
        """Count companies created in last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        with self.database.get_session() as session:
            return session.query(func.count(CompanyModel.id)).filter(
                CompanyModel.created_at >= cutoff_date
            ).scalar() or 0

    def _to_domain(self, model: CompanyModel) -> Company:
        """Convert model to domain entity"""
        return Company(
            id=CompanyId.from_string(model.id),
            name=model.name,
            domain=model.domain,
            slug=model.slug,
            logo_url=model.logo_url,
            settings=CompanySettings.from_dict(model.settings or {}),
            status=CompanyStatusEnum(model.status),
            company_type=CompanyTypeEnum(model.company_type) if model.company_type else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Company) -> CompanyModel:
        """Convert domain entity to model"""
        return CompanyModel(
            id=str(entity.id),
            name=entity.name,
            domain=entity.domain,
            slug=entity.slug,
            logo_url=entity.logo_url,
            settings=entity.settings.to_dict(),
            status=entity.status.value,
            company_type=entity.company_type.value if entity.company_type else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
