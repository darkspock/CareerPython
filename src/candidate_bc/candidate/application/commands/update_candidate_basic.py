from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Dict

from src.candidate_bc.candidate.domain.enums import WorkModalityEnum
from src.candidate_bc.candidate.domain.enums.candidate_enums import PositionRoleEnum, LanguageEnum, LanguageLevelEnum
from src.candidate_bc.candidate.domain.exceptions.candidate_exceptions import CandidateNotFoundException
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class UpdateCandidateBasicCommand(Command):
    id: CandidateId
    name: str
    date_of_birth: date
    city: str
    country: str
    phone: str
    email: str
    job_category: JobCategoryEnum
    linkedin_url: Optional[str] = None
    # Extended fields
    expected_annual_salary: Optional[int] = None
    current_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: Optional[List[WorkModalityEnum]] = None
    languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None
    skills: Optional[List[str]] = None
    current_roles: Optional[List[PositionRoleEnum]] = None
    expected_roles: Optional[List[PositionRoleEnum]] = None


class UpdateCandidateCommandHandler(CommandHandler[UpdateCandidateBasicCommand]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def execute(self, command: UpdateCandidateBasicCommand) -> None:
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
            other_languages=None,
            current_annual_salary=command.current_annual_salary,
            linkedin_url=command.linkedin_url,
            current_roles=command.current_roles,
            expected_roles=command.expected_roles,
            skills=command.skills,
            current_job_level=None,
            expected_job_level=None,
            timezone=None,
            candidate_notes=None
        )

        # Save updated candidate
        self.candidate_repository.update(existing_candidate)
