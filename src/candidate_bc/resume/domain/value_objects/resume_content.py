from dataclasses import dataclass, field
from typing import List, Optional

from .general_data import GeneralData
from .variable_section import VariableSection


@dataclass
class WorkExperience:
    """Value Object para experiencia laboral en el resume"""
    job_title: str
    company: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False


@dataclass
class ResumeContent:
    """Value Object for resume content with hybrid structure (fixed + variable sections)"""
    # Fixed section with general data
    general_data: GeneralData = field(default_factory=GeneralData)

    # Variable sections with HTML content
    variable_sections: List[VariableSection] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize with default sections if empty"""
        if not self.variable_sections:
            self.variable_sections = VariableSection.create_default_sections()

    def get_section_by_key(self, key: str) -> Optional[VariableSection]:
        """Get a variable section by its key"""
        for section in self.variable_sections:
            if section.key == key:
                return section
        return None

    def add_section(self, section: VariableSection) -> None:
        """Add a new variable section"""
        # Check if section with same key already exists
        existing = self.get_section_by_key(section.key)
        if existing:
            raise ValueError(f"Section with key '{section.key}' already exists")

        self.variable_sections.append(section)
        # Sort by order
        self.variable_sections.sort(key=lambda s: s.order)

    def update_section(self, key: str, content: str, title: Optional[str] = None) -> None:
        """Update content of an existing section"""
        section = self.get_section_by_key(key)
        if not section:
            raise ValueError(f"Section with key '{key}' not found")

        section.content = content
        if title:
            section.title = title

    def remove_section(self, key: str) -> bool:
        """Remove a variable section by key"""
        for i, section in enumerate(self.variable_sections):
            if section.key == key:
                del self.variable_sections[i]
                return True
        return False

    def get_sections_ordered(self) -> List[VariableSection]:
        """Get all sections ordered by their order field"""
        return sorted(self.variable_sections, key=lambda s: s.order)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'general_data': self.general_data.to_dict(),
            'variable_sections': [section.to_dict() for section in self.variable_sections]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ResumeContent':
        """Create from dictionary"""
        general_data = GeneralData.from_dict(data.get('general_data', {}))
        variable_sections = [
            VariableSection.from_dict(section_data)
            for section_data in data.get('variable_sections', [])
        ]

        return cls(
            general_data=general_data,
            variable_sections=variable_sections
        )

    # Legacy compatibility methods (for gradual migration)
    @property
    def datos_personales(self) -> dict:
        """Legacy compatibility - return general data as dict"""
        return self.general_data.to_dict()

    @property
    def experiencia_profesional(self) -> str:
        """Legacy compatibility - return experience section content"""
        section = self.get_section_by_key('experience')
        return section.content if section else ""

    @property
    def educacion(self) -> str:
        """Legacy compatibility - return education section content"""
        section = self.get_section_by_key('education')
        return section.content if section else ""

    @property
    def proyectos(self) -> str:
        """Legacy compatibility - return projects section content"""
        section = self.get_section_by_key('projects')
        return section.content if section else ""

    @property
    def habilidades(self) -> str:
        """Legacy compatibility - return skills section content"""
        section = self.get_section_by_key('skills')
        return section.content if section else ""


@dataclass
class AIGeneratedContent:
    """Value Object para contenido generado por IA"""
    ai_summary: Optional[str] = None
    ai_key_aspects: List[str] = field(default_factory=list)
    ai_skills_recommendations: List[str] = field(default_factory=list)
    ai_achievements: List[str] = field(default_factory=list)
    ai_intro_letter: Optional[str] = None


@dataclass
class ResumeFormattingPreferences:
    """Value Object para preferencias de formato"""
    template: str = "modern"
    color_scheme: str = "blue"
    font_family: str = "Arial"
    include_photo: bool = False
    sections_order: List[str] = field(default_factory=lambda: [
        "personal_info",
        "summary",
        "experience",
        "education",
        "skills",
        "projects"
    ])
