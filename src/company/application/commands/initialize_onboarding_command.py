"""Initialize Onboarding Command - Creates default roles and pages for a new company"""
from dataclasses import dataclass
import logging

from src.shared.application.command_bus import Command, CommandHandler, CommandBus
from src.company.domain.value_objects.company_id import CompanyId
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_role.application.commands.create_role_command import CreateRoleCommand
from src.company_page.application.commands.create_company_page_command import CreateCompanyPageCommand
from src.company_page.domain.enums.page_type import PageType

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class InitializeOnboardingCommand(Command):
    """Command to initialize onboarding for a new company
    
    Creates:
    - 7 default company roles (HR Manager, Recruiter, Tech Lead, etc.)
    - 5 default company pages in DRAFT status (empty)
    """
    company_id: CompanyId
    create_pages: bool = True  # Whether to create default pages
    create_roles: bool = True  # Whether to create default roles


class InitializeOnboardingCommandHandler(CommandHandler[InitializeOnboardingCommand]):
    """Handler for initializing onboarding for a new company"""
    
    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus
    
    def execute(self, command: InitializeOnboardingCommand) -> None:
        """Execute the onboarding initialization command"""
        log.info(f"Initializing onboarding for company: {command.company_id.value}")
        
        # Create default roles
        if command.create_roles:
            self._create_default_roles(command.company_id)
        
        # Create default pages
        if command.create_pages:
            self._create_default_pages(command.company_id)
        
        log.info(f"Onboarding initialization completed for company: {command.company_id.value}")
    
    def _create_default_roles(self, company_id: CompanyId) -> None:
        """Create 7 default company roles"""
        roles_to_create = [
            {
                "name": "HR Manager",
                "description": "Oversees recruitment strategy, candidate communication, and offer stages."
            },
            {
                "name": "Recruiter",
                "description": "Handles sourcing, screening, and initial candidate engagement."
            },
            {
                "name": "Tech Lead",
                "description": "Evaluates technical skills during assessments or interviews."
            },
            {
                "name": "Hiring Manager",
                "description": "Manages the position-specific hiring process and makes final decisions."
            },
            {
                "name": "Interviewer",
                "description": "Conducts specific interviews (e.g., technical or cultural fit)."
            },
            {
                "name": "Department Head",
                "description": "Provides high-level approval, often in final stages."
            },
            {
                "name": "CTO",
                "description": "Participates in senior-level or technical hiring decisions."
            }
        ]
        
        for role_data in roles_to_create:
            try:
                role_id = CompanyRoleId.generate()
                create_role_command = CreateRoleCommand(
                    id=role_id,
                    company_id=company_id.value,
                    name=role_data["name"],
                    description=role_data["description"]
                )
                self.command_bus.dispatch(create_role_command)
                log.debug(f"Created role: {role_data['name']} for company {company_id.value}")
            except Exception as e:
                # Log error but continue with other roles
                # The CreateRoleCommandHandler will check if role already exists
                log.warning(f"Failed to create role '{role_data['name']}': {e}")
                continue
    
    def _create_default_pages(self, company_id: CompanyId) -> None:
        """Create 5 default company pages in DRAFT status with empty content"""
        pages_to_create = [
            {
                "page_type": PageType.PUBLIC_COMPANY_DESCRIPTION.value,
                "title": "About Our Company",
                "html_content": "",
                "meta_description": None,
                "meta_keywords": [],
                "language": "es",
                "is_default": True
            },
            {
                "page_type": PageType.JOB_POSITION_DESCRIPTION.value,
                "title": "Job Position Description",
                "html_content": "",
                "meta_description": None,
                "meta_keywords": [],
                "language": "es",
                "is_default": True
            },
            {
                "page_type": PageType.DATA_PROTECTION.value,
                "title": "Data Protection",
                "html_content": "",
                "meta_description": None,
                "meta_keywords": [],
                "language": "es",
                "is_default": True
            },
            {
                "page_type": PageType.TERMS_OF_USE.value,
                "title": "Terms of Use",
                "html_content": "",
                "meta_description": None,
                "meta_keywords": [],
                "language": "es",
                "is_default": True
            },
            {
                "page_type": PageType.THANK_YOU_APPLICATION.value,
                "title": "Thank You for Your Application",
                "html_content": "",
                "meta_description": None,
                "meta_keywords": [],
                "language": "es",
                "is_default": True
            }
        ]
        
        for page_data in pages_to_create:
            try:
                create_page_command = CreateCompanyPageCommand(
                    company_id=company_id.value,
                    page_type=page_data["page_type"],
                    title=page_data["title"],
                    html_content=page_data["html_content"],
                    meta_description=page_data["meta_description"],
                    meta_keywords=page_data["meta_keywords"],
                    language=page_data["language"],
                    is_default=page_data["is_default"]
                )
                self.command_bus.dispatch(create_page_command)
                log.debug(f"Created page: {page_data['page_type']} for company {company_id.value}")
            except Exception as e:
                # Log error but continue with other pages
                # The CreateCompanyPageCommandHandler will check if page already exists
                log.warning(f"Failed to create page '{page_data['page_type']}': {e}")
                continue

