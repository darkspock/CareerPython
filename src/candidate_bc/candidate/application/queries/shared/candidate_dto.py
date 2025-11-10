from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Dict

from src.candidate_bc.candidate.domain.entities import Candidate
from src.candidate_bc.candidate.domain.enums import CandidateStatusEnum, LanguageEnum, LanguageLevelEnum, CandidateTypeEnum, \
    WorkModalityEnum
from src.candidate_bc.candidate.domain.enums.candidate_enums import PositionRoleEnum
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass
class CandidateDto:
    id: CandidateId
    name: str
    date_of_birth: date
    city: str
    country: str
    phone: str
    email: str
    user_id: UserId
    status: CandidateStatusEnum
    job_category: JobCategoryEnum
    created_at: date
    updated_at: date
    linkedin_url: Optional[str] = None
    expected_annual_salary: Optional[int] = None
    current_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: Optional[List[WorkModalityEnum]] = None
    languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None
    skills: Optional[List[str]] = None
    current_roles: Optional[List[PositionRoleEnum]] = None
    expected_roles: Optional[List[PositionRoleEnum]] = None
    type: CandidateTypeEnum = CandidateTypeEnum.BASIC

    @classmethod
    def from_entity(cls, candidate: Candidate) -> 'CandidateDto':
        return cls(
            id=candidate.id,
            name=candidate.name,
            date_of_birth=candidate.date_of_birth,
            city=candidate.city,
            country=candidate.country,
            phone=candidate.phone,
            email=candidate.email,
            user_id=candidate.user_id,
            status=candidate.status,
            job_category=candidate.job_category,
            linkedin_url=candidate.linkedin_url,
            expected_annual_salary=candidate.expected_annual_salary,
            current_annual_salary=candidate.current_annual_salary,
            currency=candidate.currency,
            relocation=candidate.relocation,
            work_modality=candidate.work_modality,
            languages=candidate.languages,
            skills=candidate.skills,
            current_roles=candidate.current_roles,
            expected_roles=candidate.expected_roles,
            type=candidate.candidate_type,
            created_at=candidate.created_on,
            updated_at=candidate.updated_on
        )
