"""Candidate domain value objects."""

from .candidate_education_id import CandidateEducationId
from .candidate_experience_id import CandidateExperienceId
from .candidate_id import CandidateId
from .candidate_project_id import CandidateProjectId

__all__ = [
    "CandidateId",
    "CandidateExperienceId",
    "CandidateProjectId",
    "CandidateEducationId"
]
