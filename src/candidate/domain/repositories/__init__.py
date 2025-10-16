"""Candidate domain repositories."""

from .candiadate_experience_repository_interface import CandidateExperienceRepositoryInterface
from .candidate_education_repository_interface import CandidateEducationRepositoryInterface
from .candidate_project_repository_interface import CandidateProjectRepositoryInterface
from .candidate_repository_interface import CandidateRepositoryInterface

__all__ = [
    "CandidateRepositoryInterface",
    "CandidateEducationRepositoryInterface",
    "CandidateExperienceRepositoryInterface",
    "CandidateProjectRepositoryInterface"
]
