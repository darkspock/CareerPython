"""
Tests unitarios para PageContent Value Object
"""
import pytest

from src.company_bc.company_page.domain.value_objects.page_content import PageContent


class TestPageContent:
    """Tests para PageContent Value Object"""
    
    def test_create_page_content_success(self):
        """Test crear PageContent exitosamente"""
        # Arrange
        html_content = "<h1>Título</h1><p>Este es un párrafo con <strong>texto en negrita</strong>.</p>"
        
        # Act
        content = PageContent.create(html_content)
        
        # Assert
        assert content.html_content == html_content
        assert content.plain_text == "Título Este es un párrafo con texto en negrita."
        assert content.word_count == 9
        assert content.word_count == len(content.plain_text.split())
    
    def test_create_page_content_with_empty_html_fails(self):
        """Test que falla al crear PageContent con HTML vacío"""
        # Act & Assert
        with pytest.raises(ValueError, match="HTML content cannot be empty"):
            PageContent.create("")
        
        with pytest.raises(ValueError, match="HTML content cannot be empty"):
            PageContent.create("   ")
    
    def test_create_page_content_with_scripts_and_styles(self):
        """Test crear PageContent removiendo scripts y styles"""
        # Arrange
        html_content = """
        <html>
        <head>
            <style>body { color: red; }</style>
            <script>console.log('test');</script>
        </head>
        <body>
            <h1>Título Principal</h1>
            <p>Contenido del párrafo.</p>
        </body>
        </html>
        """
        
        # Act
        content = PageContent.create(html_content)
        
        # Assert
        assert "Título Principal" in content.plain_text
        assert "Contenido del párrafo" in content.plain_text
        assert "body { color: red; }" not in content.plain_text
        assert "console.log('test');" not in content.plain_text
        assert content.word_count == 5
    
    def test_create_page_content_with_complex_html(self):
        """Test crear PageContent con HTML complejo"""
        # Arrange
        html_content = """
        <div class="container">
            <h1>Nuestra Empresa</h1>
            <div class="content">
                <p>Somos una <em>empresa innovadora</em> que se dedica a la <strong>tecnología</strong>.</p>
                <ul>
                    <li>Innovación</li>
                    <li>Calidad</li>
                    <li>Servicio</li>
                </ul>
            </div>
        </div>
        """
        
        # Act
        content = PageContent.create(html_content)
        
        # Assert
        assert "Nuestra Empresa" in content.plain_text
        assert "empresa innovadora" in content.plain_text
        assert "tecnología" in content.plain_text
        assert "Innovación" in content.plain_text
        assert "Calidad" in content.plain_text
        assert "Servicio" in content.plain_text
        assert content.word_count > 0
    
    def test_update_content_success(self):
        """Test actualizar contenido exitosamente"""
        # Arrange
        original_html = "<h1>Original</h1>"
        content = PageContent.create(original_html)
        new_html = "<h1>Actualizado</h1><p>Nuevo contenido.</p>"
        
        # Act
        updated_content = content.update_content(new_html)
        
        # Assert
        assert updated_content.html_content == new_html
        assert updated_content.plain_text == "Actualizado Nuevo contenido."
        assert updated_content.word_count == 3
    
    def test_page_content_immutability(self):
        """Test que PageContent es inmutable"""
        # Arrange
        html_content = "<h1>Test</h1>"
        content = PageContent.create(html_content)
        
        # Act & Assert
        # No se puede modificar directamente
        with pytest.raises(AttributeError):
            content.html_content = "Modified"
        
        with pytest.raises(AttributeError):
            content.plain_text = "Modified"
        
        with pytest.raises(AttributeError):
            content.word_count = 999
