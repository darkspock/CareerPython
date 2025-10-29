"""
Tests de integración para Company Page Router
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from src.company_page.presentation.routers.company_page_router import router
from src.company_page.presentation.routers.public_company_page_router import router as public_router
from src.company_page.presentation.schemas.company_page_response import CompanyPageResponse
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.enums.page_status import PageStatus


class TestCompanyPageRouter:
    """Tests para el router de páginas de empresa"""
    
    @pytest.fixture
    def mock_controller(self):
        """Mock del controller"""
        controller = Mock()
        return controller
    
    @pytest.fixture
    def client(self, mock_controller):
        """Cliente de prueba con mock del controller"""
        from fastapi import FastAPI
        from unittest.mock import patch
        
        app = FastAPI()
        app.include_router(router)
        app.include_router(public_router)
        
        with patch('src.company_page.presentation.routers.company_page_router.get_controller', return_value=mock_controller):
            with patch('src.company_page.presentation.routers.public_company_page_router.get_controller', return_value=mock_controller):
                yield TestClient(app)
    
    def test_create_company_page_success(self, client, mock_controller):
        """Test crear página exitosamente"""
        # Arrange
        company_id = "123e4567-e89b-12d3-a456-426614174000"
        request_data = {
            "page_type": "public_company_description",
            "title": "Nuestra Empresa",
            "html_content": "<h1>Somos una empresa innovadora</h1>",
            "meta_description": "Descripción de nuestra empresa",
            "meta_keywords": ["empresa", "innovación"],
            "language": "es",
            "is_default": False
        }
        
        expected_response = CompanyPageResponse(
            id="page-123",
            company_id=company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Nuestra Empresa",
            html_content="<h1>Somos una empresa innovadora</h1>",
            plain_text="Somos una empresa innovadora",
            word_count=4,
            meta_description="Descripción de nuestra empresa",
            meta_keywords=["empresa", "innovación"],
            language="es",
            status=PageStatus.DRAFT,
            is_default=False,
            version=1,
            created_at="2025-01-25T10:00:00Z",
            updated_at="2025-01-25T10:00:00Z",
            published_at=None
        )
        
        mock_controller.create_page.return_value = expected_response
        
        # Act
        response = client.post(f"/api/company/{company_id}/pages", json=request_data)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["title"] == "Nuestra Empresa"
        assert response.json()["page_type"] == "public_company_description"
        mock_controller.create_page.assert_called_once()
    
    def test_create_company_page_validation_error(self, client, mock_controller):
        """Test crear página con datos inválidos"""
        # Arrange
        company_id = "123e4567-e89b-12d3-a456-426614174000"
        request_data = {
            "page_type": "public_company_description",
            "title": "",  # Título vacío
            "html_content": "<h1>Test</h1>",
            "meta_keywords": ["test"]
        }
        
        # Act
        response = client.post(f"/api/company/{company_id}/pages", json=request_data)
        
        # Assert
        assert response.status_code == 422  # Validation error
        assert "title" in response.json()["detail"][0]["loc"]
    
    def test_list_company_pages_success(self, client, mock_controller):
        """Test listar páginas exitosamente"""
        # Arrange
        company_id = "123e4567-e89b-12d3-a456-426614174000"
        
        expected_response = {
            "pages": [
                {
                    "id": "page-1",
                    "company_id": company_id,
                    "page_type": "public_company_description",
                    "title": "Página 1",
                    "html_content": "<h1>Contenido 1</h1>",
                    "plain_text": "Contenido 1",
                    "word_count": 2,
                    "meta_description": None,
                    "meta_keywords": [],
                    "language": "es",
                    "status": "draft",
                    "is_default": False,
                    "version": 1,
                    "created_at": "2025-01-25T10:00:00Z",
                    "updated_at": "2025-01-25T10:00:00Z",
                    "published_at": None
                }
            ],
            "total": 1
        }
        
        mock_controller.list_pages.return_value = expected_response
        
        # Act
        response = client.get(f"/api/company/{company_id}/pages")
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()["pages"]) == 1
        assert response.json()["total"] == 1
        mock_controller.list_pages.assert_called_once_with(company_id, None)
    
    def test_get_company_page_success(self, client, mock_controller):
        """Test obtener página por ID exitosamente"""
        # Arrange
        page_id = "page-123"
        
        expected_response = CompanyPageResponse(
            id=page_id,
            company_id="123e4567-e89b-12d3-a456-426614174000",
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Test Page",
            html_content="<h1>Test</h1>",
            plain_text="Test",
            word_count=1,
            meta_description=None,
            meta_keywords=[],
            language="es",
            status=PageStatus.DRAFT,
            is_default=False,
            version=1,
            created_at="2025-01-25T10:00:00Z",
            updated_at="2025-01-25T10:00:00Z",
            published_at=None
        )
        
        mock_controller.get_page.return_value = expected_response
        
        # Act
        response = client.get(f"/api/company/pages/{page_id}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["id"] == page_id
        mock_controller.get_page.assert_called_once_with(page_id)
    
    def test_get_company_page_not_found(self, client, mock_controller):
        """Test obtener página que no existe"""
        # Arrange
        page_id = "non-existent-page"
        mock_controller.get_page.side_effect = ValueError(f"Page with ID {page_id} not found")
        
        # Act
        response = client.get(f"/api/company/pages/{page_id}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_update_company_page_success(self, client, mock_controller):
        """Test actualizar página exitosamente"""
        # Arrange
        page_id = "page-123"
        request_data = {
            "title": "Título Actualizado",
            "html_content": "<h1>Contenido Actualizado</h1>",
            "meta_description": "Descripción actualizada",
            "meta_keywords": ["actualizado", "test"]
        }
        
        expected_response = CompanyPageResponse(
            id=page_id,
            company_id="123e4567-e89b-12d3-a456-426614174000",
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Título Actualizado",
            html_content="<h1>Contenido Actualizado</h1>",
            plain_text="Contenido Actualizado",
            word_count=2,
            meta_description="Descripción actualizada",
            meta_keywords=["actualizado", "test"],
            language="es",
            status=PageStatus.DRAFT,
            is_default=False,
            version=2,
            created_at="2025-01-25T10:00:00Z",
            updated_at="2025-01-25T10:00:00Z",
            published_at=None
        )
        
        mock_controller.update_page.return_value = expected_response
        
        # Act
        response = client.put(f"/api/company/pages/{page_id}", json=request_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["title"] == "Título Actualizado"
        assert response.json()["version"] == 2
        mock_controller.update_page.assert_called_once()
    
    def test_publish_company_page_success(self, client, mock_controller):
        """Test publicar página exitosamente"""
        # Arrange
        page_id = "page-123"
        
        expected_response = CompanyPageResponse(
            id=page_id,
            company_id="123e4567-e89b-12d3-a456-426614174000",
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Test Page",
            html_content="<h1>Test</h1>",
            plain_text="Test",
            word_count=1,
            meta_description=None,
            meta_keywords=[],
            language="es",
            status=PageStatus.PUBLISHED,
            is_default=False,
            version=1,
            created_at="2025-01-25T10:00:00Z",
            updated_at="2025-01-25T10:00:00Z",
            published_at="2025-01-25T10:30:00Z"
        )
        
        mock_controller.publish_page.return_value = expected_response
        
        # Act
        response = client.post(f"/api/company/pages/{page_id}/publish")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "published"
        assert response.json()["published_at"] is not None
        mock_controller.publish_page.assert_called_once_with(page_id)
    
    def test_delete_company_page_success(self, client, mock_controller):
        """Test eliminar página exitosamente"""
        # Arrange
        page_id = "page-123"
        mock_controller.delete_page.return_value = None
        
        # Act
        response = client.delete(f"/api/company/pages/{page_id}")
        
        # Assert
        assert response.status_code == 204
        mock_controller.delete_page.assert_called_once_with(page_id)
    
    def test_get_public_company_page_success(self, client, mock_controller):
        """Test obtener página pública exitosamente"""
        # Arrange
        company_id = "123e4567-e89b-12d3-a456-426614174000"
        page_type = "public_company_description"
        
        expected_response = CompanyPageResponse(
            id="page-123",
            company_id=company_id,
            page_type=PageType.PUBLIC_COMPANY_DESCRIPTION,
            title="Página Pública",
            html_content="<h1>Contenido Público</h1>",
            plain_text="Contenido Público",
            word_count=2,
            meta_description="Descripción pública",
            meta_keywords=["público", "empresa"],
            language="es",
            status=PageStatus.PUBLISHED,
            is_default=True,
            version=1,
            created_at="2025-01-25T10:00:00Z",
            updated_at="2025-01-25T10:00:00Z",
            published_at="2025-01-25T10:30:00Z"
        )
        
        mock_controller.get_public_page.return_value = expected_response
        
        # Act
        response = client.get(f"/api/public/company/{company_id}/pages/{page_type}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "published"
        assert response.json()["is_default"] is True
        mock_controller.get_public_page.assert_called_once_with(company_id, page_type)
    
    def test_get_public_company_page_not_found(self, client, mock_controller):
        """Test obtener página pública que no existe"""
        # Arrange
        company_id = "123e4567-e89b-12d3-a456-426614174000"
        page_type = "non_existent_type"
        
        mock_controller.get_public_page.return_value = None
        
        # Act
        response = client.get(f"/api/public/company/{company_id}/pages/{page_type}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
