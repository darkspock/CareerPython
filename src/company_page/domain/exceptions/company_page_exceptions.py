"""
Company Page Domain Exceptions - Excepciones específicas del dominio de páginas
"""
from src.shared.domain.exceptions import DomainException


class CompanyPageException(DomainException):
    """Excepción base para el dominio de páginas de empresa"""
    pass


class PageTypeAlreadyExistsException(CompanyPageException):
    """Excepción cuando ya existe una página del mismo tipo para la empresa"""

    def __init__(self, company_id: str, page_type: str):
        self.company_id = company_id
        self.page_type = page_type
        super().__init__(f"Page of type '{page_type}' already exists for company '{company_id}'")


class InvalidPageContentException(CompanyPageException):
    """Excepción cuando el contenido de la página no es válido"""

    def __init__(self, message: str):
        super().__init__(f"Invalid page content: {message}")


class PageNotPublishedException(CompanyPageException):
    """Excepción cuando se intenta acceder a una página no publicada"""

    def __init__(self, page_id: str):
        self.page_id = page_id
        super().__init__(f"Page '{page_id}' is not published")


class PageNotFoundException(CompanyPageException):
    """Excepción cuando no se encuentra una página"""

    def __init__(self, page_id: str):
        self.page_id = page_id
        super().__init__(f"Page '{page_id}' not found")


class InvalidPageStatusTransitionException(CompanyPageException):
    """Excepción cuando se intenta una transición de estado inválida"""

    def __init__(self, current_status: str, target_status: str):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(f"Cannot transition from '{current_status}' to '{target_status}'")


class PageAlreadyDefaultException(CompanyPageException):
    """Excepción cuando se intenta marcar como default una página que ya lo es"""

    def __init__(self, page_id: str):
        self.page_id = page_id
        super().__init__(f"Page '{page_id}' is already the default page for its type")
