"""
Publish Company Page Command Handler - Handler para publicar página de empresa
"""
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import PageNotFoundException
from src.company_bc.company_page.application.commands.publish_company_page_command import PublishCompanyPageCommand
from src.framework.application.command_bus import CommandHandler


class PublishCompanyPageCommandHandler(CommandHandler[PublishCompanyPageCommand]):
    """Handler para publicar una página de empresa"""
    
    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository
    
    def execute(self, command: PublishCompanyPageCommand) -> None:
        """Ejecutar comando de publicación de página"""
        
        # Buscar página existente
        page_id = PageId(command.page_id)
        page = self.repository.get_by_id(page_id)
        
        if not page:
            raise PageNotFoundException(command.page_id)
        
        # Publicar página
        published_page = page.publish()
        
        # Guardar página publicada
        self.repository.save(published_page)
