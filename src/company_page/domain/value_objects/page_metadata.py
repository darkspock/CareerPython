"""
Page Metadata Value Object - Metadatos SEO de una página
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class PageMetadata:
    """Value Object para metadatos SEO de una página"""
    
    title: str
    description: Optional[str]  # Meta description
    keywords: List[str]
    language: str = "es"
    
    def __post_init__(self):
        """Validar metadatos"""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        
        if len(self.title) > 60:
            raise ValueError("Title should be 60 characters or less for SEO")
        
        if self.description and len(self.description) > 160:
            raise ValueError("Meta description should be 160 characters or less for SEO")
        
        if not self.keywords:
            raise ValueError("Keywords list cannot be empty")
        
        if len(self.keywords) > 20:
            raise ValueError("Too many keywords, maximum 20 allowed")
        
        # Validar que no haya keywords duplicados
        unique_keywords = list(set(self.keywords))
        if len(unique_keywords) != len(self.keywords):
            raise ValueError("Keywords cannot contain duplicates")
        
        # Validar que no haya keywords vacíos
        if any(not keyword.strip() for keyword in self.keywords):
            raise ValueError("Keywords cannot be empty")
        
        if not self.language.strip():
            raise ValueError("Language cannot be empty")
        
        if len(self.language) != 2:
            raise ValueError("Language must be a 2-character code (e.g., 'es', 'en')")
    
    @classmethod
    def create(
        cls,
        title: str,
        description: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        language: str = "es"
    ) -> "PageMetadata":
        """Crear PageMetadata con validaciones"""
        if keywords is None:
            keywords = []
        
        return cls(
            title=title.strip(),
            description=description.strip() if description else None,
            keywords=[keyword.strip() for keyword in keywords if keyword.strip()],
            language=language.strip().lower()
        )
    
    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        language: Optional[str] = None
    ) -> "PageMetadata":
        """Crear nueva instancia con metadatos actualizados"""
        return self.create(
            title=title if title is not None else self.title,
            description=description if description is not None else self.description,
            keywords=keywords if keywords is not None else self.keywords,
            language=language if language is not None else self.language
        )
