"""Candidate application module - exports queries and commands"""

# Commands
from .commands import (
    CreateCandidateCommand,
    CreateCandidateCommandHandler,
    UpdateCandidateCommand,
    UpdateCandidateCommandHandler,
)
# Queries
from .queries import (
    GetCandidateByIdQuery,
    GetCandidateByIdQueryHandler,
    GetCandidateByUserIdQuery,
    GetCandidateByUserIdQueryHandler,
    GetEducationByIdQuery,
    GetEducationByIdQueryHandler,
    GetProjectByIdQuery,
    GetProjectByIdQueryHandler,
    ListCandidatesQuery,
    ListCandidatesQueryHandler,
    ListCandidateEducationsByCandidateIdQuery,
    ListCandidateEducationsByCandidateIdQueryHandler,
    ListCandidateExperiencesByCandidateIdQuery,
    ListCandidateExperiencesByCandidateIdQueryHandler,
    ListCandidateProjectsByCandidateIdQuery,
    ListCandidateProjectsByCandidateIdQueryHandler,
    ReadCandidateQuery,
    ReadCandidateQueryHandler,
)

__all__ = [
    # Queries
    "GetCandidateByIdQuery",
    "GetCandidateByIdQueryHandler",
    "GetCandidateByUserIdQuery",
    "GetCandidateByUserIdQueryHandler",
    "GetEducationByIdQuery",
    "GetEducationByIdQueryHandler",
    "GetProjectByIdQuery",
    "GetProjectByIdQueryHandler",
    "ListCandidatesQuery",
    "ListCandidatesQueryHandler",
    "ListCandidateEducationsByCandidateIdQuery",
    "ListCandidateEducationsByCandidateIdQueryHandler",
    "ListCandidateExperiencesByCandidateIdQuery",
    "ListCandidateExperiencesByCandidateIdQueryHandler",
    "ListCandidateProjectsByCandidateIdQuery",
    "ListCandidateProjectsByCandidateIdQueryHandler",
    "ReadCandidateQuery",
    "ReadCandidateQueryHandler",
    # Commands
    "CreateCandidateCommand",
    "CreateCandidateCommandHandler",
    "UpdateCandidateCommand",
    "UpdateCandidateCommandHandler",
]
