"""
Company Page Repository Interface - Interface para repositorio de páginas de empresa
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.company_page.domain.entities.company_page import CompanyPage
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.enums.page_status import PageStatus
from src.company_page.domain.value_objects.page_id import PageId


class CompanyPageRepositoryInterface(ABC):
    """Interface para repositorio de páginas de empresa"""
    
    @abstractmethod
    def save(self, page: CompanyPage) -> None:
        """
        Guardar una página de empresa.
        
        Args:
            page: Página de empresa a guardar
            
        Raises:
            PageTypeAlreadyExistsException: Si ya existe una página del mismo tipo
        """
        pass
    
    @abstractmethod
    def get_by_id(self, page_id: PageId) -> Optional[CompanyPage]:
        """
        Obtener página por ID.
        
        Args:
            page_id: ID de la página
            
        Returns:
            Página encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_company_and_type(
        self, 
        company_id: CompanyId, 
        page_type: PageType
    ) -> Optional[CompanyPage]:
        """
        Obtener página por empresa y tipo.
        
        Args:
            company_id: ID de la empresa
            page_type: Tipo de página
            
        Returns:
            Página encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def list_by_company(self, company_id: CompanyId) -> List[CompanyPage]:
        """
        Listar todas las páginas de una empresa.
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de páginas de la empresa
        """
        pass
    
    @abstractmethod
    def list_by_company_and_status(
        self, 
        company_id: CompanyId, 
        status: PageStatus
    ) -> List[CompanyPage]:
        """
        Listar páginas de una empresa por estado.
        
        Args:
            company_id: ID de la empresa
            status: Estado de las páginas
            
        Returns:
            Lista de páginas con el estado especificado
        """
        pass
    
    @abstractmethod
    def list_by_company_and_type(
        self, 
        company_id: CompanyId, 
        page_type: PageType
    ) -> List[CompanyPage]:
        """
        Listar páginas de una empresa por tipo.
        
        Args:
            company_id: ID de la empresa
            page_type: Tipo de página
            
        Returns:
            Lista de páginas del tipo especificado
        """
        pass
    
    @abstractmethod
    def list_by_company_type_and_status(
        self, 
        company_id: CompanyId, 
        page_type: PageType,
        status: PageStatus
    ) -> List[CompanyPage]:
        """
        Listar páginas de una empresa por tipo y estado.
        
        Args:
            company_id: ID de la empresa
            page_type: Tipo de página
            status: Estado de las páginas
            
        Returns:
            Lista de páginas del tipo y estado especificados
        """
        pass
    
    @abstractmethod
    def get_default_by_type(
        self, 
        company_id: CompanyId, 
        page_type: PageType
    ) -> Optional[CompanyPage]:
        """
        Obtener página por defecto de un tipo específico.
        
        Args:
            company_id: ID de la empresa
            page_type: Tipo de página
            
        Returns:
            Página por defecto o None si no existe
        """
        pass
    
    @abstractmethod
    def list_public_pages(self, company_id: CompanyId) -> List[CompanyPage]:
        """
        Listar páginas públicas de una empresa.
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de páginas publicadas
        """
        pass
    
    @abstractmethod
    def delete(self, page_id: PageId) -> None:
        """
        Eliminar una página.
        
        Args:
            page_id: ID de la página a eliminar
            
        Raises:
            PageNotFoundException: Si la página no existe
        """
        pass
    
    @abstractmethod
    def exists_by_company_and_type(
        self, 
        company_id: CompanyId, 
        page_type: PageType
    ) -> bool:
        """
        Verificar si existe una página del tipo especificado para la empresa.
        
        Args:
            company_id: ID de la empresa
            page_type: Tipo de página
            
        Returns:
            True si existe, False si no
        """
        pass
    
    @abstractmethod
    def count_by_company(self, company_id: CompanyId) -> int:
        """
        Contar páginas de una empresa.
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Número de páginas de la empresa
        """
        pass
