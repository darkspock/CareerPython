"""
Company Page Request Schemas - Schemas de request para páginas de empresa
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from src.company_page.domain.enums.page_type import PageType


class CreateCompanyPageRequest(BaseModel):
    """Request para crear una página de empresa"""
    
    page_type: PageType = Field(..., description="Tipo de página")
    title: str = Field(..., min_length=1, max_length=500, description="Título de la página")
    html_content: str = Field(..., min_length=1, description="Contenido HTML de la página")
    meta_description: Optional[str] = Field(None, max_length=160, description="Meta descripción para SEO")
    meta_keywords: List[str] = Field(default_factory=list, max_items=20, description="Keywords para SEO")
    language: str = Field(default="es", min_length=2, max_length=2, description="Idioma de la página")
    is_default: bool = Field(default=False, description="Si es la página por defecto para este tipo")
    
    @validator('meta_keywords')
    def validate_keywords(cls, v):
        if len(v) > 20:
            raise ValueError('Maximum 20 keywords allowed')
        if any(not keyword.strip() for keyword in v):
            raise ValueError('Keywords cannot be empty')
        return v
    
    @validator('language')
    def validate_language(cls, v):
        if len(v) != 2:
            raise ValueError('Language must be a 2-character code')
        return v.lower()


class UpdateCompanyPageRequest(BaseModel):
    """Request para actualizar una página de empresa"""
    
    title: str = Field(..., min_length=1, max_length=500, description="Título de la página")
    html_content: str = Field(..., min_length=1, description="Contenido HTML de la página")
    meta_description: Optional[str] = Field(None, max_length=160, description="Meta descripción para SEO")
    meta_keywords: List[str] = Field(default_factory=list, max_items=20, description="Keywords para SEO")
    
    @validator('meta_keywords')
    def validate_keywords(cls, v):
        if len(v) > 20:
            raise ValueError('Maximum 20 keywords allowed')
        if any(not keyword.strip() for keyword in v):
            raise ValueError('Keywords cannot be empty')
        return v
