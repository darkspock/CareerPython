from enum import Enum


class AssetTypeEnum(str, Enum):
    """Tipos de assets de usuario"""
    PDF_RESUME = "pdf_resume"
    LINKEDIN_PROFILE = "linkedin_profile"
    PORTFOLIO = "portfolio"
    COVER_LETTER = "cover_letter"


class ProcessingStatusEnum(str, Enum):
    """Estados de procesamiento de assets"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
