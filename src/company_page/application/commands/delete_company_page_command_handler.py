"""
Delete Company Page Command Handler - Handler para eliminar página de empresa
"""
from src.company_page.domain.value_objects.page_id import PageId
from src.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_page.application.commands.delete_company_page_command import DeleteCompanyPageCommand
from src.shared.application.command_bus import CommandHandler


class DeleteCompanyPageCommandHandler(CommandHandler[DeleteCompanyPageCommand]):
    """Handler para eliminar una página de empresa"""
    
    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository
    
    def execute(self, command: DeleteCompanyPageCommand) -> None:
        """Ejecutar comando de eliminación de página"""
        
        # Eliminar página
        page_id = PageId(command.page_id)
        self.repository.delete(page_id)
