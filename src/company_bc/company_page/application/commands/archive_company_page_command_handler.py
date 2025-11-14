"""
Archive Company Page Command Handler - Handler para archivar página de empresa
"""
from src.company_bc.company_page.application.commands.archive_company_page_command import ArchiveCompanyPageCommand
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import PageNotFoundException
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import \
    CompanyPageRepositoryInterface
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.framework.application.command_bus import CommandHandler


class ArchiveCompanyPageCommandHandler(CommandHandler[ArchiveCompanyPageCommand]):
    """Handler para archivar una página de empresa"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def execute(self, command: ArchiveCompanyPageCommand) -> None:
        """Ejecutar comando de archivado de página"""

        # Buscar página existente
        page_id = PageId(command.page_id)
        page = self.repository.get_by_id(page_id)

        if not page:
            raise PageNotFoundException(command.page_id)

        # Archivar página
        archived_page = page.archive()

        # Guardar página archivada
        self.repository.save(archived_page)
