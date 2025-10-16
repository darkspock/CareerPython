from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.resume.domain.entities.resume import Resume
from src.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.resume.domain.value_objects.general_data import GeneralData
from src.resume.domain.value_objects.resume_id import ResumeId
from src.resume.domain.value_objects.variable_section import VariableSection
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdateResumeContentCommand(Command):
    """Command to update resume content with hybrid structure (fixed + variable sections)"""
    resume_id: ResumeId
    # General data (fixed section)
    general_data: Optional[Dict[str, Any]] = None
    # Variable sections
    variable_sections: Optional[List[Dict[str, Any]]] = None
    # Legacy fields for compatibility
    experiencia_profesional: Optional[str] = None
    educacion: Optional[str] = None
    proyectos: Optional[str] = None
    habilidades: Optional[str] = None
    datos_personales: Optional[Dict[str, Any]] = None
    # Other fields
    custom_content: Optional[Dict[str, Any]] = None
    preserve_ai_content: bool = True


class UpdateResumeContentCommandHandler(CommandHandler[UpdateResumeContentCommand]):
    """Handler to update resume content with hybrid structure support"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def execute(self, command: UpdateResumeContentCommand) -> None:
        """Handle resume content update with support for both new and legacy formats"""

        # 1. Get resume
        resume = self.resume_repository.get_by_id(command.resume_id)
        if not resume:
            raise ValueError(f"Resume with id {command.resume_id.value} not found")

        # 2. Check if resume can be edited
        if not resume.can_be_edited():
            raise ValueError(f"Resume cannot be edited in status {resume.status.value}")

        # 3. Handle new structure (preferred)
        if command.general_data is not None or command.variable_sections is not None:
            self._update_with_new_structure(resume, command)
        # 4. Handle legacy structure for backward compatibility
        elif any([command.experiencia_profesional, command.educacion,
                  command.proyectos, command.habilidades, command.datos_personales]):
            self._update_with_legacy_structure(resume, command)

        # 5. Update custom content if provided
        if command.custom_content:
            resume.custom_content.update(command.custom_content)

        # 6. Save changes
        self.resume_repository.update(resume)

    def _update_with_new_structure(self, resume: Resume, command: UpdateResumeContentCommand) -> None:
        """Update resume using new hybrid structure"""

        # Update general data if provided
        if command.general_data:
            general_data = GeneralData.from_dict(command.general_data)
            resume.content.general_data = general_data

        # Update variable sections if provided
        if command.variable_sections:
            # Clear existing sections
            resume.content.variable_sections = []

            # Add new sections
            for section_data in command.variable_sections:
                section = VariableSection.from_dict(section_data)
                resume.content.add_section(section)

        # Update the resume content
        resume.update_content(
            content=resume.content,
            custom_content=command.custom_content,
            preserve_ai_content=command.preserve_ai_content
        )

    def _update_with_legacy_structure(self, resume: Resume, command: UpdateResumeContentCommand) -> None:
        """Update resume using legacy structure for backward compatibility"""

        # Update general data from legacy datos_personales
        if command.datos_personales:
            resume.content.general_data = GeneralData.from_dict(command.datos_personales)

        # Update variable sections from legacy fields
        if command.experiencia_profesional is not None:
            resume.update_variable_section('experience', command.experiencia_profesional)

        if command.educacion is not None:
            resume.update_variable_section('education', command.educacion)

        if command.proyectos is not None:
            resume.update_variable_section('projects', command.proyectos)

        if command.habilidades is not None:
            resume.update_variable_section('skills', command.habilidades)

        # Update custom content
        resume.update_content(
            content=resume.content,
            custom_content=command.custom_content,
            preserve_ai_content=command.preserve_ai_content
        )
