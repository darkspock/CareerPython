"""
Profile Markdown Service

Renders a candidate's profile as markdown for recruiter view.
This creates a snapshot of the candidate's information at application time.
"""
from datetime import date
from typing import Any, Dict, List, Optional

from src.candidate_bc.candidate.domain.entities.candidate import Candidate
from src.candidate_bc.candidate.domain.entities.candidate_education import CandidateEducation
from src.candidate_bc.candidate.domain.entities.candidate_experience import CandidateExperience
from src.candidate_bc.candidate.domain.entities.candidate_project import CandidateProject


class ProfileMarkdownService:
    """Service to render candidate profile as markdown"""

    @staticmethod
    def render(
            candidate: Candidate,
            experiences: List[CandidateExperience],
            education: List[CandidateEducation],
            projects: List[CandidateProject],
            language: str = "es"
    ) -> str:
        """
        Render candidate profile as markdown.

        Args:
            candidate: The candidate entity
            experiences: List of work experiences
            education: List of education entries
            projects: List of projects
            language: Language for section headers (es/en)

        Returns:
            Markdown string with full profile
        """
        headers = ProfileMarkdownService._get_headers(language)
        lines: List[str] = []

        # Header with name
        lines.append(f"# {candidate.name}")
        lines.append("")

        # Contact info line
        contact_parts = []
        if candidate.email:
            contact_parts.append(f"{candidate.email}")
        if candidate.phone:
            contact_parts.append(f"{candidate.phone}")
        if candidate.city and candidate.country:
            contact_parts.append(f"{candidate.city}, {candidate.country}")
        elif candidate.city:
            contact_parts.append(candidate.city)
        elif candidate.country:
            contact_parts.append(candidate.country)

        if contact_parts:
            lines.append(" | ".join(contact_parts))
            lines.append("")

        # LinkedIn
        if candidate.linkedin_url:
            lines.append(f"**LinkedIn:** {candidate.linkedin_url}")
            lines.append("")

        # Professional Experience
        if experiences:
            lines.append(f"## {headers['experience']}")
            lines.append("")

            # Sort by start_date descending (most recent first)
            sorted_experiences = sorted(
                experiences,
                key=lambda x: x.start_date,
                reverse=True
            )

            for exp in sorted_experiences:
                date_range = ProfileMarkdownService._format_date_range(
                    exp.start_date, exp.end_date, language
                )
                lines.append(f"### {exp.job_title} @ {exp.company}")
                lines.append(f"*{date_range}*")
                lines.append("")
                if exp.description:
                    # Split description into bullet points if it contains newlines
                    for line in exp.description.strip().split("\n"):
                        if line.strip():
                            if not line.strip().startswith("-"):
                                lines.append(f"- {line.strip()}")
                            else:
                                lines.append(line.strip())
                    lines.append("")

        # Education
        if education:
            lines.append(f"## {headers['education']}")
            lines.append("")

            # Sort by start_date descending
            sorted_education = sorted(
                education,
                key=lambda x: x.start_date,
                reverse=True
            )

            for edu in sorted_education:
                date_range = ProfileMarkdownService._format_date_range(
                    edu.start_date, edu.end_date, language
                )
                lines.append(f"### {edu.degree}")
                lines.append(f"**{edu.institution}** | *{date_range}*")
                lines.append("")
                if edu.description:
                    lines.append(edu.description.strip())
                    lines.append("")

        # Skills
        if candidate.skills:
            lines.append(f"## {headers['skills']}")
            lines.append("")
            lines.append(", ".join(candidate.skills))
            lines.append("")

        # Projects
        if projects:
            lines.append(f"## {headers['projects']}")
            lines.append("")

            # Sort by start_date descending
            sorted_projects = sorted(
                projects,
                key=lambda x: x.start_date,
                reverse=True
            )

            for proj in sorted_projects:
                date_range = ProfileMarkdownService._format_date_range(
                    proj.start_date, proj.end_date, language
                )
                lines.append(f"### {proj.name}")
                lines.append(f"*{date_range}*")
                lines.append("")
                if proj.description:
                    lines.append(proj.description.strip())
                    lines.append("")

        # Languages
        if candidate.languages:
            lines.append(f"## {headers['languages']}")
            lines.append("")
            for lang, level in candidate.languages.items():
                lang_name = lang.value if hasattr(lang, 'value') else str(lang)
                level_name = level.value if hasattr(level, 'value') else str(level)
                lines.append(f"- **{lang_name}**: {level_name}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def render_json_snapshot(
            candidate: Candidate,
            experiences: List[CandidateExperience],
            education: List[CandidateEducation],
            projects: List[CandidateProject]
    ) -> Dict[str, Any]:
        """
        Create a JSON snapshot of candidate profile.

        Args:
            candidate: The candidate entity
            experiences: List of work experiences
            education: List of education entries
            projects: List of projects

        Returns:
            Dictionary with structured profile data
        """
        return {
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "city": candidate.city,
            "country": candidate.country,
            "linkedin_url": candidate.linkedin_url,
            "job_category": candidate.job_category.value if candidate.job_category else None,
            "skills": candidate.skills or [],
            "languages": {
                (lang.value if hasattr(lang, 'value') else str(lang)): (level.value if hasattr(level, 'value') else str(level))
                for lang, level in (candidate.languages or {}).items()
            },
            "experiences": [
                {
                    "job_title": exp.job_title,
                    "company": exp.company,
                    "description": exp.description,
                    "start_date": exp.start_date.isoformat() if exp.start_date else None,
                    "end_date": exp.end_date.isoformat() if exp.end_date else None
                }
                for exp in experiences
            ],
            "education": [
                {
                    "degree": edu.degree,
                    "institution": edu.institution,
                    "description": edu.description,
                    "start_date": edu.start_date.isoformat() if edu.start_date else None,
                    "end_date": edu.end_date.isoformat() if edu.end_date else None
                }
                for edu in education
            ],
            "projects": [
                {
                    "name": proj.name,
                    "description": proj.description,
                    "start_date": proj.start_date.isoformat() if proj.start_date else None,
                    "end_date": proj.end_date.isoformat() if proj.end_date else None
                }
                for proj in projects
            ]
        }

    @staticmethod
    def _get_headers(language: str) -> Dict[str, str]:
        """Get section headers in the specified language"""
        if language == "en":
            return {
                "experience": "Professional Experience",
                "education": "Education",
                "skills": "Skills",
                "projects": "Projects",
                "languages": "Languages"
            }
        # Default to Spanish
        return {
            "experience": "Experiencia Profesional",
            "education": "Educación",
            "skills": "Habilidades",
            "projects": "Proyectos",
            "languages": "Idiomas"
        }

    @staticmethod
    def _format_date_range(start: date, end: Optional[date], language: str) -> str:
        """Format a date range for display"""
        def format_date(d: date) -> str:
            months_es = [
                "", "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
            ]
            months_en = [
                "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]
            months = months_en if language == "en" else months_es
            return f"{months[d.month]} {d.year}"

        start_str = format_date(start)
        if end:
            end_str = format_date(end)
        else:
            end_str = "Presente" if language == "es" else "Present"

        return f"{start_str} - {end_str}"
