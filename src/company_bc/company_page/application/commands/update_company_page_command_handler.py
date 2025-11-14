"""
Update Company Page Command Handler - Handler para actualizar página de empresa
"""
from src.company_bc.company_page.application.commands.update_company_page_command import UpdateCompanyPageCommand
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import PageNotFoundException
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import \
    CompanyPageRepositoryInterface
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.framework.application.command_bus import CommandHandler


class UpdateCompanyPageCommandHandler(CommandHandler[UpdateCompanyPageCommand]):
    """Handler para actualizar una página de empresa existente"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateCompanyPageCommand) -> None:
        """Ejecutar comando de actualización de página"""

        # Buscar página existente
        page_id = PageId(command.page_id)
        page = self.repository.get_by_id(page_id)

        if not page:
            raise PageNotFoundException(command.page_id)

        # Crear metadata actualizada
        updated_metadata = page.metadata.update(
            title=command.title,
            description=command.meta_description,
            keywords=command.meta_keywords
        )

        # Actualizar contenido
        updated_page = page.update_content(
            title=command.title,
            html_content=command.html_content,
            metadata=updated_metadata
        )

        # Guardar página actualizada
        self.repository.save(updated_page)
