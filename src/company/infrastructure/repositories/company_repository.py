from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import or_

from core.database import DatabaseInterface
from src.company.domain.entities.company import Company
from src.company.domain.enums import CompanyStatusEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.company.infrastructure.models.company_model import CompanyModel
from src.user.domain.value_objects.UserId import UserId


class CompanyRepositoryInterface(ABC):
    @abstractmethod
    def save(self, company: Company) -> Company:
        pass

    @abstractmethod
    def get_by_id(self, company_id: str) -> Optional[Company]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[Company]:
        pass

    @abstractmethod
    def find_by_filters(self, status: Optional[CompanyStatusEnum] = None,
                        sector: Optional[str] = None,
                        location: Optional[str] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0) -> List[Company]:
        pass

    @abstractmethod
    def count_by_status(self, status: CompanyStatusEnum) -> int:
        pass

    @abstractmethod
    def count_total(self) -> int:
        pass

    @abstractmethod
    def count_recent(self, days: int = 30) -> int:
        pass

    @abstractmethod
    def delete(self, company_id: str) -> bool:
        pass


class CompanyRepository(CompanyRepositoryInterface):
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, company: Company) -> Company:
        """Save or update company"""
        with self.database.get_session() as session:
            company_model = session.query(CompanyModel).filter(
                CompanyModel.id == company.id.value
            ).first()

            if company_model:
                # Update existing
                self._update_model_from_entity(company_model, company)
            else:
                # Create new
                company_model = self._create_model_from_entity(company)
                session.add(company_model)

            session.commit()
            session.refresh(company_model)

            return self._create_entity_from_model(company_model)

    def get_by_id(self, company_id: str) -> Optional[Company]:
        """Get company by ID"""
        with self.database.get_session() as session:
            company_model = session.query(CompanyModel).filter(
                CompanyModel.id == company_id
            ).first()

            if not company_model:
                return None

            return self._create_entity_from_model(company_model)

    def get_by_user_id(self, user_id: str) -> Optional[Company]:
        """Get company by user ID"""
        with self.database.get_session() as session:
            company_model = session.query(CompanyModel).filter(
                CompanyModel.user_id == user_id
            ).first()

            if not company_model:
                return None

            return self._create_entity_from_model(company_model)

    def find_by_filters(self, status: Optional[CompanyStatusEnum] = None,
                        sector: Optional[str] = None,
                        location: Optional[str] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0) -> List[Company]:
        """Find companies by filters"""
        with self.database.get_session() as session:
            query = session.query(CompanyModel)

            # Apply filters
            if status:
                query = query.filter(CompanyModel.status == status)

            if sector:
                query = query.filter(CompanyModel.sector.ilike(f"%{sector}%"))

            if location:
                query = query.filter(CompanyModel.location.ilike(f"%{location}%"))

            if search_term:
                query = query.filter(
                    or_(
                        CompanyModel.name.ilike(f"%{search_term}%"),
                        CompanyModel.sector.ilike(f"%{search_term}%"),
                        CompanyModel.location.ilike(f"%{search_term}%")
                    )
                )

            # Order by name asc (must be before pagination)
            query = query.order_by(CompanyModel.name.asc())

            # Apply pagination
            query = query.offset(offset).limit(limit)

            company_models = query.all()
            return [self._create_entity_from_model(model) for model in company_models]

    def count_by_status(self, status: CompanyStatusEnum) -> int:
        """Count companies by status"""
        with self.database.get_session() as session:
            return session.query(CompanyModel).filter(
                CompanyModel.status == status
            ).count()

    def count_total(self) -> int:
        """Count total companies"""
        with self.database.get_session() as session:
            return session.query(CompanyModel).count()

    def count_recent(self, days: int = 30) -> int:
        """Count companies created in the last N days"""
        with self.database.get_session() as session:
            since_date = datetime.utcnow() - timedelta(days=days)
            return session.query(CompanyModel).filter(
                CompanyModel.created_at >= since_date
            ).count()

    def delete(self, company_id: str) -> bool:
        """Delete company"""
        with self.database.get_session() as session:
            company_model = session.query(CompanyModel).filter(
                CompanyModel.id == company_id
            ).first()

            if not company_model:
                return False

            session.delete(company_model)
            session.commit()
            return True

    def _create_entity_from_model(self, model: CompanyModel) -> Company:
        """Convert CompanyModel to Company entity"""
        return Company(
            id=CompanyId.from_string(str(model.id)),
            user_id=UserId.from_string_or_null(model.user_id),
            name=model.name,
            sector=model.sector,
            size=model.size,
            location=model.location,
            website=model.website,
            culture=model.culture,
            external_data=model.external_data,
            status=CompanyStatusEnum(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _create_model_from_entity(self, company: Company) -> CompanyModel:
        """Create CompanyModel from Company entity"""
        return CompanyModel(
            id=company.id.value,
            user_id=company.user_id.value if company.user_id else None,
            name=company.name,
            sector=company.sector,
            size=company.size,
            location=company.location,
            website=company.website,
            culture=company.culture,
            external_data=company.external_data,
            status=company.status,
            created_at=company.created_at,
            updated_at=company.updated_at
        )

    def _update_model_from_entity(self, model: CompanyModel, company: Company) -> None:
        """Update CompanyModel with Company entity data"""
        model.name = company.name
        model.sector = company.sector
        model.size = company.size
        model.location = company.location
        model.website = company.website
        model.culture = company.culture
        model.external_data = company.external_data
        model.status = company.status
        model.updated_at = company.updated_at
