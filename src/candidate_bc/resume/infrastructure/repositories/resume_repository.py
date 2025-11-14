from typing import List, Optional, Dict, Any

from sqlalchemy import func, and_

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.resume.domain.entities.resume import Resume
from src.candidate_bc.resume.domain.enums.resume_type import ResumeType, ResumeStatus, AIEnhancementStatus
from src.candidate_bc.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.candidate_bc.resume.domain.value_objects.general_data import GeneralData
from src.candidate_bc.resume.domain.value_objects.resume_content import (
    ResumeContent,
    AIGeneratedContent,
    ResumeFormattingPreferences
)
from src.candidate_bc.resume.domain.value_objects.resume_id import ResumeId
from src.candidate_bc.resume.domain.value_objects.variable_section import VariableSection
from src.candidate_bc.resume.infrastructure.models.resume_model import ResumeModel


class SQLAlchemyResumeRepository(ResumeRepositoryInterface):
    """Implementación SQLAlchemy del repositorio de Resume"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def create(self, resume: Resume) -> Resume:
        """Crea un nuevo resume"""
        with self.database.get_session() as session:
            model = self._to_model(resume)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._to_domain(model)

    def get_by_id(self, resume_id: ResumeId) -> Optional[Resume]:
        """Obtiene un resume por ID"""
        with self.database.get_session() as session:
            model = session.query(ResumeModel).filter(
                ResumeModel.id == resume_id.value
            ).first()
            return self._to_domain(model) if model else None

    def get_by_candidate_id(
            self,
            candidate_id: CandidateId,
            resume_type: Optional[ResumeType] = None,
            limit: Optional[int] = None
    ) -> List[Resume]:
        """Obtiene resumes por candidate ID"""
        with self.database.get_session() as session:
            query = session.query(ResumeModel).filter(
                ResumeModel.candidate_id == candidate_id.value
            )

            if resume_type:
                query = query.filter(ResumeModel.resume_type == resume_type.value)

            query = query.order_by(ResumeModel.created_at.desc())

            if limit:
                query = query.limit(limit)

            models = query.all()
            return [self._to_domain(model) for model in models]

    def update(self, resume: Resume) -> Resume:
        """Actualiza un resume"""
        with self.database.get_session() as session:
            model = session.query(ResumeModel).filter(
                ResumeModel.id == resume.id.value
            ).first()

            if not model:
                raise ValueError(f"Resume with id {resume.id.value} not found")

            # Actualizar campos básicos
            model.name = resume.name
            model.resume_type = resume.resume_type.value

            # Pack content into JSON field with new hybrid structure
            model.content_data = {
                'general_data': resume.content.general_data.to_dict(),
                'variable_sections': [section.to_dict() for section in resume.content.variable_sections],
                # Store status and AI enhancement status in content_data
                'status': resume.status.value,
                'ai_enhancement_status': resume.ai_enhancement_status.value,
                # Include legacy fields for backward compatibility
                'experiencia_profesional': resume.content.experiencia_profesional,
                'educacion': resume.content.educacion,
                'proyectos': resume.content.proyectos,
                'habilidades': resume.content.habilidades,
                'datos_personales': resume.content.datos_personales
            }

            # Pack AI content into JSON field
            if resume.ai_generated_content:
                model.ai_content = {
                    'ai_summary': resume.ai_generated_content.ai_summary,
                    'ai_key_aspects': resume.ai_generated_content.ai_key_aspects,
                    'ai_skills_recommendations': resume.ai_generated_content.ai_skills_recommendations,
                    'ai_achievements': resume.ai_generated_content.ai_achievements,
                    'ai_intro_letter': resume.ai_generated_content.ai_intro_letter
                }

            # Pack formatting preferences into JSON field
            model.formatting_preferences = {
                'template': resume.formatting_preferences.template,
                'color_scheme': resume.formatting_preferences.color_scheme,
                'font_family': resume.formatting_preferences.font_family,
                'include_photo': resume.formatting_preferences.include_photo,
                'sections_order': resume.formatting_preferences.sections_order
            }

            # Store general_data in custom_content field
            model.custom_content = resume.general_data
            model.updated_at = resume.updated_at

            session.commit()
            session.refresh(model)
            return self._to_domain(model)

    def delete(self, resume_id: ResumeId) -> bool:
        """Elimina un resume"""
        with self.database.get_session() as session:
            model = session.query(ResumeModel).filter(
                ResumeModel.id == resume_id.value
            ).first()

            if model:
                session.delete(model)
                session.commit()
                return True
            return False

    def get_statistics_by_candidate(self, candidate_id: CandidateId) -> Dict[str, Any]:
        """Obtiene estadísticas de resumes por candidato"""
        with self.database.get_session() as session:
            # Contar total de resumes
            total_resumes = session.query(func.count(ResumeModel.id)).filter(
                ResumeModel.candidate_id == candidate_id.value
            ).scalar()

            # Contar por tipo
            resume_types_counts = {}
            for resume_type in ResumeType:
                count = session.query(func.count(ResumeModel.id)).filter(
                    and_(
                        ResumeModel.candidate_id == candidate_id.value,
                        ResumeModel.resume_type == resume_type.value
                    )
                ).scalar()
                resume_types_counts[resume_type.value] = count

            # Fechas de primer y último resume
            first_resume = session.query(
                func.min(ResumeModel.created_at)
            ).filter(
                ResumeModel.candidate_id == candidate_id.value
            ).scalar()

            last_resume = session.query(
                func.max(ResumeModel.created_at)
            ).filter(
                ResumeModel.candidate_id == candidate_id.value
            ).scalar()

            return {
                "total_resumes": total_resumes,
                "resume_types": resume_types_counts,
                "oldest_resume_date": first_resume.isoformat() if first_resume else None,
                "newest_resume_date": last_resume.isoformat() if last_resume else None,
                "user_id": candidate_id.value,
                "has_resumes": total_resumes > 0,
                "average_resumes_per_type": {
                    resume_type: count / len(ResumeType) if total_resumes > 0 else 0
                    for resume_type, count in resume_types_counts.items()
                }
            }

    def get_all_by_status(self, status: ResumeStatus) -> List[Resume]:
        """Obtiene resumes por status (simplified - returns all since DB doesn't have status)"""
        with self.database.get_session() as session:
            # Since the database doesn't have status column, return all resumes
            # In a real implementation, status would be stored in JSON fields
            models = session.query(ResumeModel).all()
            return [self._to_domain(model) for model in models]

    def bulk_delete(self, resume_ids: List[ResumeId]) -> int:
        """Elimina múltiples resumes y retorna el número eliminado"""
        with self.database.get_session() as session:
            ids_to_delete = [resume_id.value for resume_id in resume_ids]
            deleted_count = session.query(ResumeModel).filter(
                ResumeModel.id.in_(ids_to_delete)
            ).delete(synchronize_session=False)
            session.commit()
            return deleted_count

    def _to_domain(self, model: ResumeModel) -> Resume:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        # Extract content from JSON field
        content_json = model.content_data or {}

        # Build ResumeContent with new hybrid structure
        general_data = GeneralData.from_dict(content_json.get('general_data', {}))

        # Create variable sections from JSON
        variable_sections = []
        sections_data = content_json.get('variable_sections', [])
        for section_data in sections_data:
            variable_sections.append(VariableSection.from_dict(section_data))

        # If no variable sections exist, try to create from legacy fields for backward compatibility
        if not variable_sections and any([
            content_json.get('experiencia_profesional'),
            content_json.get('educacion'),
            content_json.get('proyectos'),
            content_json.get('habilidades')
        ]):
            # Create sections from legacy data
            if content_json.get('experiencia_profesional'):
                variable_sections.append(VariableSection(
                    key='experience',
                    title='Work Experience',
                    content=content_json.get('experiencia_profesional', ''),
                    order=1
                ))
            if content_json.get('educacion'):
                variable_sections.append(VariableSection(
                    key='education',
                    title='Education',
                    content=content_json.get('educacion', ''),
                    order=2
                ))
            if content_json.get('habilidades'):
                variable_sections.append(VariableSection(
                    key='skills',
                    title='Skills',
                    content=content_json.get('habilidades', ''),
                    order=3
                ))
            if content_json.get('proyectos'):
                variable_sections.append(VariableSection(
                    key='projects',
                    title='Projects',
                    content=content_json.get('proyectos', ''),
                    order=4
                ))

            # Update general data from legacy datos_personales if needed
            if not general_data.name and content_json.get('datos_personales'):
                general_data = GeneralData.from_dict(content_json.get('datos_personales', {}))

        content = ResumeContent(
            general_data=general_data,
            variable_sections=variable_sections
        )

        # Extract AI content from JSON field
        ai_content_json = model.ai_content or {}
        ai_generated_content = None
        if ai_content_json:
            ai_generated_content = AIGeneratedContent(
                ai_summary=ai_content_json.get('ai_summary'),
                ai_key_aspects=ai_content_json.get('ai_key_aspects', []),
                ai_skills_recommendations=ai_content_json.get('ai_skills_recommendations', []),
                ai_achievements=ai_content_json.get('ai_achievements', []),
                ai_intro_letter=ai_content_json.get('ai_intro_letter')
            )

        # Extract formatting preferences from JSON field
        formatting_json = model.formatting_preferences or {}
        formatting_preferences = ResumeFormattingPreferences(
            template=formatting_json.get('template', 'modern'),
            color_scheme=formatting_json.get('color_scheme', 'blue'),
            font_family=formatting_json.get('font_family', 'Arial'),
            include_photo=formatting_json.get('include_photo', False),
            sections_order=formatting_json.get('sections_order', [])
        )

        # Read status from JSON fields
        status = ResumeStatus(content_json.get('status', 'COMPLETED'))
        ai_enhancement_status = AIEnhancementStatus(content_json.get('ai_enhancement_status', 'NOT_REQUESTED'))

        return Resume(
            id=ResumeId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            name=model.name,
            resume_type=ResumeType(model.resume_type),
            status=status,
            content=content,
            ai_generated_content=ai_generated_content,
            formatting_preferences=formatting_preferences,
            ai_enhancement_status=ai_enhancement_status,
            general_data=model.custom_content or {},  # Use custom_content as general_data
            custom_content=model.custom_content or {},
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, resume: Resume) -> ResumeModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        model = ResumeModel()
        model.id = resume.id.value
        model.candidate_id = resume.candidate_id.value
        model.name = resume.name
        model.resume_type = resume.resume_type.value

        # Pack content into JSON field with new hybrid structure
        model.content_data = {
            'general_data': resume.content.general_data.to_dict(),
            'variable_sections': [section.to_dict() for section in resume.content.variable_sections],
            # Store status and AI enhancement status in content_data
            'status': resume.status.value,
            'ai_enhancement_status': resume.ai_enhancement_status.value,
            # Include legacy fields for backward compatibility
            'experiencia_profesional': resume.content.experiencia_profesional,
            'educacion': resume.content.educacion,
            'proyectos': resume.content.proyectos,
            'habilidades': resume.content.habilidades,
            'datos_personales': resume.content.datos_personales
        }

        # Pack AI content into JSON field
        if resume.ai_generated_content:
            model.ai_content = {
                'ai_summary': resume.ai_generated_content.ai_summary,
                'ai_key_aspects': resume.ai_generated_content.ai_key_aspects,
                'ai_skills_recommendations': resume.ai_generated_content.ai_skills_recommendations,
                'ai_achievements': resume.ai_generated_content.ai_achievements,
                'ai_intro_letter': resume.ai_generated_content.ai_intro_letter
            }

        # Pack formatting preferences into JSON field
        model.formatting_preferences = {
            'template': resume.formatting_preferences.template,
            'color_scheme': resume.formatting_preferences.color_scheme,
            'font_family': resume.formatting_preferences.font_family,
            'include_photo': resume.formatting_preferences.include_photo,
            'sections_order': resume.formatting_preferences.sections_order
        }

        # Store general_data in custom_content field
        model.custom_content = resume.general_data
        model.created_at = resume.created_at
        model.updated_at = resume.updated_at

        return model
