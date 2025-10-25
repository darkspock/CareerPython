"""Company Role entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company.domain.value_objects.company_id import CompanyId


@dataclass(frozen=True)
class CompanyRole:
    """Company role entity - defines roles within a company for workflow assignment."""
    id: CompanyRoleId
    company_id: CompanyId
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: CompanyRoleId,
        company_id: CompanyId,
        name: str,
        description: Optional[str] = None,
        is_active: bool = True
    ) -> "CompanyRole":
        """Factory method to create a new company role."""
        if not name or not name.strip():
            raise ValueError("Role name cannot be empty")

        if len(name) > 100:
            raise ValueError("Role name cannot exceed 100 characters")

        now = datetime.utcnow()
        return CompanyRole(
            id=id,
            company_id=company_id,
            name=name.strip(),
            description=description.strip() if description else None,
            is_active=is_active,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        name: str,
        description: Optional[str] = None
    ) -> "CompanyRole":
        """Update role information."""
        if not name or not name.strip():
            raise ValueError("Role name cannot be empty")

        if len(name) > 100:
            raise ValueError("Role name cannot exceed 100 characters")

        return CompanyRole(
            id=self.id,
            company_id=self.company_id,
            name=name.strip(),
            description=description.strip() if description else None,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def activate(self) -> "CompanyRole":
        """Activate this role."""
        return CompanyRole(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            is_active=True,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def deactivate(self) -> "CompanyRole":
        """Deactivate this role."""
        return CompanyRole(
            id=self.id,
            company_id=self.company_id,
            name=self.name,
            description=self.description,
            is_active=False,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
