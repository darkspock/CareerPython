"""
Set Default Page Command Handler - Handler para marcar página como default
"""
from src.company_bc.company.domain import CompanyId
from src.company_bc.company_page.application.commands.set_default_page_command import SetDefaultPageCommand
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import PageNotFoundException
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.framework.application.command_bus import CommandHandler


class SetDefaultPageCommandHandler(CommandHandler[SetDefaultPageCommand]):
    """Handler para marcar una página como página por defecto"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def execute(self, command: SetDefaultPageCommand) -> None:
        """Ejecutar comando de marcar como página por defecto"""

        # Buscar página existente
        page_id = PageId(command.page_id)
        page = self.repository.get_by_id(page_id)

        if not page:
            raise PageNotFoundException(command.page_id)

        # Desmarcar otras páginas del mismo tipo como default
        self._unset_other_default_pages(page.company_id, page.page_type)

        # Marcar como default
        default_page = page.set_as_default()

        # Guardar página marcada como default
        self.repository.save(default_page)

    def _unset_other_default_pages(self, company_id: CompanyId, page_type: PageType) -> None:
        """Desmarcar otras páginas del mismo tipo como default"""
        # Buscar página por defecto existente del mismo tipo
        existing_default = self.repository.get_default_by_type(company_id, page_type)

        if existing_default:
            # Desmarcar como default
            unset_page = existing_default.unset_as_default()
            self.repository.save(unset_page)
