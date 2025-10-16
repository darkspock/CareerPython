from dataclasses import dataclass
from typing import Optional, List, Any

from src.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate.application.queries.shared.candidate_education_dto import CandidateEducationDto
from src.candidate.application.queries.shared.candidate_experience_dto import CandidateExperienceDto
from src.candidate.application.queries.shared.candidate_project_dto import CandidateProjectDto
from src.candidate.domain.entities import Candidate
from src.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate.domain.repositories.candidate_project_repository_interface import CandidateProjectRepositoryInterface
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.shared.application.query_bus import Query


@dataclass
class CandidateDetailedProfile:
    """Complete candidate profile with all related data"""
    candidate: CandidateDto
    experiences: List[CandidateExperienceDto]
    education: List[CandidateEducationDto]
    projects: List[CandidateProjectDto]
    interviews_count: int
    applications_count: int
    resume_count: int
    last_activity: Optional[str]
    profile_completion_percentage: int


@dataclass
class GetCandidateDetailedProfileQuery(Query):
    id: CandidateId


class GetCandidateDetailedProfileQueryHandler:
    def __init__(self,
                 candidate_repository: CandidateRepositoryInterface,
                 candidate_experience_repository: CandidateExperienceRepositoryInterface,
                 candidate_education_repository: CandidateEducationRepositoryInterface,
                 candidate_project_repository: CandidateProjectRepositoryInterface):
        self.candidate_repository = candidate_repository
        self.candidate_experience_repository = candidate_experience_repository
        self.candidate_education_repository = candidate_education_repository
        self.candidate_project_repository = candidate_project_repository

    def execute(self, query: GetCandidateDetailedProfileQuery) -> Optional[CandidateDetailedProfile]:
        # Get candidate basic info
        candidate = self.candidate_repository.get_by_id(query.id)
        if not candidate:
            return None

        # Get all related data
        experiences = self.candidate_experience_repository.get_by_candidate_id(query.id)
        education = self.candidate_education_repository.get_by_candidate_id(query.id)
        projects = self.candidate_project_repository.get_by_candidate_id(query.id)

        # Calculate metrics (placeholder implementations)
        interviews_count = 0  # TODO: Implement actual count from interview repository
        applications_count = 0  # TODO: Implement actual count from applications repository
        resume_count = 0  # TODO: Implement actual count from resume repository
        last_activity = None  # TODO: Implement based on latest activity timestamp

        # Calculate profile completion percentage
        profile_completion = self._calculate_profile_completion(candidate, experiences, education, projects)

        return CandidateDetailedProfile(
            candidate=CandidateDto.from_entity(candidate),
            experiences=[CandidateExperienceDto.from_entity(exp) for exp in experiences],
            education=[CandidateEducationDto.from_entity(edu) for edu in education],
            projects=[CandidateProjectDto.from_entity(proj) for proj in projects],
            interviews_count=interviews_count,
            applications_count=applications_count,
            resume_count=resume_count,
            last_activity=last_activity,
            profile_completion_percentage=profile_completion
        )

    def _calculate_profile_completion(self, candidate: Candidate, experiences: List[Any],
                                      education: List[Any], projects: List[Any]) -> int:
        """Calculate profile completion percentage"""
        total_fields = 10
        completed_fields = 0

        # Basic info (weight: 5 points)
        if candidate.name:
            completed_fields += 1
        if candidate.email:
            completed_fields += 1
        if candidate.phone:
            completed_fields += 1
        if candidate.city and candidate.country:
            completed_fields += 1
        if candidate.job_category:
            completed_fields += 1

        # Professional info (weight: 3 points)
        if experiences:
            completed_fields += 2
        if education:
            completed_fields += 1
        if projects:
            completed_fields += 1

        # Additional info (weight: 2 points)
        if candidate.expected_annual_salary:
            completed_fields += 1

        return min(int((completed_fields / total_fields) * 100), 100)
