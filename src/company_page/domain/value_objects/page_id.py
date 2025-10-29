"""
Page ID Value Object - Identificador único de una página
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class PageId:
    """Value Object para el ID de una página de empresa"""
    
    value: str
    
    def __post_init__(self):
        """Validar que el ID sea un UUID válido"""
        if not self.value:
            raise ValueError("PageId cannot be empty")
        
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError(f"PageId must be a valid UUID, got: {self.value}")
    
    @classmethod
    def generate(cls) -> "PageId":
        """Generar un nuevo PageId único"""
        return cls(value=str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self.value
