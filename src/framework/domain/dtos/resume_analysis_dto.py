"""DTOs for resume analysis results."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from ..enums.job_category import JobCategoryEnum

if TYPE_CHECKING:
    from ..value_objects.resume_analysis_result import ResumeAnalysisResult


@dataclass
class CandidateInfoDto:
    """DTO for candidate basic information from resume analysis."""
    name: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    country: Optional[str]
    email: Optional[str]
    linkedin_url: Optional[str]
    skills: List[str]
    job_category: Optional[JobCategoryEnum]


@dataclass
class ExperienceDto:
    """DTO for work experience from resume analysis."""
    job_title: str
    company: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


@dataclass
class EducationDto:
    """DTO for education from resume analysis."""
    degree: str
    institution: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


@dataclass
class ProjectDto:
    """DTO for project from resume analysis."""
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]


@dataclass
class ResumeAnalysisDto:
    """DTO for complete resume analysis result."""
    candidate_info: CandidateInfoDto
    experiences: List[ExperienceDto]
    educations: List[EducationDto]
    projects: List[ProjectDto]
    skills: List[str]
    success: bool
    confidence_score: float
    error_message: Optional[str] = None

    @classmethod
    def from_xai_result(cls, xai_result: "ResumeAnalysisResult") -> "ResumeAnalysisDto":
        """Create DTO from XAI service result."""
        from ..value_objects.resume_analysis_result import ResumeAnalysisResult

        if not isinstance(xai_result, ResumeAnalysisResult):
            raise ValueError("Expected ResumeAnalysisResult instance")

        # Parse candidate info
        candidate_data = xai_result.candidate_info
        job_category = None
        if candidate_data.get("job_category"):
            try:
                job_category = JobCategoryEnum(candidate_data["job_category"])
            except ValueError:
                job_category = JobCategoryEnum.OTHER

        candidate_info = CandidateInfoDto(
            name=candidate_data.get("name"),
            phone=candidate_data.get("phone"),
            city=candidate_data.get("city"),
            country=candidate_data.get("country"),
            email=candidate_data.get("email"),
            linkedin_url=candidate_data.get("linkedin_url"),
            skills=candidate_data.get("skills", []),
            job_category=job_category
        )

        # Parse experiences
        experiences = []
        for exp_data in xai_result.experiences:
            start_date = cls._parse_date(exp_data.get("start_date"))
            end_date = cls._parse_date(exp_data.get("end_date"))

            experiences.append(ExperienceDto(
                job_title=exp_data.get("job_title", ""),
                company=exp_data.get("company", ""),
                description=exp_data.get("description"),
                start_date=start_date,
                end_date=end_date
            ))

        # Parse educations
        educations = []
        for edu_data in xai_result.educations:
            start_date = cls._parse_date(edu_data.get("start_date"))
            end_date = cls._parse_date(edu_data.get("end_date"))

            educations.append(EducationDto(
                degree=edu_data.get("degree", ""),
                institution=edu_data.get("institution", ""),
                description=edu_data.get("description"),
                start_date=start_date,
                end_date=end_date
            ))

        # Parse projects
        projects = []
        for proj_data in xai_result.projects:
            start_date = cls._parse_date(proj_data.get("start_date"))
            end_date = cls._parse_date(proj_data.get("end_date"))

            projects.append(ProjectDto(
                name=proj_data.get("name", ""),
                description=proj_data.get("description"),
                start_date=start_date,
                end_date=end_date
            ))

        return cls(
            candidate_info=candidate_info,
            experiences=experiences,
            educations=educations,
            projects=projects,
            skills=xai_result.skills,
            success=xai_result.success,
            confidence_score=xai_result.confidence_score,
            error_message=xai_result.error_message
        )

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[date]:
        """Parse date string in YYYY-MM-DD format."""
        if not date_str or date_str == "null":
            return None

        try:
            from datetime import datetime
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None


@dataclass
class AsyncJobStatusDto:
    """DTO for async job status."""
    job_id: str
    job_type: str
    status: str
    progress: int
    message: Optional[str]
    estimated_time_remaining: Optional[int]
    started_at: Optional[str]
    timeout_seconds: int
    created_at: str
    updated_at: str


@dataclass
class AsyncJobResultDto:
    """DTO for async job results."""
    job_id: str
    job_type: str
    status: str
    success: bool
    results: Optional[Dict[str, Any]]
    error_message: Optional[str]
    completed_at: Optional[str]
