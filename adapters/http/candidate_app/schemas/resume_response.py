from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel

from src.candidate_bc.resume.domain.enums.resume_type import ResumeType, ResumeStatus, AIEnhancementStatus


class GeneralDataResponse(BaseModel):
    """Response schema for fixed resume data section"""
    cv_title: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""


class VariableSectionResponse(BaseModel):
    """Response schema for variable resume sections"""
    key: str
    title: str
    content: str = ""  # HTML content
    order: int = 0


class ResumeContentResponse(BaseModel):
    """Response schema for resume content with hybrid structure (new + legacy compatibility)"""
    # New hybrid structure
    general_data: GeneralDataResponse
    variable_sections: List[VariableSectionResponse] = []

    # Legacy compatibility fields (kept for backward compatibility)
    experiencia_profesional: str = ""
    educacion: str = ""
    proyectos: str = ""
    habilidades: str = ""
    datos_personales: Dict[str, Any] = {}


class AIGeneratedContentResponse(BaseModel):
    """Response schema para contenido generado por IA"""
    ai_summary: Optional[str] = None
    ai_key_aspects: List[str] = []
    ai_skills_recommendations: List[str] = []
    ai_achievements: List[str] = []
    ai_intro_letter: Optional[str] = None


class ResumeFormattingPreferencesResponse(BaseModel):
    """Response schema para preferencias de formato"""
    template: str = "modern"
    color_scheme: str = "blue"
    font_family: str = "Arial"
    include_photo: bool = False
    sections_order: List[str] = []


class ResumeResponse(BaseModel):
    """Response schema para Resume"""
    id: str
    candidate_id: str
    name: str
    resume_type: ResumeType
    status: ResumeStatus
    ai_enhancement_status: AIEnhancementStatus
    content: ResumeContentResponse
    ai_generated_content: Optional[AIGeneratedContentResponse] = None
    formatting_preferences: ResumeFormattingPreferencesResponse
    general_data: Dict[str, Any] = {}
    custom_content: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime


class ResumeListResponse(BaseModel):
    """Response schema para lista de resumes"""
    resumes: List[ResumeResponse]
    total_count: int
    message: Optional[str] = None


class ResumeStatisticsResponse(BaseModel):
    """Response schema para estadísticas de resumes"""
    total_resumes: int
    resume_types: Dict[str, int]
    oldest_resume_date: Optional[str] = None
    newest_resume_date: Optional[str] = None
    user_id: str
    has_resumes: bool
    average_resumes_per_type: Dict[str, float]
    message: Optional[str] = None
