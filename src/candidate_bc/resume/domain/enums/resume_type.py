from enum import Enum


class ResumeType(Enum):
    """Tipos de resume disponibles"""
    GENERAL = "GENERAL"
    POSITION = "POSITION"  # Específico para una posición
    ROLE = "ROLE"  # Específico para un rol/área


class ResumeStatus(Enum):
    """Estados del resume"""
    DRAFT = "DRAFT"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class AIEnhancementStatus(Enum):
    """Estados del proceso de mejora con IA"""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NOT_REQUESTED = "NOT_REQUESTED"
