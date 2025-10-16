from datetime import datetime
from typing import Optional, Dict, Any

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.resume.domain.enums.resume_type import ResumeType, ResumeStatus, AIEnhancementStatus
from src.resume.domain.value_objects.resume_content import (
    ResumeContent,
    AIGeneratedContent,
    ResumeFormattingPreferences
)
from src.resume.domain.value_objects.resume_id import ResumeId
from src.resume.domain.value_objects.variable_section import VariableSection


class Resume:
    """Entidad Resume"""

    def __init__(
            self,
            id: ResumeId,
            candidate_id: CandidateId,
            name: str,
            resume_type: ResumeType,
            status: ResumeStatus,
            content: ResumeContent,
            ai_generated_content: Optional[AIGeneratedContent] = None,
            formatting_preferences: Optional[ResumeFormattingPreferences] = None,
            ai_enhancement_status: AIEnhancementStatus = AIEnhancementStatus.NOT_REQUESTED,
            general_data: Optional[Dict[str, Any]] = None,
            custom_content: Optional[Dict[str, Any]] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.candidate_id = candidate_id
        self.name = name
        self.resume_type = resume_type
        self.status = status
        self.content = content
        self.ai_generated_content = ai_generated_content
        self.formatting_preferences = formatting_preferences or ResumeFormattingPreferences()
        self.ai_enhancement_status = ai_enhancement_status
        self.general_data = general_data or {}
        self.custom_content = custom_content or {}
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @classmethod
    def create_general_resume(
            cls,
            id: ResumeId,
            candidate_id: CandidateId,
            name: str,
            include_ai_enhancement: bool = False,
            general_data: Optional[Dict[str, Any]] = None
    ) -> 'Resume':
        """Factory method para crear un resume general con nueva estructura híbrida"""
        from src.resume.domain.value_objects.general_data import GeneralData

        resume_id = id

        # Create content with new hybrid structure
        content = ResumeContent()

        # Initialize general data from provided data
        if general_data:
            # Map legacy fields to new structure
            content.general_data = GeneralData(
                cv_title=general_data.get('cv_title', name),
                name=general_data.get('name', ''),
                email=general_data.get('email', ''),
                phone=general_data.get('phone', '')
            )
        else:
            content.general_data = GeneralData(cv_title=name)

        ai_enhancement_status = (
            AIEnhancementStatus.PENDING if include_ai_enhancement
            else AIEnhancementStatus.NOT_REQUESTED
        )

        return cls(
            id=resume_id,
            candidate_id=candidate_id,
            name=name,
            resume_type=ResumeType.GENERAL,
            status=ResumeStatus.DRAFT,
            content=content,
            ai_enhancement_status=ai_enhancement_status,
            general_data=general_data or {}
        )

    @classmethod
    def create_position_specific_resume(
            cls,
            candidate_id: CandidateId,
            name: str,
            position_data: Dict[str, Any],
            include_ai_enhancement: bool = False
    ) -> 'Resume':
        """Factory method para crear un resume específico para una posición con nueva estructura"""
        from src.resume.domain.value_objects.general_data import GeneralData

        resume_id = ResumeId.create()

        # Create content with new hybrid structure
        content = ResumeContent()

        # Initialize general data with position-specific information
        content.general_data = GeneralData(
            cv_title=position_data.get('cv_title', f"{name} - Position Specific"),
            name=position_data.get('candidate_name', ''),
            email=position_data.get('candidate_email', ''),
            phone=position_data.get('candidate_phone', '')
        )

        ai_enhancement_status = (
            AIEnhancementStatus.PENDING if include_ai_enhancement
            else AIEnhancementStatus.NOT_REQUESTED
        )

        return cls(
            id=resume_id,
            candidate_id=candidate_id,
            name=name,
            resume_type=ResumeType.POSITION,
            status=ResumeStatus.DRAFT,
            content=content,
            ai_enhancement_status=ai_enhancement_status,
            general_data=position_data
        )

    def start_generation(self) -> None:
        """Inicia el proceso de generación del resume"""
        if self.status != ResumeStatus.DRAFT:
            raise ValueError(f"Cannot start generation. Resume status is {self.status.value}")

        self.status = ResumeStatus.GENERATING
        if self.ai_enhancement_status == AIEnhancementStatus.PENDING:
            self.ai_enhancement_status = AIEnhancementStatus.PROCESSING
        self._touch_updated_at()

    def complete_generation(
            self,
            content: ResumeContent,
            ai_generated_content: Optional[AIGeneratedContent] = None
    ) -> None:
        """Completa el proceso de generación del resume"""
        if self.status != ResumeStatus.GENERATING:
            raise ValueError(f"Cannot complete generation. Resume status is {self.status.value}")

        self.status = ResumeStatus.COMPLETED
        self.content = content

        if ai_generated_content:
            self.ai_generated_content = ai_generated_content
            self.ai_enhancement_status = AIEnhancementStatus.COMPLETED
        elif self.ai_enhancement_status == AIEnhancementStatus.PROCESSING:
            self.ai_enhancement_status = AIEnhancementStatus.FAILED

        self._touch_updated_at()

    def fail_generation(self, error_reason: Optional[str] = None) -> None:
        """Marca el resume como fallido en la generación"""
        self.status = ResumeStatus.ERROR
        if self.ai_enhancement_status == AIEnhancementStatus.PROCESSING:
            self.ai_enhancement_status = AIEnhancementStatus.FAILED

        if error_reason:
            self.general_data['error_reason'] = error_reason

        self._touch_updated_at()

    def update_content(
            self,
            content: ResumeContent,
            custom_content: Optional[Dict[str, Any]] = None,
            preserve_ai_content: bool = True
    ) -> None:
        """Actualiza el contenido del resume"""
        self.content = content

        if custom_content:
            self.custom_content.update(custom_content)

        if not preserve_ai_content:
            self.ai_generated_content = None
            self.ai_enhancement_status = AIEnhancementStatus.NOT_REQUESTED

        self._touch_updated_at()

    def update_name(self, new_name: str) -> None:
        """Actualiza el nombre del resume"""
        if not new_name or not new_name.strip():
            raise ValueError("Resume name cannot be empty")

        self.name = new_name.strip()
        self._touch_updated_at()

    def update_formatting_preferences(self, preferences: ResumeFormattingPreferences) -> None:
        """Actualiza las preferencias de formato"""
        self.formatting_preferences = preferences
        self._touch_updated_at()

    def can_be_edited(self) -> bool:
        """Verifica si el resume puede ser editado"""
        return self.status != ResumeStatus.GENERATING

    def can_be_deleted(self) -> bool:
        """Verifica si el resume puede ser eliminado"""
        return True  # Los resumes siempre pueden eliminarse

    def duplicate(self, new_name: str, candidate_id: Optional[CandidateId] = None) -> 'Resume':
        """Crea una copia del resume"""
        new_id = ResumeId.create()
        new_candidate_id = candidate_id or self.candidate_id

        return Resume(
            id=new_id,
            candidate_id=new_candidate_id,
            name=new_name,
            resume_type=self.resume_type,
            status=ResumeStatus.DRAFT,
            content=self.content,
            ai_generated_content=self.ai_generated_content,
            formatting_preferences=self.formatting_preferences,
            ai_enhancement_status=self.ai_enhancement_status,
            general_data=self.general_data.copy(),
            custom_content=self.custom_content.copy()
        )

    def _touch_updated_at(self) -> None:
        """Actualiza el timestamp de updated_at"""
        self.updated_at = datetime.now()

    # New methods for managing variable sections
    def add_variable_section(self, key: str, title: str, content: str = "", order: int = 0) -> None:
        """Add a new variable section"""
        from src.resume.domain.value_objects.variable_section import VariableSection

        section = VariableSection(key=key, title=title, content=content, order=order)
        self.content.add_section(section)
        self._touch_updated_at()

    def update_variable_section(self, key: str, content: str, title: Optional[str] = None) -> None:
        """Update content of a variable section"""
        self.content.update_section(key, content, title)
        self._touch_updated_at()

    def remove_variable_section(self, key: str) -> bool:
        """Remove a variable section"""
        result = self.content.remove_section(key)
        if result:
            self._touch_updated_at()
        return result

    def get_variable_section(self, key: str) -> Optional[VariableSection]:
        """Get a variable section by key"""
        return self.content.get_section_by_key(key)

    def update_general_data(self, cv_title: Optional[str] = None, name: Optional[str] = None,
                            email: Optional[str] = None, phone: Optional[str] = None) -> None:
        """Update general data section"""
        if cv_title is not None:
            self.content.general_data.cv_title = cv_title
        if name is not None:
            self.content.general_data.name = name
        if email is not None:
            self.content.general_data.email = email
        if phone is not None:
            self.content.general_data.phone = phone

        self._touch_updated_at()

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario para serialización"""
        return {
            'id': self.id.value,
            'candidate_id': self.candidate_id.value,
            'name': self.name,
            'resume_type': self.resume_type.value,
            'status': self.status.value,
            'ai_enhancement_status': self.ai_enhancement_status.value,
            'content': self.content.to_dict(),  # Use new structure
            'ai_generated_content': {
                'ai_summary': self.ai_generated_content.ai_summary if self.ai_generated_content else None,
                'ai_key_aspects': self.ai_generated_content.ai_key_aspects if self.ai_generated_content else [],
                'ai_skills_recommendations': self.ai_generated_content.ai_skills_recommendations if self.ai_generated_content else [],
                'ai_achievements': self.ai_generated_content.ai_achievements if self.ai_generated_content else [],
                'ai_intro_letter': self.ai_generated_content.ai_intro_letter if self.ai_generated_content else None
            } if self.ai_generated_content else None,
            'formatting_preferences': {
                'template': self.formatting_preferences.template,
                'color_scheme': self.formatting_preferences.color_scheme,
                'font_family': self.formatting_preferences.font_family,
                'include_photo': self.formatting_preferences.include_photo,
                'sections_order': self.formatting_preferences.sections_order
            },
            'general_data': self.general_data,
            'custom_content': self.custom_content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
