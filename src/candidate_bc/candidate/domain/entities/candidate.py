from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List, Dict

from src.candidate_bc.candidate.domain.enums.candidate_enums import CandidateStatusEnum, CandidateTypeEnum, WorkModalityEnum, \
    LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass
class Candidate:
    """Entidad del dominio para candidatos"""
    id: CandidateId
    name: str
    date_of_birth: date
    city: str
    country: str
    phone: str
    email: str
    user_id: UserId
    status: CandidateStatusEnum = CandidateStatusEnum.DRAFT
    job_category: JobCategoryEnum = JobCategoryEnum.OTHER
    candidate_type: CandidateTypeEnum = CandidateTypeEnum.BASIC
    expected_annual_salary: Optional[int] = None
    current_annual_salary: Optional[int] = None
    currency: Optional[str] = 'EUR'
    relocation: Optional[bool] = None
    work_modality: List[WorkModalityEnum] = field(default_factory=list)
    languages: Dict[LanguageEnum, LanguageLevelEnum] = field(default_factory=dict)
    other_languages: Optional[str] = None
    linkedin_url: Optional[str] = None
    data_consent: Optional[bool] = None
    data_consent_on: Optional[date] = None
    current_roles: List[PositionRoleEnum] = field(default_factory=list)
    expected_roles: List[PositionRoleEnum] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    current_job_level: Optional[JobPositionLevelEnum] = None
    expected_job_level: Optional[JobPositionLevelEnum] = None
    created_on: date = field(default_factory=date.today)
    updated_on: date = field(default_factory=date.today)
    timezone: Optional[str] = None
    candidate_notes: Optional[str] = None  # The candidate can add notes, like how to contact, availability, etc..

    def update_details(
            self,
            name: str,
            date_of_birth: date,
            city: str,
            country: str,
            phone: str,
            email: str,
            job_category: JobCategoryEnum,
            expected_annual_salary: Optional[int] = None,
            current_annual_salary: Optional[int] = None,
            currency: Optional[str] = None,
            relocation: Optional[bool] = None,
            work_modality: Optional[List[WorkModalityEnum]] = None,
            languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None,
            other_languages: Optional[str] = None,
            linkedin_url: Optional[str] = None,
            current_roles: Optional[List[PositionRoleEnum]] = None,
            expected_roles: Optional[List[PositionRoleEnum]] = None,
            current_job_level: Optional[JobPositionLevelEnum] = None,
            expected_job_level: Optional[JobPositionLevelEnum] = None,
            skills: Optional[List[str]] = None,
            timezone: Optional[str] = None,
            candidate_notes: Optional[str] = None
    ) -> None:
        """Actualiza los detalles del candidato"""
        self.name = name
        self.date_of_birth = date_of_birth
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.job_category = job_category
        self.expected_annual_salary = expected_annual_salary
        self.current_annual_salary = current_annual_salary
        self.currency = currency
        self.relocation = relocation
        self.work_modality = work_modality if work_modality is not None else self.work_modality
        self.languages = languages if languages is not None else self.languages
        self.other_languages = other_languages
        self.linkedin_url = linkedin_url
        self.current_roles = current_roles if current_roles is not None else self.current_roles
        self.expected_roles = expected_roles if expected_roles is not None else self.expected_roles
        self.current_job_level = current_job_level
        self.expected_job_level = expected_job_level
        self.skills = skills if skills is not None else self.skills
        self.timezone = timezone
        self.candidate_notes = candidate_notes

    def complete(self) -> None:
        self.status = CandidateStatusEnum.COMPLETE

    def delete(self) -> None:
        self.status = CandidateStatusEnum.DELETED

    @staticmethod
    def create(
            id: CandidateId,
            name: str,
            date_of_birth: date,
            city: str,
            country: str,
            phone: str,
            email: str,
            user_id: UserId,
            job_category: JobCategoryEnum = JobCategoryEnum.OTHER,
            candidate_type: CandidateTypeEnum = CandidateTypeEnum.BASIC,
            expected_annual_salary: Optional[int] = None,
            current_annual_salary: Optional[int] = None,
            currency: Optional[str] = None,
            relocation: Optional[bool] = None,
            work_modality: Optional[List[WorkModalityEnum]] = None,
            languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None,
            other_languages: Optional[str] = None,
            linkedin_url: Optional[str] = None,
            data_consent: Optional[bool] = None,
            data_consent_on: Optional[date] = None,
            current_roles: Optional[List[PositionRoleEnum]] = None,
            expected_roles: Optional[List[PositionRoleEnum]] = None,
            current_job_level: Optional[JobPositionLevelEnum] = None,
            expected_job_level: Optional[JobPositionLevelEnum] = None,
            skills: Optional[List[str]] = None,
            timezone: Optional[str] = None,
            candidate_notes: Optional[str] = None
    ) -> 'Candidate':
        return Candidate(
            id=id,
            name=name,
            date_of_birth=date_of_birth,
            city=city,
            country=country,
            phone=phone,
            email=email,
            user_id=user_id,
            status=CandidateStatusEnum.DRAFT,
            job_category=job_category,
            candidate_type=candidate_type,
            expected_annual_salary=expected_annual_salary,
            current_annual_salary=current_annual_salary,
            currency=currency,
            relocation=relocation,
            work_modality=work_modality or [],
            languages=languages or {},
            other_languages=other_languages,
            linkedin_url=linkedin_url,
            data_consent=data_consent,
            data_consent_on=data_consent_on,
            current_roles=current_roles or [],
            expected_roles=expected_roles or [],
            current_job_level=current_job_level,
            expected_job_level=expected_job_level,
            skills=skills or [],
            timezone=timezone,
            candidate_notes=candidate_notes
        )

    def update_basic(self, name: str, date_of_birth: date, city: str, country: str, phone: str, email: str,
                     job_category: JobCategoryEnum) -> None:
        self.name = name
        self.date_of_birth = date_of_birth
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.job_category = job_category
