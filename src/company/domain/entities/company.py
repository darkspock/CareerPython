from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.domain.enums import CompanyStatusEnum
from src.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company.domain.value_objects import CompanyId, CompanySettings


@dataclass
class Company:
    """
    Company domain entity
    Represents a recruiting company that uses the platform to manage candidates
    """
    id: CompanyId
    name: str
    domain: str
    logo_url: Optional[str]
    settings: CompanySettings
    status: CompanyStatusEnum
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: CompanyId,
            name: str,
            domain: str,
            logo_url: Optional[str] = None,
            settings: Optional[CompanySettings] = None,
    ) -> "Company":
        """
        Factory method to create a new company

        Args:
            id: Company ID (required, must be provided from outside)
            name: Company name
            domain: Corporate domain (e.g., "company.com")
            logo_url: Logo URL (optional)
            settings: Custom settings (optional)

        Returns:
            Company: New company instance

        Raises:
            CompanyValidationError: If data is invalid
        """
        # Business validations
        if not name or len(name.strip()) < 3:
            raise CompanyValidationError("Name must be at least 3 characters")

        if not domain or len(domain.strip()) < 3:
            raise CompanyValidationError("Domain is required")

        # Validate domain doesn't contain @
        if "@" in domain:
            raise CompanyValidationError("Domain must not contain @")

        # Default values
        now = datetime.utcnow()
        company_settings = settings or CompanySettings.default()

        return cls(
            id=id,
            name=name.strip(),
            domain=domain.strip().lower(),
            logo_url=logo_url,
            settings=company_settings,
            status=CompanyStatusEnum.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def update(
            self,
            name: str,
            domain: str,
            logo_url: Optional[str],
            settings: CompanySettings,
    ) -> "Company":
        """
        Updates the company with new values
        Returns a new instance (immutability)

        Args:
            name: New name
            domain: New domain
            logo_url: New logo URL
            settings: New settings

        Returns:
            Company: New instance with updated data

        Raises:
            CompanyValidationError: If data is invalid
        """
        # Validations
        if not name or len(name.strip()) < 3:
            raise CompanyValidationError("Name must be at least 3 characters")

        if not domain or len(domain.strip()) < 3:
            raise CompanyValidationError("Domain is required")

        if "@" in domain:
            raise CompanyValidationError("Domain must not contain @")

        # Return new instance
        return Company(
            id=self.id,
            name=name.strip(),
            domain=domain.strip().lower(),
            logo_url=logo_url,
            settings=settings,
            status=self.status,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def suspend(self, reason: Optional[str] = None) -> "Company":
        """
        Suspends the company

        Args:
            reason: Suspension reason (optional)

        Returns:
            Company: New instance with SUSPENDED status

        Raises:
            CompanyValidationError: If company is already deleted
        """
        if self.status == CompanyStatusEnum.DELETED:
            raise CompanyValidationError("Cannot suspend a deleted company")

        return Company(
            id=self.id,
            name=self.name,
            domain=self.domain,
            logo_url=self.logo_url,
            settings=self.settings,
            status=CompanyStatusEnum.SUSPENDED,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def activate(self) -> None:
        """
        Activates the company

        Raises:
            CompanyValidationError: If company is deleted
        """
        if self.status == CompanyStatusEnum.DELETED:
            raise CompanyValidationError("Cannot activate a deleted company")

        self.status = CompanyStatusEnum.ACTIVE

    def delete(self) -> None:
        """
        Marks the company as deleted (soft delete)

        Returns:
            Company: New instance with DELETED status
        """
        self.status = CompanyStatusEnum.DELETED

    def is_active(self) -> bool:
        """Checks if company is active"""
        return self.status == CompanyStatusEnum.ACTIVE

    def is_suspended(self) -> bool:
        """Checks if company is suspended"""
        return self.status == CompanyStatusEnum.SUSPENDED

    def is_deleted(self) -> bool:
        """Checks if company is deleted"""
        return self.status == CompanyStatusEnum.DELETED
