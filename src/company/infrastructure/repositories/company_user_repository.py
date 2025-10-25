from typing import Optional, List

from core.database import DatabaseInterface
from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.enums import CompanyUserRole, CompanyUserStatus
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.infrastructure.models.company_user_model import CompanyUserModel
from src.user.domain.value_objects.UserId import UserId


class CompanyUserRepository(CompanyUserRepositoryInterface):
    """Company user repository implementation"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, company_user: CompanyUser) -> None:
        """Save or update a company user"""
        model = self._to_model(company_user)
        with self.database.get_session() as session:
            session.merge(model)
            session.commit()

    def get_by_id(self, company_user_id: CompanyUserId) -> Optional[CompanyUser]:
        """Get a company user by ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyUserModel).filter(
                CompanyUserModel.id == str(company_user_id)
            ).first()
            return self._to_domain(model) if model else None

    def get_by_company_and_user(
        self,
        company_id: CompanyId,
        user_id: UserId
    ) -> Optional[CompanyUser]:
        """Get a company user by company and user ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyUserModel).filter(
                CompanyUserModel.company_id == str(company_id),
                CompanyUserModel.user_id == str(user_id)
            ).first()
            return self._to_domain(model) if model else None

    def list_by_company(self, company_id: CompanyId) -> List[CompanyUser]:
        """List all users for a company"""
        with self.database.get_session() as session:
            models = session.query(CompanyUserModel).filter(
                CompanyUserModel.company_id == str(company_id)
            ).all()
            return [self._to_domain(m) for m in models]

    def list_active_by_company(self, company_id: CompanyId) -> List[CompanyUser]:
        """List all active users for a company"""
        with self.database.get_session() as session:
            models = session.query(CompanyUserModel).filter(
                CompanyUserModel.company_id == str(company_id),
                CompanyUserModel.status == CompanyUserStatus.ACTIVE.value
            ).all()
            return [self._to_domain(m) for m in models]

    def delete(self, company_user_id: CompanyUserId) -> None:
        """Delete a company user"""
        with self.database.get_session() as session:
            session.query(CompanyUserModel).filter(
                CompanyUserModel.id == str(company_user_id)
            ).delete()
            session.commit()

    def get_by_user_id(self, user_id: UserId) -> Optional[CompanyUser]:
        """Get a company user by user ID"""
        with self.database.get_session() as session:
            model = session.query(CompanyUserModel).filter(
                CompanyUserModel.user_id == str(user_id)
            ).first()
            return self._to_domain(model) if model else None

    def _to_domain(self, model: CompanyUserModel) -> CompanyUser:
        """Convert model to domain entity"""
        return CompanyUser(
            id=CompanyUserId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            user_id=UserId.from_string(model.user_id),
            role=CompanyUserRole(model.role),
            permissions=CompanyUserPermissions.from_dict(model.permissions or {}),
            status=CompanyUserStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CompanyUser) -> CompanyUserModel:
        """Convert domain entity to model"""
        return CompanyUserModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            user_id=str(entity.user_id),
            role=entity.role.value,
            permissions=entity.permissions.to_dict(),
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
