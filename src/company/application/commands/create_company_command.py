from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.entities.company import Company
from src.company.domain.value_objects import CompanyId, CompanySettings
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyValidationError


@dataclass
class CreateCompanyCommand:
    """Command to create a new company"""
    id: str
    name: str
    domain: str
    logo_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class CreateCompanyCommandHandler:
    """Handler for creating a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def handle(self, command: CreateCompanyCommand) -> None:
        """Execute the command - NO return value"""
        # Check if domain already exists
        existing = self.repository.get_by_domain(command.domain)
        if existing:
            raise CompanyValidationError(f"Company with domain {command.domain} already exists")

        # Create entity using factory method
        company = Company.create(
            id=CompanyId.from_string(command.id),
            name=command.name,
            domain=command.domain,
            logo_url=command.logo_url,
            settings=CompanySettings.from_dict(command.settings) if command.settings else None,
        )

        # Persist
        self.repository.save(company)
