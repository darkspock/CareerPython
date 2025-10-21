from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VisibilitySettings:
    """Value object for candidate visibility settings controlled by the company"""
    education: bool
    experience: bool
    projects: bool
    skills: bool
    certifications: bool
    languages: bool
    contact_info: bool

    @classmethod
    def default(cls) -> "VisibilitySettings":
        """Create default visibility settings (all visible)"""
        return cls(
            education=True,
            experience=True,
            projects=True,
            skills=True,
            certifications=True,
            languages=True,
            contact_info=True,
        )

    @classmethod
    def minimal(cls) -> "VisibilitySettings":
        """Create minimal visibility settings (only basic info)"""
        return cls(
            education=False,
            experience=False,
            projects=False,
            skills=False,
            certifications=False,
            languages=False,
            contact_info=False,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, bool]) -> "VisibilitySettings":
        """Create from dictionary"""
        return cls(
            education=data.get("education", True),
            experience=data.get("experience", True),
            projects=data.get("projects", True),
            skills=data.get("skills", True),
            certifications=data.get("certifications", True),
            languages=data.get("languages", True),
            contact_info=data.get("contact_info", True),
        )

    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary"""
        return {
            "education": self.education,
            "experience": self.experience,
            "projects": self.projects,
            "skills": self.skills,
            "certifications": self.certifications,
            "languages": self.languages,
            "contact_info": self.contact_info,
        }
