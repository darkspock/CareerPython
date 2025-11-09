from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.entities.company import Company
from src.company.domain.value_objects import CompanyId, CompanySettings
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.shared.application.command_bus import Command, CommandHandler, CommandBus
from src.phase.application.commands.initialize_company_phases_command import InitializeCompanyPhasesCommand


@dataclass
class CreateCompanyCommand(Command):
    """Command to create a new company"""
    id: str
    name: str
    domain: str
    logo_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class CreateCompanyCommandHandler(CommandHandler):
    """Handler for creating a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateCompanyCommand) -> None:
        """Execute the command - NO return value
        
        Note: This command ONLY creates the company entity.
        Workflow initialization should be called explicitly by the caller
        using InitializeOnboardingCommand and InitializeCompanyPhasesCommand.
        """
        # TODO: Re-enable domain uniqueness check when needed
        # Check if domain already exists
        # existing = self.repository.get_by_domain(command.domain)
        # if existing:
        #     raise CompanyValidationError(f"Company with domain {command.domain} already exists")

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
