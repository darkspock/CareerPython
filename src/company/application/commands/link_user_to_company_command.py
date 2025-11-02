"""Command and handler for linking an existing user to a new company"""
from dataclasses import dataclass
from typing import Optional

from src.shared.application.command_bus import Command, CommandHandler, CommandBus
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.user.domain.value_objects.UserId import UserId
from src.user.domain.entities.user import User
from src.user.domain.services.password_service import PasswordService
from src.user.domain.exceptions.user_exceptions import UserNotFoundException
from src.company.domain.repositories.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.value_objects import CompanyId
from src.company.domain.exceptions.company_exceptions import CompanyValidationError, CompanyDomainAlreadyExistsError
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.value_objects import CompanyUserId
from src.company.domain.enums import CompanyUserRole
from src.company.application.commands.create_company_command import CreateCompanyCommand

import logging

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class LinkUserToCompanyCommand(Command):
    """Command to link an existing user to a new company"""
    
    # User authentication
    user_email: str
    user_password: str
    
    # Company data
    company_id: CompanyId
    company_name: str
    company_domain: str
    company_logo_url: Optional[str] = None
    company_contact_phone: Optional[str] = None
    company_address: Optional[str] = None
    
    # Options
    include_example_data: bool = False


class LinkUserToCompanyCommandHandler(CommandHandler[LinkUserToCompanyCommand]):
    """Handler for linking an existing user to a new company"""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        company_repository: CompanyRepositoryInterface,
        company_user_repository: CompanyUserRepositoryInterface,
        command_bus: CommandBus,
    ):
        self.user_repository = user_repository
        self.company_repository = company_repository
        self.company_user_repository = company_user_repository
        self.command_bus = command_bus
    
    def execute(self, command: LinkUserToCompanyCommand) -> None:
        """
        Execute the link user command
        
        Steps:
        1. Authenticate user (validate email and password)
        2. Create new company (this automatically initializes phases and workflows)
        3. Link user to company with ADMIN role
        """
        log.info(f"LinkUserToCompanyCommand called with email: {command.user_email}, domain: {command.company_domain}")
        
        try:
            # Step 1: Authenticate user
            user = self.user_repository.get_by_email(command.user_email)
            if not user:
                raise UserNotFoundException(f"User with email {command.user_email} not found")
            
            # Verify password
            if not PasswordService.verify_password(command.user_password, user.hashed_password):
                raise CompanyValidationError("Invalid email or password")
            
            log.info(f"User authenticated successfully: {command.user_email}")
            
            # Step 2: Validate domain before creating company
            existing_company = self.company_repository.get_by_domain(command.company_domain)
            if existing_company:
                raise CompanyDomainAlreadyExistsError(f"Company with domain {command.company_domain} already exists")
            
            # Prepare company settings
            company_settings = {}
            if command.company_contact_phone:
                company_settings["contact_phone"] = command.company_contact_phone
            if command.company_address:
                company_settings["address"] = command.company_address
            if command.include_example_data:
                company_settings["include_example_data"] = True
            
            # Create company using CreateCompanyCommand (this will trigger InitializeCompanyPhasesCommand automatically)
            create_company_command = CreateCompanyCommand(
                id=str(command.company_id.value),
                name=command.company_name,
                domain=command.company_domain,
                logo_url=command.company_logo_url,
                settings=company_settings if company_settings else None,
            )
            self.command_bus.dispatch(create_company_command)
            log.info(f"Company created successfully: {command.company_name} ({command.company_domain})")
            
            # Step 3: Link user to company with ADMIN role
            company_user_id = CompanyUserId.generate()
            company_user = CompanyUser.create(
                id=company_user_id,
                company_id=command.company_id,
                user_id=user.id,
                role=CompanyUserRole.ADMIN,  # First user is always ADMIN
                permissions=None,  # Will use default ADMIN permissions
            )
            self.company_user_repository.save(company_user)
            log.info(f"Company user relationship created: {command.user_email} -> {command.company_name} (Role: ADMIN)")
            
            log.info(f"User linked to company successfully: {command.company_name}")
            
        except (UserNotFoundException, CompanyDomainAlreadyExistsError, CompanyValidationError):
            # Re-raise domain exceptions
            raise
        except Exception as e:
            log.error(f"Error in LinkUserToCompanyCommand: {str(e)}")
            raise CompanyValidationError(f"Failed to link user to company: {str(e)}")

