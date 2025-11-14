"""Command and handler for registering a company with a new user"""
from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.exceptions.user_exceptions import EmailAlreadyExistException
from src.company_bc.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyValidationError, CompanyDomainAlreadyExistsError
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company_bc.company.domain.entities.company_user import CompanyUser
from src.company_bc.company.domain.value_objects import CompanyUserId
from src.company_bc.company.domain.enums import CompanyUserRole, CompanyTypeEnum
from src.company_bc.company.application.commands.create_company_command import CreateCompanyCommand
from src.company_bc.company.application.commands.initialize_onboarding_command import InitializeOnboardingCommand
from src.company_bc.company.application.commands.initialize_sample_data_command import InitializeSampleDataCommand
from src.shared_bc.customization.phase.application.commands.initialize_company_phases_command import InitializeCompanyPhasesCommand

import logging

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RegisterCompanyWithUserCommand(Command):
    """Command to register a new company with a new user"""
    
    # User data
    user_id: UserId
    user_email: str
    user_password: str
    user_full_name: str
    
    # Company data
    company_id: CompanyId
    company_name: str
    company_domain: str
    company_logo_url: Optional[str] = None
    company_contact_phone: Optional[str] = None
    company_address: Optional[str] = None
    company_type: Optional[CompanyTypeEnum] = None  # Company type for onboarding customization
    
    # Options
    initialize_workflows: bool = True   # Whether to initialize default workflows
    include_example_data: bool = False  # Whether to include sample data


class RegisterCompanyWithUserCommandHandler(CommandHandler[RegisterCompanyWithUserCommand]):
    """Handler for registering a company with a new user"""
    
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
    
    def execute(self, command: RegisterCompanyWithUserCommand) -> None:
        """
        Execute the registration command
        
        Steps:
        1. Create new user
        2. Create new company
        3. Link user to company with ADMIN role
        4. Initialize onboarding (roles + pages) - ALWAYS
        5. Initialize workflows - CONDITIONAL (if initialize_workflows=True)
        6. Initialize sample data - CONDITIONAL (if include_example_data=True)
        """
        log.info(f"RegisterCompanyWithUserCommand called with email: {command.user_email}, domain: {command.company_domain}")
        
        try:
            # Step 1: Validate and create user
            existing_user = self.user_repository.get_by_email(command.user_email)
            if existing_user:
                raise EmailAlreadyExistException(command.user_email)
            
            # Hash password
            hashed_password = PasswordService.hash_password(command.user_password)
            
            # Create user entity
            user = User(
                id=command.user_id,
                email=command.user_email,
                hashed_password=hashed_password,
                is_active=True
            )
            self.user_repository.create(user)
            log.info(f"User created successfully: {command.user_email}")
            
            # Step 2: Validate domain before creating company
            # TODO: Re-enable domain uniqueness check when needed
            # existing_company = self.company_repository.get_by_domain(command.company_domain)
            # if existing_company:
            #     raise CompanyDomainAlreadyExistsError(f"Company with domain {command.company_domain} already exists")
            
            # Prepare company settings (include contact info if provided)
            company_settings: Dict[str, Any] = {}
            if command.company_contact_phone:
                company_settings["contact_phone"] = command.company_contact_phone
            if command.company_address:
                company_settings["address"] = command.company_address
            if command.user_full_name:
                company_settings["owner_name"] = command.user_full_name
            if command.include_example_data:
                company_settings["include_example_data"] = True
            
            # Create company using CreateCompanyCommand
            create_company_command = CreateCompanyCommand(
                id=str(command.company_id.value),
                name=command.company_name,
                domain=command.company_domain,
                logo_url=command.company_logo_url,
                settings=company_settings if company_settings else None,
                company_type=command.company_type,
            )
            self.command_bus.dispatch(create_company_command)
            log.info(f"Company created successfully: {command.company_name} ({command.company_domain})")
            
            # Step 3: Link user to company with ADMIN role
            company_user_id = CompanyUserId.generate()
            company_user = CompanyUser.create(
                id=company_user_id,
                company_id=command.company_id,
                user_id=command.user_id,
                role=CompanyUserRole.ADMIN,  # First user is always ADMIN
                permissions=None,  # Will use default ADMIN permissions
            )
            self.company_user_repository.save(company_user)
            log.info(f"Company user relationship created: {command.user_email} -> {command.company_name} (Role: ADMIN)")
            
            # Step 4: Initialize onboarding (ALWAYS) - roles and pages
            onboarding_command = InitializeOnboardingCommand(
                company_id=command.company_id,
                create_roles=True,
                create_pages=True
            )
            self.command_bus.dispatch(onboarding_command)
            log.info(f"Onboarding initialized for company: {command.company_name}")
            
            # Step 5: Initialize workflows (CONDITIONAL)
            if command.initialize_workflows:
                workflows_command = InitializeCompanyPhasesCommand(
                    company_id=command.company_id
                )
                self.command_bus.dispatch(workflows_command)
                log.info(f"Workflows initialized for company: {command.company_name}")
            
            # Step 6: Initialize sample data (CONDITIONAL)
            if command.include_example_data:
                sample_data_command = InitializeSampleDataCommand(
                    company_id=command.company_id,
                    company_user_id=company_user_id,
                    num_candidates=50,
                    num_recruiters=3,
                    num_viewers=2
                )
                self.command_bus.dispatch(sample_data_command)
                log.info(f"Sample data initialized for company: {command.company_name}")
            
            log.info(f"Company registration completed successfully: {command.company_name}")
            
        except (EmailAlreadyExistException, CompanyDomainAlreadyExistsError, CompanyValidationError):
            # Re-raise domain exceptions
            raise
        except Exception as e:
            log.error(f"Error in RegisterCompanyWithUserCommand: {str(e)}")
            raise CompanyValidationError(f"Failed to register company: {str(e)}")

