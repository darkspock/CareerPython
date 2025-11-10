from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Dict

from src.candidate_bc.candidate.domain.enums import CandidateTypeEnum, WorkModalityEnum
from src.candidate_bc.candidate.domain.enums.candidate_enums import PositionRoleEnum, LanguageEnum, LanguageLevelEnum
from src.candidate_bc.candidate.domain.exceptions.candidate_exceptions import CandidateNotFoundException
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class UpdateCandidateCommand(Command):
    id: CandidateId
    name: str
    date_of_birth: date
    city: str
    country: str
    phone: str
    email: str
    job_category: JobCategoryEnum
    candidate_type: CandidateTypeEnum
    expected_annual_salary: Optional[int]
    currency: Optional[str]
    relocation: bool
    work_modality: Optional[List[WorkModalityEnum]]
    languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]]
    other_languages: Optional[str]
    current_annual_salary: Optional[int]
    linkedin_url: Optional[str]
    current_roles: Optional[List[PositionRoleEnum]]
    expected_roles: Optional[List[PositionRoleEnum]]
    skills: Optional[List[str]]
    current_job_level: Optional[JobPositionLevelEnum]
    expected_job_level: Optional[JobPositionLevelEnum]
    timezone: Optional[str]
    candidate_notes: Optional[str]


class UpdateCandidateCommandHandler(CommandHandler[UpdateCandidateCommand]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def execute(self, command: UpdateCandidateCommand) -> None:
        # Get existing candidate
        existing_candidate = self.candidate_repository.get_by_id(command.id)
        if not existing_candidate:
            raise CandidateNotFoundException(f"Candidate with id {command.id} not found")

        existing_candidate.update_details(
            name=command.name,
            date_of_birth=command.date_of_birth,
            city=command.city,
            country=command.country,
            phone=command.phone,
            email=command.email,
            job_category=command.job_category,
            expected_annual_salary=command.expected_annual_salary,
            currency=command.currency,
            relocation=command.relocation,
            work_modality=command.work_modality,
            languages=command.languages,
            other_languages=command.other_languages,
            current_annual_salary=command.current_annual_salary,
            linkedin_url=command.linkedin_url,
            current_roles=command.current_roles,
            expected_roles=command.expected_roles,
            current_job_level=command.current_job_level,
            expected_job_level=command.expected_job_level,
            skills=command.skills,
            timezone=command.timezone,
            candidate_notes=command.candidate_notes
        )

        # Save updated candidate
        self.candidate_repository.update(existing_candidate)
