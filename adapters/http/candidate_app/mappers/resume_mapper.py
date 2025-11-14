from typing import List, Dict, Any, Optional

from adapters.http.candidate_app.schemas.resume_dto import ResumeDto
from adapters.http.candidate_app.schemas.resume_response import (
    ResumeResponse,
    ResumeContentResponse,
    GeneralDataResponse,
    VariableSectionResponse,
    AIGeneratedContentResponse,
    ResumeFormattingPreferencesResponse,
    ResumeListResponse,
    ResumeStatisticsResponse
)


class ResumeMapper:
    """Mapper para convertir DTOs a Response schemas"""

    @staticmethod
    def dto_to_response(dto: ResumeDto) -> ResumeResponse:
        """Convierte ResumeDto a ResumeResponse"""
        # Create GeneralDataResponse from new structure
        general_data_response = GeneralDataResponse(
            cv_title=dto.content.general_data.cv_title,
            name=dto.content.general_data.name,
            email=dto.content.general_data.email,
            phone=dto.content.general_data.phone
        )

        # Create VariableSectionResponse list from new structure
        variable_sections_response = [
            VariableSectionResponse(
                key=section.key,
                title=section.title,
                content=section.content,
                order=section.order
            )
            for section in dto.content.variable_sections
        ]

        # Create content response with both new and legacy structures
        content_response = ResumeContentResponse(
            # New hybrid structure
            general_data=general_data_response,
            variable_sections=variable_sections_response,
            # Legacy compatibility fields
            experiencia_profesional=dto.content.experiencia_profesional,
            educacion=dto.content.educacion,
            proyectos=dto.content.proyectos,
            habilidades=dto.content.habilidades,
            datos_personales=dto.content.datos_personales
        )

        ai_content_response = None
        if dto.ai_generated_content:
            ai_content_response = AIGeneratedContentResponse(
                ai_summary=dto.ai_generated_content.ai_summary,
                ai_key_aspects=dto.ai_generated_content.ai_key_aspects,
                ai_skills_recommendations=dto.ai_generated_content.ai_skills_recommendations,
                ai_achievements=dto.ai_generated_content.ai_achievements,
                ai_intro_letter=dto.ai_generated_content.ai_intro_letter
            )

        formatting_response = ResumeFormattingPreferencesResponse(
            template=dto.formatting_preferences.template,
            color_scheme=dto.formatting_preferences.color_scheme,
            font_family=dto.formatting_preferences.font_family,
            include_photo=dto.formatting_preferences.include_photo,
            sections_order=dto.formatting_preferences.sections_order
        )

        return ResumeResponse(
            id=dto.id,
            candidate_id=dto.candidate_id,
            name=dto.name,
            resume_type=dto.resume_type,
            status=dto.status,
            ai_enhancement_status=dto.ai_enhancement_status,
            content=content_response,
            ai_generated_content=ai_content_response,
            formatting_preferences=formatting_response,
            general_data=dto.general_data,
            custom_content=dto.custom_content,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def dtos_to_list_response(dtos: List[ResumeDto], message: Optional[str] = None) -> ResumeListResponse:
        """Convierte lista de DTOs a ResumeListResponse"""
        resume_responses = [ResumeMapper.dto_to_response(dto) for dto in dtos]

        return ResumeListResponse(
            resumes=resume_responses,
            total_count=len(resume_responses),
            message=message
        )

    @staticmethod
    def statistics_to_response(statistics: Dict[str, Any]) -> ResumeStatisticsResponse:
        """Convierte diccionario de estadísticas a ResumeStatisticsResponse"""
        return ResumeStatisticsResponse(
            total_resumes=statistics.get('total_resumes', 0),
            resume_types=statistics.get('resume_types', {}),
            oldest_resume_date=statistics.get('oldest_resume_date'),
            newest_resume_date=statistics.get('newest_resume_date'),
            user_id=statistics.get('user_id', ''),
            has_resumes=statistics.get('has_resumes', False),
            average_resumes_per_type=statistics.get('average_resumes_per_type', {})
        )
