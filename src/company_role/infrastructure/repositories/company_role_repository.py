"""Company Role Repository implementation."""
from typing import Optional, List, Any

from src.company_role.domain.entities.company_role import CompanyRole
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company.domain.value_objects.company_id import CompanyId
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.company_role.infrastructure.models.company_role_model import CompanyRoleModel
from src.shared.infrastructure.helpers.mixed_helper import MixedHelper


class CompanyRoleRepository(CompanyRoleRepositoryInterface):
    """Repository implementation for company role operations."""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, role: CompanyRole) -> None:
        """Save a company role."""
        model = self._to_model(role)
        with self._database.get_session() as session:
            existing = session.query(CompanyRoleModel).filter_by(id=str(role.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, role_id: CompanyRoleId) -> Optional[CompanyRole]:
        """Get role by ID."""
        with self._database.get_session() as session:
            model = session.query(CompanyRoleModel).filter_by(id=str(role_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_company(self, company_id: CompanyId, active_only: bool = False) -> List[CompanyRole]:
        """List all roles for a company."""
        with self._database.get_session() as session:
            query = session.query(CompanyRoleModel).filter_by(company_id=str(company_id))
            if active_only:
                query = query.filter_by(is_active=True)
            models = query.order_by(CompanyRoleModel.name).all()
            return [self._to_domain(model) for model in models]

    def delete(self, role_id: CompanyRoleId) -> None:
        """Delete a role."""
        with self._database.get_session() as session:
            session.query(CompanyRoleModel).filter_by(id=str(role_id)).delete()
            session.commit()

    def exists_by_name(self, company_id: CompanyId, name: str, exclude_id: Optional[CompanyRoleId] = None) -> bool:
        """Check if a role with the given name exists for the company."""
        with self._database.get_session() as session:
            query = session.query(CompanyRoleModel).filter_by(
                company_id=str(company_id),
                name=name.strip()
            )
            if exclude_id:
                query = query.filter(CompanyRoleModel.id != str(exclude_id))
            result: bool = MixedHelper.get_boolean(session.query(query.exists()).scalar())
            return result

    def _to_domain(self, model: CompanyRoleModel) -> CompanyRole:
        """Convert model to domain entity."""
        return CompanyRole(
            id=CompanyRoleId.from_string(model.id),
            company_id=CompanyId(model.company_id),
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CompanyRole) -> CompanyRoleModel:
        """Convert domain entity to model."""
        return CompanyRoleModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
