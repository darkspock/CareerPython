"""
Create Company Page Command Handler - Handler para crear página de empresa
"""
from src.company.domain.value_objects.company_id import CompanyId
from src.company_page.application.commands.create_company_page_command import CreateCompanyPageCommand
from src.company_page.domain.entities.company_page import CompanyPage
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_page.domain.value_objects.page_metadata import PageMetadata
from src.shared.application.command_bus import CommandHandler


class CreateCompanyPageCommandHandler(CommandHandler[CreateCompanyPageCommand]):
    """Handler para crear una nueva página de empresa"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateCompanyPageCommand) -> None:
        """Ejecutar comando de creación de página"""

        # Convertir strings a value objects
        company_id = CompanyId(command.company_id)
        page_type = PageType(command.page_type)

        # Crear metadata
        metadata = PageMetadata.create(
            title=command.title,
            description=command.meta_description,
            keywords=command.meta_keywords,
            language=command.language
        )

        # Crear página
        page = CompanyPage.create(
            company_id=company_id,
            page_type=page_type,
            title=command.title,
            html_content=command.html_content,
            metadata=metadata,
            is_default=command.is_default
        )

        # Si es página por defecto, desmarcar otras páginas del mismo tipo
        if command.is_default:
            self._unset_other_default_pages(company_id, page_type)

        # Guardar página
        self.repository.save(page)

    def _unset_other_default_pages(self, company_id: CompanyId, page_type: PageType) -> None:
        """Desmarcar otras páginas del mismo tipo como default"""
        # Buscar página por defecto existente del mismo tipo
        existing_default = self.repository.get_default_by_type(company_id, page_type)

        if existing_default:
            # Desmarcar como default
            unset_page = existing_default.unset_as_default()
            self.repository.save(unset_page)
