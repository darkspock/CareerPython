"""
Page Content Value Object - Contenido de una página
"""
from dataclasses import dataclass
import re
from typing import Optional


@dataclass(frozen=True)
class PageContent:
    """Value Object para el contenido de una página"""
    
    html_content: str
    plain_text: str  # Para SEO y búsquedas
    word_count: int
    
    def __post_init__(self)->None:
        """Validar el contenido de la página"""
        if not self.html_content.strip():
            raise ValueError("HTML content cannot be empty")
        
        if not self.plain_text.strip():
            raise ValueError("Plain text content cannot be empty")
        
        if self.word_count < 0:
            raise ValueError("Word count cannot be negative")
        
        # Validar que el word_count coincida aproximadamente con el contenido
        actual_word_count = len(self.plain_text.split())
        if abs(actual_word_count - self.word_count) > 5:  # Tolerancia de 5 palabras
            raise ValueError(f"Word count mismatch: expected {self.word_count}, actual {actual_word_count}")
    
    @classmethod
    def create(cls, html_content: str) -> "PageContent":
        """Crear PageContent a partir de HTML"""
        if not html_content.strip():
            raise ValueError("HTML content cannot be empty")
        
        # Extraer texto plano del HTML (método básico)
        plain_text = cls._extract_plain_text(html_content)
        word_count = len(plain_text.split())
        
        return cls(
            html_content=html_content,
            plain_text=plain_text,
            word_count=word_count
        )
    
    @staticmethod
    def _extract_plain_text(html_content: str) -> str:
        """Extraer texto plano del HTML (implementación básica)"""
        # Remover tags HTML básicos
        import re
        # Remover scripts y styles
        text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remover todos los tags HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Limpiar espacios en blanco
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def update_content(self, html_content: str) -> "PageContent":
        """Crear nueva instancia con contenido actualizado"""
        return self.create(html_content)
