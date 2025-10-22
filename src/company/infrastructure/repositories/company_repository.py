from typing import Optional, List
from sqlalchemy.orm import Session

from src.company.domain.entities.company import Company
from src.company.domain.enums import CompanyStatusEnum
from src.company.domain.value_objects import CompanyId, CompanySettings
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.infrastructure.models.company_model import CompanyModel


class CompanyRepository(CompanyRepositoryInterface):
    """Company repository implementation"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, company: Company) -> None:
        """Save or update a company"""
        model = self._to_model(company)
        self.session.merge(model)
        self.session.flush()

    def get_by_id(self, company_id: CompanyId) -> Optional[Company]:
        """Get a company by ID"""
        model = self.session.query(CompanyModel).filter(
            CompanyModel.id == str(company_id)
        ).first()
        return self._to_domain(model) if model else None

    def get_by_domain(self, domain: str) -> Optional[Company]:
        """Get a company by domain"""
        model = self.session.query(CompanyModel).filter(
            CompanyModel.domain == domain.lower()
        ).first()
        return self._to_domain(model) if model else None

    def list_all(self) -> List[Company]:
        """List all companies"""
        models = self.session.query(CompanyModel).all()
        return [self._to_domain(m) for m in models]

    def list_active(self) -> List[Company]:
        """List all active companies"""
        models = self.session.query(CompanyModel).filter(
            CompanyModel.status == CompanyStatusEnum.ACTIVE.value
        ).all()
        return [self._to_domain(m) for m in models]

    def delete(self, company_id: CompanyId) -> None:
        """Delete a company"""
        self.session.query(CompanyModel).filter(
            CompanyModel.id == str(company_id)
        ).delete()
        self.session.flush()

    def _to_domain(self, model: CompanyModel) -> Company:
        """Convert model to domain entity"""
        return Company(
            id=CompanyId.from_string(model.id),
            name=model.name,
            domain=model.domain,
            logo_url=model.logo_url,
            settings=CompanySettings.from_dict(model.settings or {}),
            status=CompanyStatusEnum(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Company) -> CompanyModel:
        """Convert domain entity to model"""
        return CompanyModel(
            id=str(entity.id),
            name=entity.name,
            domain=entity.domain,
            logo_url=entity.logo_url,
            settings=entity.settings.to_dict(),
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
