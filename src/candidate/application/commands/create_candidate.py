from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Dict

from core.event_bus import EventBus
from src.candidate.domain.entities.candidate import Candidate
from src.candidate.domain.enums import CandidateTypeEnum
from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum, \
    WorkModalityEnum
from src.candidate.domain.events.candidate_created_event import CandidateCreatedEvent
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.enums.job_category import JobCategoryEnum
from src.user.domain.value_objects.UserId import UserId


@dataclass
class CreateCandidateCommand(Command):
    id: CandidateId
    name: str
    date_of_birth: date
    city: str
    country: str
    phone: str
    email: str
    user_id: UserId
    job_category: Optional[JobCategoryEnum] = None
    candidate_type: Optional[CandidateTypeEnum] = None
    expected_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: Optional[List[WorkModalityEnum]] = None
    languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None
    other_languages: Optional[str] = None
    current_annual_salary: Optional[int] = None
    linkedin_url: Optional[str] = None
    data_consent: Optional[bool] = None
    data_consent_on: Optional[date] = None
    current_roles: Optional[List[PositionRoleEnum]] = None
    expected_roles: Optional[List[PositionRoleEnum]] = None
    skills: Optional[List[str]] = None
    current_job_level: Optional[JobPositionLevelEnum] = None
    expected_job_level: Optional[JobPositionLevelEnum] = None
    timezone: Optional[str] = None
    candidate_notes: Optional[str] = None


class CreateCandidateCommandHandler(CommandHandler[CreateCandidateCommand]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface, event_bus: EventBus):
        self.candidate_repository = candidate_repository
        self.event_bus = event_bus

    def execute(self, command: CreateCandidateCommand) -> None:
        # Generate new candidate ID

        # Use date object directly (no conversion needed)
        date_of_birth_obj = command.date_of_birth

        # Use enum objects directly (no conversion needed)
        job_category = command.job_category if command.job_category else JobCategoryEnum.OTHER
        candidate_type = command.candidate_type if command.candidate_type else CandidateTypeEnum.BASIC

        # Use language dictionaries directly (no conversion needed)
        languages_dict = command.languages or {}

        # Use role enums directly (no conversion needed)
        current_roles_enums = command.current_roles or []
        expected_roles_enums = command.expected_roles or []

        # Use date object directly (no conversion needed)
        data_consent_on_obj = command.data_consent_on

        # Use job level enums directly (no conversion needed)
        current_job_level_enum = command.current_job_level
        expected_job_level_enum = command.expected_job_level

        # Create candidate using factory method
        new_candidate = Candidate.create(
            id=command.id,
            name=command.name,
            date_of_birth=date_of_birth_obj,
            city=command.city,
            country=command.country,
            phone=command.phone,
            email=command.email,
            user_id=command.user_id,
            job_category=job_category,
            candidate_type=candidate_type,
            expected_annual_salary=command.expected_annual_salary,
            current_annual_salary=command.current_annual_salary,
            currency=command.currency,
            relocation=command.relocation,
            work_modality=command.work_modality,
            languages=languages_dict,
            other_languages=command.other_languages,
            linkedin_url=command.linkedin_url,
            data_consent=command.data_consent,
            data_consent_on=data_consent_on_obj,
            current_roles=current_roles_enums,
            expected_roles=expected_roles_enums,
            current_job_level=current_job_level_enum,
            expected_job_level=expected_job_level_enum,
            skills=command.skills,
            timezone=command.timezone,
            candidate_notes=command.candidate_notes
        )

        # Save candidate
        self.candidate_repository.create(new_candidate)

        # Dispatch domain event
        self.event_bus.dispatch(CandidateCreatedEvent.create(id=command.id))
