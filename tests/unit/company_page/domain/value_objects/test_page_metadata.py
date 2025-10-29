"""
Tests unitarios para PageMetadata Value Object
"""
import pytest

from src.company_page.domain.value_objects.page_metadata import PageMetadata


class TestPageMetadata:
    """Tests para PageMetadata Value Object"""
    
    def test_create_page_metadata_success(self):
        """Test crear PageMetadata exitosamente"""
        # Arrange
        title = "Nuestra Empresa"
        description = "Descripción de nuestra empresa innovadora"
        keywords = ["empresa", "innovación", "tecnología"]
        language = "es"
        
        # Act
        metadata = PageMetadata.create(
            title=title,
            description=description,
            keywords=keywords,
            language=language
        )
        
        # Assert
        assert metadata.title == title
        assert metadata.description == description
        assert metadata.keywords == keywords
        assert metadata.language == language
    
    def test_create_page_metadata_with_defaults(self):
        """Test crear PageMetadata con valores por defecto"""
        # Arrange
        title = "Test Page"
        keywords = ["test"]
        
        # Act
        metadata = PageMetadata.create(title=title, keywords=keywords)
        
        # Assert
        assert metadata.title == title
        assert metadata.description is None
        assert metadata.keywords == keywords
        assert metadata.language == "es"
    
    def test_create_page_metadata_with_empty_title_fails(self):
        """Test que falla al crear PageMetadata con título vacío"""
        # Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            PageMetadata.create(title="", keywords=["test"])
        
        with pytest.raises(ValueError, match="Title cannot be empty"):
            PageMetadata.create(title="   ", keywords=["test"])
    
    def test_create_page_metadata_with_long_title_fails(self):
        """Test que falla al crear PageMetadata con título muy largo"""
        # Arrange
        long_title = "A" * 61  # Más de 60 caracteres
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title should be 60 characters or less for SEO"):
            PageMetadata.create(title=long_title, keywords=["test"])
    
    def test_create_page_metadata_with_long_description_fails(self):
        """Test que falla al crear PageMetadata con descripción muy larga"""
        # Arrange
        long_description = "A" * 161  # Más de 160 caracteres
        
        # Act & Assert
        with pytest.raises(ValueError, match="Meta description should be 160 characters or less for SEO"):
            PageMetadata.create(
                title="Test",
                description=long_description,
                keywords=["test"]
            )
    
    def test_create_page_metadata_with_empty_keywords_fails(self):
        """Test que falla al crear PageMetadata con keywords vacías"""
        # Act & Assert
        with pytest.raises(ValueError, match="Keywords list cannot be empty"):
            PageMetadata.create(title="Test", keywords=[])
    
    def test_create_page_metadata_with_too_many_keywords_fails(self):
        """Test que falla al crear PageMetadata con demasiadas keywords"""
        # Arrange
        many_keywords = [f"keyword{i}" for i in range(21)]  # 21 keywords
        
        # Act & Assert
        with pytest.raises(ValueError, match="Too many keywords, maximum 20 allowed"):
            PageMetadata.create(title="Test", keywords=many_keywords)
    
    def test_create_page_metadata_with_duplicate_keywords_fails(self):
        """Test que falla al crear PageMetadata con keywords duplicadas"""
        # Arrange
        duplicate_keywords = ["test", "empresa", "test", "innovación"]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Keywords cannot contain duplicates"):
            PageMetadata.create(title="Test", keywords=duplicate_keywords)
    
    def test_create_page_metadata_with_empty_keywords_fails(self):
        """Test que falla al crear PageMetadata con keywords vacías"""
        # Arrange
        empty_keywords = ["test", "", "empresa", "   "]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Keywords cannot be empty"):
            PageMetadata.create(title="Test", keywords=empty_keywords)
    
    def test_create_page_metadata_with_invalid_language_fails(self):
        """Test que falla al crear PageMetadata con idioma inválido"""
        # Act & Assert
        with pytest.raises(ValueError, match="Language must be a 2-character code"):
            PageMetadata.create(title="Test", keywords=["test"], language="spanish")
        
        with pytest.raises(ValueError, match="Language must be a 2-character code"):
            PageMetadata.create(title="Test", keywords=["test"], language="e")
        
        with pytest.raises(ValueError, match="Language must be a 2-character code"):
            PageMetadata.create(title="Test", keywords=["test"], language="")
    
    def test_create_page_metadata_removes_empty_keywords(self):
        """Test que PageMetadata remueve keywords vacías automáticamente"""
        # Arrange
        keywords_with_empty = ["test", "", "empresa", "   ", "innovación"]
        
        # Act
        metadata = PageMetadata.create(title="Test", keywords=keywords_with_empty)
        
        # Assert
        assert metadata.keywords == ["test", "empresa", "innovación"]
    
    def test_update_metadata_success(self):
        """Test actualizar metadatos exitosamente"""
        # Arrange
        metadata = PageMetadata.create(
            title="Original",
            description="Original description",
            keywords=["original"],
            language="es"
        )
        
        # Act
        updated_metadata = metadata.update(
            title="Updated",
            description="Updated description",
            keywords=["updated", "new"],
            language="en"
        )
        
        # Assert
        assert updated_metadata.title == "Updated"
        assert updated_metadata.description == "Updated description"
        assert updated_metadata.keywords == ["updated", "new"]
        assert updated_metadata.language == "en"
    
    def test_update_metadata_partial(self):
        """Test actualizar metadatos parcialmente"""
        # Arrange
        metadata = PageMetadata.create(
            title="Original",
            description="Original description",
            keywords=["original"],
            language="es"
        )
        
        # Act
        updated_metadata = metadata.update(title="Updated")
        
        # Assert
        assert updated_metadata.title == "Updated"
        assert updated_metadata.description == "Original description"  # Sin cambios
        assert updated_metadata.keywords == ["original"]  # Sin cambios
        assert updated_metadata.language == "es"  # Sin cambios
    
    def test_page_metadata_immutability(self):
        """Test que PageMetadata es inmutable"""
        # Arrange
        metadata = PageMetadata.create(title="Test", keywords=["test"])
        
        # Act & Assert
        # No se puede modificar directamente
        with pytest.raises(AttributeError):
            metadata.title = "Modified"
        
        with pytest.raises(AttributeError):
            metadata.description = "Modified"
        
        with pytest.raises(AttributeError):
            metadata.keywords = ["modified"]
        
        with pytest.raises(AttributeError):
            metadata.language = "en"
