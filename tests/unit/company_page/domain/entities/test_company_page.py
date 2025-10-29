"""
Tests unitarios para la entidad CompanyPage
"""
import pytest
from datetime import datetime

from src.company.domain.value_objects.company_id import CompanyId
from src.company_page.domain.entities.company_page import CompanyPage
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.enums.page_status import PageStatus
from src.company_page.domain.value_objects.page_metadata import PageMetadata
from src.company_page.domain.exceptions.company_page_exceptions import (
    PageAlreadyDefaultException,
    InvalidPageStatusTransitionException
)


class TestCompanyPage:
    """Tests para la entidad CompanyPage"""
    
    def test_create_company_page_success(self):
        """Test crear página exitosamente"""
        # Arrange
        company_id = CompanyId("123e4567-e89b-12d3-a456-426614174000")
        page_type = PageType.PUBLIC_COMPANY_DESCRIPTION
        title = "Nuestra Empresa"
        html_content = "<h1>Somos una empresa innovadora</h1><p>Descripción de la empresa.</p>"
        metadata = PageMetadata.create(
            title="Nuestra Empresa",
            description="Descripción de nuestra empresa",
            keywords=["empresa", "innovación", "tecnología"]
        )
        
        # Act
        page = CompanyPage.create(
            company_id=company_id,
            page_type=page_type,
            title=title,
            html_content=html_content,
            metadata=metadata,
            is_default=False
        )
        
        # Assert
        assert page.company_id == company_id
        assert page.page_type == page_type
        assert page.title == title
        assert page.content.html_content == html_content
        assert page.metadata == metadata
        assert page.status == PageStatus.DRAFT
        assert page.is_default is False
        assert page.version == 1
        assert page.published_at is None
        assert page.can_be_edited() is True
        assert page.can_be_published() is True
        assert page.is_publicly_visible() is False
    
    def test_create_company_page_with_empty_title_fails(self):
        """Test que falla al crear página con título vacío"""
        # Arrange
        company_id = CompanyId("123e4567-e89b-12d3-a456-426614174000")
        page_type = PageType.PUBLIC_COMPANY_DESCRIPTION
        title = ""
        html_content = "<h1>Test</h1>"
        metadata = PageMetadata.create(title="Test", keywords=["test"])
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            CompanyPage.create(
                company_id=company_id,
                page_type=page_type,
                title=title,
                html_content=html_content,
                metadata=metadata
            )
    
    def test_update_content_success(self):
        """Test actualizar contenido exitosamente"""
        # Arrange
        page = self._create_test_page()
        new_title = "Nuevo Título"
        new_html_content = "<h1>Nuevo contenido</h1><p>Contenido actualizado.</p>"
        new_metadata = PageMetadata.create(
            title="Nuevo Título",
            description="Nueva descripción",
            keywords=["nuevo", "actualizado"]
        )
        
        # Act
        updated_page = page.update_content(
            title=new_title,
            html_content=new_html_content,
            metadata=new_metadata
        )
        
        # Assert
        assert updated_page.title == new_title
        assert updated_page.content.html_content == new_html_content
        assert updated_page.metadata == new_metadata
        assert updated_page.version == page.version + 1
        assert updated_page.updated_at > page.updated_at
    
    def test_publish_page_success(self):
        """Test publicar página exitosamente"""
        # Arrange
        page = self._create_test_page()
        
        # Act
        published_page = page.publish()
        
        # Assert
        assert published_page.status == PageStatus.PUBLISHED
        assert published_page.published_at is not None
        assert published_page.is_publicly_visible() is True
        assert published_page.can_be_published() is False
        assert published_page.can_be_archived() is True
    
    def test_publish_archived_page_fails(self):
        """Test que falla al publicar página archivada"""
        # Arrange
        page = self._create_test_page()
        archived_page = page.archive()
        
        # Act & Assert
        with pytest.raises(InvalidPageStatusTransitionException):
            archived_page.publish()
    
    def test_archive_page_success(self):
        """Test archivar página exitosamente"""
        # Arrange
        page = self._create_test_page()
        
        # Act
        archived_page = page.archive()
        
        # Assert
        assert archived_page.status == PageStatus.ARCHIVED
        assert archived_page.is_default is False  # Página archivada no puede ser default
        assert archived_page.can_be_archived() is False
        assert archived_page.is_publicly_visible() is False
    
    def test_set_as_default_success(self):
        """Test marcar como página por defecto exitosamente"""
        # Arrange
        page = self._create_test_page()
        published_page = page.publish()
        
        # Act
        default_page = published_page.set_as_default()
        
        # Assert
        assert default_page.is_default is True
        assert default_page.status == PageStatus.PUBLISHED
    
    def test_set_as_default_draft_page_fails(self):
        """Test que falla al marcar como default una página en draft"""
        # Arrange
        page = self._create_test_page()  # Está en DRAFT
        
        # Act & Assert
        with pytest.raises(InvalidPageStatusTransitionException):
            page.set_as_default()
    
    def test_set_as_default_already_default_fails(self):
        """Test que falla al marcar como default una página que ya es default"""
        # Arrange
        page = self._create_test_page()
        published_page = page.publish()
        default_page = published_page.set_as_default()
        
        # Act & Assert
        with pytest.raises(PageAlreadyDefaultException):
            default_page.set_as_default()
    
    def test_unset_as_default_success(self):
        """Test desmarcar como página por defecto exitosamente"""
        # Arrange
        page = self._create_test_page()
        published_page = page.publish()
        default_page = published_page.set_as_default()
        
        # Act
        unset_page = default_page.unset_as_default()
        
        # Assert
        assert unset_page.is_default is False
    
    def test_unset_as_default_not_default(self):
        """Test desmarcar como default una página que no es default"""
        # Arrange
        page = self._create_test_page()
        
        # Act
        result = page.unset_as_default()
        
        # Assert
        assert result.is_default is False
        assert result == page  # Debe retornar la misma instancia
    
    def _create_test_page(self) -> CompanyPage:
        """Helper para crear página de prueba"""
        company_id = CompanyId("123e4567-e89b-12d3-a456-426614174000")
        metadata = PageMetadata.create(
            title="Test Page",
            description="Test description",
            keywords=["test"]
        )
        
        return CompanyPage.create(
            company_id=company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Test Page",
            html_content="<h1>Test</h1>",
            metadata=metadata
        )
