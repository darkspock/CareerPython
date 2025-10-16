from typing import Optional, Dict, Any, List

from pydantic import BaseModel, field_validator


class CreateGeneralResumeRequest(BaseModel):
    """Request schema to create a general resume"""
    name: str
    include_ai_enhancement: bool = False
    general_data: Optional[Dict[str, Any]] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Resume name cannot be empty')
        if len(v.strip()) > 255:
            raise ValueError('Resume name cannot exceed 255 characters')
        return v.strip()


class GeneralDataRequest(BaseModel):
    """Request schema for fixed resume data section"""
    cv_title: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class VariableSectionRequest(BaseModel):
    """Request schema for variable resume sections"""
    key: str
    title: str
    content: str = ""  # HTML content
    order: int = 0

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if len(v) > 10000:
            raise ValueError('Section content cannot exceed 10000 characters')
        return v


class UpdateResumeContentRequest(BaseModel):
    """Request schema for updating resume content with hybrid structure (new + legacy compatibility)"""
    # New hybrid structure fields
    general_data: Optional[GeneralDataRequest] = None
    variable_sections: Optional[List[VariableSectionRequest]] = None

    # Legacy compatibility fields (kept for backward compatibility)
    experiencia_profesional: Optional[str] = None
    educacion: Optional[str] = None
    proyectos: Optional[str] = None
    habilidades: Optional[str] = None
    datos_personales: Optional[Dict[str, Any]] = None

    # Common fields
    custom_content: Optional[Dict[str, Any]] = None
    preserve_ai_content: bool = True

    @field_validator('experiencia_profesional')
    @classmethod
    def validate_experiencia_profesional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 10000:
            raise ValueError('Experiencia profesional cannot exceed 10000 characters')
        return v

    @field_validator('educacion')
    @classmethod
    def validate_educacion(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 5000:
            raise ValueError('Educación cannot exceed 5000 characters')
        return v

    @field_validator('proyectos')
    @classmethod
    def validate_proyectos(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 5000:
            raise ValueError('Proyectos cannot exceed 5000 characters')
        return v

    @field_validator('habilidades')
    @classmethod
    def validate_habilidades(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 2000:
            raise ValueError('Habilidades cannot exceed 2000 characters')
        return v


class UpdateResumeNameRequest(BaseModel):
    """Request schema to update resume name"""
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Resume name cannot be empty')
        if len(v.strip()) > 255:
            raise ValueError('Resume name cannot exceed 255 characters')
        return v.strip()


class BulkDeleteResumesRequest(BaseModel):
    """Request schema for bulk resume deletion"""
    resume_ids: List[str]

    @field_validator('resume_ids')
    @classmethod
    def validate_resume_ids(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError('At least one resume ID must be provided')
        if len(v) > 50:
            raise ValueError('Cannot delete more than 50 resumes at once')
        return v


# Variable Section Management Requests
class AddVariableSectionRequest(BaseModel):
    """Request schema for adding a new variable section"""
    section_key: str
    section_title: str
    section_content: str = ""
    section_order: Optional[int] = None

    @field_validator('section_key')
    @classmethod
    def validate_section_key(cls, v: str) -> str:
        import re
        if not re.match(r'^[a-z][a-z0-9_]*$', v):
            raise ValueError('Section key must be lowercase with underscores only')
        return v

    @field_validator('section_content')
    @classmethod
    def validate_section_content(cls, v: str) -> str:
        if len(v) > 10000:
            raise ValueError('Section content cannot exceed 10000 characters')
        return v


class UpdateVariableSectionRequest(BaseModel):
    """Request schema for updating a variable section"""
    section_key: str
    section_content: Optional[str] = None
    section_title: Optional[str] = None
    section_order: Optional[int] = None

    @field_validator('section_content')
    @classmethod
    def validate_section_content(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 10000:
            raise ValueError('Section content cannot exceed 10000 characters')
        return v


class RemoveVariableSectionRequest(BaseModel):
    """Request schema for removing a variable section"""
    section_key: str


class ReorderVariableSectionsRequest(BaseModel):
    """Request schema for reordering variable sections"""
    sections_order: List[Dict[str, Any]]  # [{"key": "experience", "order": 1}, ...]

    @field_validator('sections_order')
    @classmethod
    def validate_sections_order(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not v:
            raise ValueError('At least one section order must be provided')

        for item in v:
            if 'key' not in item or 'order' not in item:
                raise ValueError('Each section order item must have "key" and "order" fields')

        return v
