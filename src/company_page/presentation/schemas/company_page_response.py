"""
Company Page Response Schemas - Schemas de response para páginas de empresa
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.enums.page_status import PageStatus


class CompanyPageResponse(BaseModel):
    """Response para una página de empresa"""
    
    id: str = Field(..., description="ID único de la página")
    company_id: str = Field(..., description="ID de la empresa")
    page_type: PageType = Field(..., description="Tipo de página")
    title: str = Field(..., description="Título de la página")
    html_content: str = Field(..., description="Contenido HTML de la página")
    plain_text: str = Field(..., description="Texto plano extraído del HTML")
    word_count: int = Field(..., description="Número de palabras en el contenido")
    meta_description: Optional[str] = Field(None, description="Meta descripción para SEO")
    meta_keywords: List[str] = Field(..., description="Keywords para SEO")
    language: str = Field(..., description="Idioma de la página")
    status: PageStatus = Field(..., description="Estado de la página")
    is_default: bool = Field(..., description="Si es la página por defecto para este tipo")
    version: int = Field(..., description="Versión de la página")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    published_at: Optional[datetime] = Field(None, description="Fecha de publicación")
    
    class Config:
        from_attributes = True


class CompanyPageListResponse(BaseModel):
    """Response para lista de páginas de empresa"""
    
    pages: List[CompanyPageResponse] = Field(..., description="Lista de páginas")
    total: int = Field(..., description="Total de páginas")
    
    class Config:
        from_attributes = True


class CompanyPageSummaryResponse(BaseModel):
    """Response resumido para una página de empresa (para listas)"""
    
    id: str = Field(..., description="ID único de la página")
    page_type: PageType = Field(..., description="Tipo de página")
    title: str = Field(..., description="Título de la página")
    status: PageStatus = Field(..., description="Estado de la página")
    is_default: bool = Field(..., description="Si es la página por defecto para este tipo")
    version: int = Field(..., description="Versión de la página")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")
    published_at: Optional[datetime] = Field(None, description="Fecha de publicación")
    
    class Config:
        from_attributes = True
