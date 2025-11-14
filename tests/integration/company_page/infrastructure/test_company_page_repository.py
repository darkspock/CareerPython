"""
Tests de integración para CompanyPageRepository
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.domain.entities.company_page import CompanyPage
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.enums.page_status import PageStatus
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.domain.value_objects.page_metadata import PageMetadata
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import (
    PageTypeAlreadyExistsException,
    PageNotFoundException
)
from src.company_page.infrastructure.repositories.company_page_repository import CompanyPageRepository
from src.company_page.infrastructure.models.company_page_model import CompanyPageModel
from src.framework.infrastructure.models.base import Base


class TestCompanyPageRepository:
    """Tests para CompanyPageRepository"""
    
    @pytest.fixture
    def db_session(self):
        """Crear sesión de base de datos para tests"""
        # Crear base de datos en memoria para tests
        engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    @pytest.fixture
    def repository(self, db_session):
        """Crear repositorio para tests"""
        return CompanyPageRepository(db_session)
    
    @pytest.fixture
    def test_company_id(self):
        """ID de empresa para tests"""
        return CompanyId("123e4567-e89b-12d3-a456-426614174000")
    
    @pytest.fixture
    def test_page(self, test_company_id):
        """Crear página de prueba"""
        metadata = PageMetadata.create(
            title="Test Page",
            description="Test description",
            keywords=["test", "page"]
        )
        
        return CompanyPage.create(
            company_id=test_company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Test Page",
            html_content="<h1>Test Content</h1>",
            metadata=metadata
        )
    
    def test_save_new_page_success(self, repository, test_page):
        """Test guardar nueva página exitosamente"""
        # Act
        repository.save(test_page)
        
        # Assert
        saved_model = repository.session.query(CompanyPageModel).filter(
            CompanyPageModel.id == test_page.id.value
        ).first()
        
        assert saved_model is not None
        assert saved_model.company_id == test_page.company_id.value
        assert saved_model.page_type == test_page.page_type.value
        assert saved_model.title == test_page.title
        assert saved_model.status == test_page.status.value
    
    def test_save_duplicate_page_type_fails(self, repository, test_page):
        """Test que falla al guardar página con tipo duplicado"""
        # Arrange
        repository.save(test_page)
        
        # Crear segunda página del mismo tipo
        metadata2 = PageMetadata.create(
            title="Test Page 2",
            description="Test description 2",
            keywords=["test2"]
        )
        
        page2 = CompanyPage.create(
            company_id=test_page.company_id,
            page_type=test_page.page_type,  # Mismo tipo
            title="Test Page 2",
            html_content="<h1>Test Content 2</h1>",
            metadata=metadata2
        )
        
        # Act & Assert
        with pytest.raises(PageTypeAlreadyExistsException):
            repository.save(page2)
    
    def test_get_by_id_success(self, repository, test_page):
        """Test obtener página por ID exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Act
        found_page = repository.get_by_id(test_page.id)
        
        # Assert
        assert found_page is not None
        assert found_page.id == test_page.id
        assert found_page.title == test_page.title
    
    def test_get_by_id_not_found(self, repository):
        """Test obtener página por ID que no existe"""
        # Arrange
        page_id = PageId.generate()
        
        # Act
        found_page = repository.get_by_id(page_id)
        
        # Assert
        assert found_page is None
    
    def test_get_by_company_and_type_success(self, repository, test_page):
        """Test obtener página por empresa y tipo exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Act
        found_page = repository.get_by_company_and_type(
            test_page.company_id,
            test_page.page_type
        )
        
        # Assert
        assert found_page is not None
        assert found_page.company_id == test_page.company_id
        assert found_page.page_type == test_page.page_type
    
    def test_list_by_company_success(self, repository, test_company_id):
        """Test listar páginas de empresa exitosamente"""
        # Arrange
        metadata1 = PageMetadata.create(title="Page 1", keywords=["test1"])
        page1 = CompanyPage.create(
            company_id=test_company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Page 1",
            html_content="<h1>Content 1</h1>",
            metadata=metadata1
        )
        
        metadata2 = PageMetadata.create(title="Page 2", keywords=["test2"])
        page2 = CompanyPage.create(
            company_id=test_company_id,
            page_type=PageType.JOB_POSITION_DESCRIPTION,
            title="Page 2",
            html_content="<h1>Content 2</h1>",
            metadata=metadata2
        )
        
        repository.save(page1)
        repository.save(page2)
        
        # Act
        pages = repository.list_by_company(test_company_id)
        
        # Assert
        assert len(pages) == 2
        assert any(p.title == "Page 1" for p in pages)
        assert any(p.title == "Page 2" for p in pages)
    
    def test_list_by_company_and_status_success(self, repository, test_page):
        """Test listar páginas por estado exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Act
        draft_pages = repository.list_by_company_and_status(
            test_page.company_id,
            PageStatus.DRAFT
        )
        
        published_pages = repository.list_by_company_and_status(
            test_page.company_id,
            PageStatus.PUBLISHED
        )
        
        # Assert
        assert len(draft_pages) == 1
        assert len(published_pages) == 0
        assert draft_pages[0].status == PageStatus.DRAFT
    
    def test_list_public_pages_success(self, repository, test_page):
        """Test listar páginas públicas exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Publicar la página
        published_page = test_page.publish()
        repository.save(published_page)
        
        # Act
        public_pages = repository.list_public_pages(test_page.company_id)
        
        # Assert
        assert len(public_pages) == 1
        assert public_pages[0].status == PageStatus.PUBLISHED
    
    def test_delete_page_success(self, repository, test_page):
        """Test eliminar página exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Act
        repository.delete(test_page.id)
        
        # Assert
        found_page = repository.get_by_id(test_page.id)
        assert found_page is None
    
    def test_delete_page_not_found_fails(self, repository):
        """Test que falla al eliminar página que no existe"""
        # Arrange
        page_id = PageId.generate()
        
        # Act & Assert
        with pytest.raises(PageNotFoundException):
            repository.delete(page_id)
    
    def test_exists_by_company_and_type_success(self, repository, test_page):
        """Test verificar existencia de página por tipo exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Act
        exists = repository.exists_by_company_and_type(
            test_page.company_id,
            test_page.page_type
        )
        
        # Assert
        assert exists is True
    
    def test_exists_by_company_and_type_not_found(self, repository, test_company_id):
        """Test verificar existencia de página que no existe"""
        # Act
        exists = repository.exists_by_company_and_type(
            test_company_id,
            PageType.DATA_PROTECTION
        )
        
        # Assert
        assert exists is False
    
    def test_count_by_company_success(self, repository, test_company_id):
        """Test contar páginas de empresa exitosamente"""
        # Arrange
        metadata1 = PageMetadata.create(title="Page 1", keywords=["test1"])
        page1 = CompanyPage.create(
            company_id=test_company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Page 1",
            html_content="<h1>Content 1</h1>",
            metadata=metadata1
        )
        
        metadata2 = PageMetadata.create(title="Page 2", keywords=["test2"])
        page2 = CompanyPage.create(
            company_id=test_company_id,
            page_type=PageType.JOB_POSITION_DESCRIPTION,
            title="Page 2",
            html_content="<h1>Content 2</h1>",
            metadata=metadata2
        )
        
        repository.save(page1)
        repository.save(page2)
        
        # Act
        count = repository.count_by_company(test_company_id)
        
        # Assert
        assert count == 2
    
    def test_update_existing_page_success(self, repository, test_page):
        """Test actualizar página existente exitosamente"""
        # Arrange
        repository.save(test_page)
        
        # Actualizar contenido
        new_metadata = PageMetadata.create(
            title="Updated Page",
            description="Updated description",
            keywords=["updated", "page"]
        )
        
        updated_page = test_page.update_content(
            title="Updated Page",
            html_content="<h1>Updated Content</h1>",
            metadata=new_metadata
        )
        
        # Act
        repository.save(updated_page)
        
        # Assert
        found_page = repository.get_by_id(test_page.id)
        assert found_page.title == "Updated Page"
        assert found_page.version == test_page.version + 1
        assert found_page.metadata.description == "Updated description"
