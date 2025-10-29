"""
Page Status Enum - Estados de las páginas de empresa
"""
from enum import Enum


class PageStatus(str, Enum):
    """Estados posibles de una página de empresa"""
    
    DRAFT = "draft"
    """Página en borrador, no visible públicamente"""
    
    PUBLISHED = "published"
    """Página publicada y visible públicamente"""
    
    ARCHIVED = "archived"
    """Página archivada, no visible públicamente"""
