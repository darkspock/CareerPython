"""
Test data builder for Candidate domain
"""
from datetime import date, timedelta
from typing import Dict, List, Optional
from faker import Faker

from src.candidate.application.commands.create_candidate import CreateCandidateCommand
from src.candidate.application.commands.update_candidate import UpdateCandidateCommand
from src.candidate.domain.entities.candidate import Candidate
from src.candidate.domain.enums.candidate_enums import (
    CandidateStatusEnum, CandidateTypeEnum, WorkModalityEnum,
    LanguageEnum, LanguageLevelEnum, PositionRoleEnum
)
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.shared.domain.enums.job_category import JobCategoryEnum
from src.user.domain.value_objects.UserId import UserId

fake = Faker()


class CandidateMother:
    """Object Mother for creating Candidate test data"""

    @staticmethod
    def create_candidate_entity(
        candidate_id: Optional[CandidateId] = None,
        user_id: Optional[UserId] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        **kwargs
    ) -> Candidate:
        """Create a Candidate entity with test data"""
        return Candidate.create(
            id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08"),
            name=name or fake.name(),
            date_of_birth=kwargs.get('date_of_birth', fake.date_of_birth(minimum_age=18, maximum_age=65)),
            city=kwargs.get('city', fake.city()),
            country=kwargs.get('country', fake.country()),
            phone=kwargs.get('phone', fake.phone_number()),
            email=email or fake.email(),
            user_id=user_id or UserId.from_string("01HQ7K8NZFT7QK3SR3VEF05S09"),
            job_category=kwargs.get('job_category', JobCategoryEnum.TECHNOLOGY),
            candidate_type=kwargs.get('candidate_type', CandidateTypeEnum.BASIC),
            expected_annual_salary=kwargs.get('expected_annual_salary', fake.random_int(30000, 120000)),
            current_annual_salary=kwargs.get('current_annual_salary', fake.random_int(25000, 100000)),
            currency=kwargs.get('currency', 'EUR'),
            relocation=kwargs.get('relocation', fake.boolean()),
            work_modality=kwargs.get('work_modality', [WorkModalityEnum.REMOTE, WorkModalityEnum.HYBRID]),
            languages=kwargs.get('languages', {
                LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL,
                LanguageEnum.SPANISH: LanguageLevelEnum.PROFESSIONAL
            }),
            other_languages=kwargs.get('other_languages', 'Portuguese (Basic)'),
            linkedin_url=kwargs.get('linkedin_url', f"https://linkedin.com/in/{fake.user_name()}"),
            data_consent=kwargs.get('data_consent', True),
            data_consent_on=kwargs.get('data_consent_on', date.today()),
            current_roles=kwargs.get('current_roles', [PositionRoleEnum.TECHNOLOGY]),
            expected_roles=kwargs.get('expected_roles', [PositionRoleEnum.LEAD_INITIATIVES]),
            current_job_level=kwargs.get('current_job_level', JobPositionLevelEnum.MID),
            expected_job_level=kwargs.get('expected_job_level', JobPositionLevelEnum.SENIOR),
            skills=kwargs.get('skills', ['Python', 'FastAPI', 'PostgreSQL', 'Docker']),
            timezone=kwargs.get('timezone', 'Europe/Madrid'),
            candidate_notes=kwargs.get('candidate_notes', fake.text(max_nb_chars=200))
        )

    @staticmethod
    def create_candidate_command(
        candidate_id: Optional[CandidateId] = None,
        user_id: Optional[UserId] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        **kwargs
    ) -> CreateCandidateCommand:
        """Create a CreateCandidateCommand with test data"""
        return CreateCandidateCommand(
            id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08"),
            name=name or fake.name(),
            date_of_birth=kwargs.get('date_of_birth', fake.date_of_birth(minimum_age=18, maximum_age=65)),
            city=kwargs.get('city', fake.city()),
            country=kwargs.get('country', fake.country()),
            phone=kwargs.get('phone', fake.phone_number()),
            email=email or fake.email(),
            user_id=user_id or UserId.from_string("01HQ7K8NZFT7QK3SR3VEF05S09"),
            job_category=kwargs.get('job_category', JobCategoryEnum.TECHNOLOGY),
            candidate_type=kwargs.get('candidate_type', CandidateTypeEnum.BASIC),
            expected_annual_salary=kwargs.get('expected_annual_salary', fake.random_int(30000, 120000)),
            current_annual_salary=kwargs.get('current_annual_salary', fake.random_int(25000, 100000)),
            currency=kwargs.get('currency', 'EUR'),
            relocation=kwargs.get('relocation', fake.boolean()),
            work_modality=kwargs.get('work_modality', [WorkModalityEnum.REMOTE, WorkModalityEnum.HYBRID]),
            languages=kwargs.get('languages', {
                LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL,
                LanguageEnum.SPANISH: LanguageLevelEnum.PROFESSIONAL
            }),
            other_languages=kwargs.get('other_languages', 'Portuguese (Basic)'),
            linkedin_url=kwargs.get('linkedin_url', f"https://linkedin.com/in/{fake.user_name()}"),
            data_consent=kwargs.get('data_consent', True),
            data_consent_on=kwargs.get('data_consent_on', date.today()),
            current_roles=kwargs.get('current_roles', [PositionRoleEnum.TECHNOLOGY]),
            expected_roles=kwargs.get('expected_roles', [PositionRoleEnum.LEAD_INITIATIVES]),
            current_job_level=kwargs.get('current_job_level', JobPositionLevelEnum.MID),
            expected_job_level=kwargs.get('expected_job_level', JobPositionLevelEnum.SENIOR),
            skills=kwargs.get('skills', ['Python', 'FastAPI', 'PostgreSQL', 'Docker']),
            timezone=kwargs.get('timezone', 'Europe/Madrid'),
            candidate_notes=kwargs.get('candidate_notes', fake.text(max_nb_chars=200))
        )

    @staticmethod
    def create_update_candidate_command(
        candidate_id: CandidateId,
        **kwargs
    ) -> UpdateCandidateCommand:
        """Create an UpdateCandidateCommand with test data"""
        return UpdateCandidateCommand(
            id=candidate_id,
            name=kwargs.get('name', fake.name()),
            date_of_birth=kwargs.get('date_of_birth', fake.date_of_birth(minimum_age=18, maximum_age=65)),
            city=kwargs.get('city', fake.city()),
            country=kwargs.get('country', fake.country()),
            phone=kwargs.get('phone', fake.phone_number()),
            email=kwargs.get('email', fake.email()),
            job_category=kwargs.get('job_category', JobCategoryEnum.TECHNOLOGY),
            candidate_type=kwargs.get('candidate_type', CandidateTypeEnum.BASIC),
            expected_annual_salary=kwargs.get('expected_annual_salary', fake.random_int(30000, 120000)),
            current_annual_salary=kwargs.get('current_annual_salary', fake.random_int(25000, 100000)),
            currency=kwargs.get('currency', 'USD'),
            relocation=kwargs.get('relocation', fake.boolean()),
            work_modality=kwargs.get('work_modality', [WorkModalityEnum.ON_SITE]),
            languages=kwargs.get('languages', {
                LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL,
                LanguageEnum.FRENCH: LanguageLevelEnum.CONVERSATIONAL
            }),
            other_languages=kwargs.get('other_languages', 'German (Beginner)'),
            linkedin_url=kwargs.get('linkedin_url', f"https://linkedin.com/in/{fake.user_name()}-updated"),
            current_roles=kwargs.get('current_roles', [PositionRoleEnum.TECHNOLOGY]),
            expected_roles=kwargs.get('expected_roles', [PositionRoleEnum.LEAD_INITIATIVES]),
            current_job_level=kwargs.get('current_job_level', JobPositionLevelEnum.SENIOR),
            expected_job_level=kwargs.get('expected_job_level', JobPositionLevelEnum.LEAD),
            skills=kwargs.get('skills', ['Python', 'React', 'TypeScript', 'AWS']),
            timezone=kwargs.get('timezone', 'America/New_York'),
            candidate_notes=kwargs.get('candidate_notes', 'Updated candidate notes')
        )