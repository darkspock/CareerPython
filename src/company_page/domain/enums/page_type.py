"""
Page Type Enum - Tipos de páginas que puede crear una empresa
"""
from enum import Enum


class PageType(str, Enum):
    """Tipos de páginas disponibles para empresas"""
    
    PUBLIC_COMPANY_DESCRIPTION = "public_company_description"
    """Descripción pública de la empresa que se muestra en la parte pública"""
    
    JOB_POSITION_DESCRIPTION = "job_position_description"
    """Descripción de la empresa que se incluye en cada oferta de trabajo"""
    
    DATA_PROTECTION = "data_protection"
    """Página de protección de datos y privacidad"""
    
    TERMS_OF_USE = "terms_of_use"
    """Página de condiciones de uso"""
    
    THANK_YOU_APPLICATION = "thank_you_application"
    """Página de agradecimiento que se muestra después de aplicar"""
