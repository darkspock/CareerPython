from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company.domain.enums import CompanyStatusEnum, CompanyTypeEnum
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
    slug: Optional[str]  # URL-friendly identifier for public pages
    logo_url: Optional[str]
    settings: CompanySettings
    status: CompanyStatusEnum
    company_type: Optional[CompanyTypeEnum]  # Company type for onboarding customization
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
            cls,
            id: CompanyId,
            name: str,
            domain: str,
            slug: Optional[str] = None,
            logo_url: Optional[str] = None,
            settings: Optional[CompanySettings] = None,
            company_type: Optional[CompanyTypeEnum] = None,
    ) -> "Company":
        """
        Factory method to create a new company

        Args:
            id: Company ID (required, must be provided from outside)
            name: Company name
            domain: Corporate domain (e.g., "company.com")
            slug: URL-friendly identifier (optional, auto-generated from name if not provided)
            logo_url: Logo URL (optional)
            settings: Custom settings (optional)
            company_type: Company type for onboarding customization (optional, defaults to MID_SIZE)

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

        # Generate slug if not provided
        if not slug:
            slug = name.strip().lower().replace(" ", "-").replace("_", "-")
            # Remove special characters
            slug = "".join(c for c in slug if c.isalnum() or c == "-")

        # Validate slug format
        if slug and not slug.replace("-", "").isalnum():
            raise CompanyValidationError("Slug can only contain letters, numbers, and hyphens")

        # Default values
        now = datetime.utcnow()
        company_settings = settings or CompanySettings.default()
        company_type_value = company_type or CompanyTypeEnum.MID_SIZE

        return cls(
            id=id,
            name=name.strip(),
            domain=domain.strip().lower(),
            slug=slug,
            logo_url=logo_url,
            settings=company_settings,
            status=CompanyStatusEnum.ACTIVE,
            company_type=company_type_value,
            created_at=now,
            updated_at=now,
        )

    def update(
            self,
            name: str,
            domain: str,
            slug: Optional[str],
            logo_url: Optional[str],
            settings: CompanySettings,
    ) -> "Company":
        """
        Updates the company with new values
        Returns a new instance (immutability)

        Args:
            name: New name
            domain: New domain
            slug: New slug (URL-friendly identifier)
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

        # Validate slug format if provided
        if slug and not slug.replace("-", "").isalnum():
            raise CompanyValidationError("Slug can only contain letters, numbers, and hyphens")

        # Return new instance
        return Company(
            id=self.id,
            name=name.strip(),
            domain=domain.strip().lower(),
            slug=slug,
            logo_url=logo_url,
            settings=settings,
            status=self.status,
            company_type=self.company_type,
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
            slug=self.slug,
            logo_url=self.logo_url,
            settings=self.settings,
            status=CompanyStatusEnum.SUSPENDED,
            company_type=self.company_type,
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
