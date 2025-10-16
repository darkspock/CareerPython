from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

from src.resume.domain.entities.resume import Resume
from src.resume.domain.enums.resume_type import ResumeType, ResumeStatus, AIEnhancementStatus


@dataclass
class GeneralDataDto:
    """DTO for fixed resume data section"""
    cv_title: str
    name: str
    email: str
    phone: str


@dataclass
class VariableSectionDto:
    """DTO for variable resume sections with HTML content"""
    key: str
    title: str
    content: str  # HTML content
    order: int


@dataclass
class ResumeContentDto:
    """DTO for resume content with hybrid structure (new + legacy compatibility)"""
    # New hybrid structure
    general_data: GeneralDataDto
    variable_sections: List[VariableSectionDto]

    # Legacy compatibility fields (kept for backward compatibility)
    experiencia_profesional: str
    educacion: str
    proyectos: str
    habilidades: str
    datos_personales: Dict[str, Any]


@dataclass
class AIGeneratedContentDto:
    """DTO para contenido generado por IA"""
    ai_summary: Optional[str]
    ai_key_aspects: List[str]
    ai_skills_recommendations: List[str]
    ai_achievements: List[str]
    ai_intro_letter: Optional[str]


@dataclass
class ResumeFormattingPreferencesDto:
    """DTO para preferencias de formato"""
    template: str
    color_scheme: str
    font_family: str
    include_photo: bool
    sections_order: List[str]


@dataclass
class ResumeDto:
    """DTO para Resume"""
    id: str
    candidate_id: str
    name: str
    resume_type: ResumeType
    status: ResumeStatus
    ai_enhancement_status: AIEnhancementStatus
    content: ResumeContentDto
    ai_generated_content: Optional[AIGeneratedContentDto]
    formatting_preferences: ResumeFormattingPreferencesDto
    general_data: Dict[str, Any]
    custom_content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, resume: Resume) -> 'ResumeDto':
        """Crea un DTO desde una entidad Resume"""
        # Create GeneralDataDto from new structure
        general_data_dto = GeneralDataDto(
            cv_title=resume.content.general_data.cv_title,
            name=resume.content.general_data.name,
            email=resume.content.general_data.email,
            phone=resume.content.general_data.phone
        )

        # Create VariableSectionDto list from new structure
        variable_sections_dto = [
            VariableSectionDto(
                key=section.key,
                title=section.title,
                content=section.content,
                order=section.order
            )
            for section in resume.content.variable_sections
        ]

        # Create content DTO with both new and legacy structures
        content_dto = ResumeContentDto(
            # New hybrid structure
            general_data=general_data_dto,
            variable_sections=variable_sections_dto,
            # Legacy compatibility fields
            experiencia_profesional=resume.content.experiencia_profesional,
            educacion=resume.content.educacion,
            proyectos=resume.content.proyectos,
            habilidades=resume.content.habilidades,
            datos_personales=resume.content.datos_personales
        )

        ai_content_dto = None
        if resume.ai_generated_content:
            ai_content_dto = AIGeneratedContentDto(
                ai_summary=resume.ai_generated_content.ai_summary,
                ai_key_aspects=resume.ai_generated_content.ai_key_aspects,
                ai_skills_recommendations=resume.ai_generated_content.ai_skills_recommendations,
                ai_achievements=resume.ai_generated_content.ai_achievements,
                ai_intro_letter=resume.ai_generated_content.ai_intro_letter
            )

        formatting_dto = ResumeFormattingPreferencesDto(
            template=resume.formatting_preferences.template,
            color_scheme=resume.formatting_preferences.color_scheme,
            font_family=resume.formatting_preferences.font_family,
            include_photo=resume.formatting_preferences.include_photo,
            sections_order=resume.formatting_preferences.sections_order
        )

        return cls(
            id=resume.id.value,
            candidate_id=resume.candidate_id.value,
            name=resume.name,
            resume_type=resume.resume_type,
            status=resume.status,
            ai_enhancement_status=resume.ai_enhancement_status,
            content=content_dto,
            ai_generated_content=ai_content_dto,
            formatting_preferences=formatting_dto,
            general_data=resume.general_data,
            custom_content=resume.custom_content,
            created_at=resume.created_at,
            updated_at=resume.updated_at
        )
