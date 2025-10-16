"""
Test data builder for CandidateExperience domain
"""
from datetime import date, timedelta
from typing import Optional
from faker import Faker

from src.candidate.application.commands.create_experience import CreateExperienceCommand
from src.candidate.application.commands.update_experience import UpdateExperienceCommand
from src.candidate.domain.entities.candidate_experience import CandidateExperience
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate.domain.value_objects.candidate_id import CandidateId

fake = Faker()


class ExperienceMother:
    """Object Mother for creating CandidateExperience test data"""

    @staticmethod
    def create_experience_entity(
        experience_id: Optional[CandidateExperienceId] = None,
        candidate_id: Optional[CandidateId] = None,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> CandidateExperience:
        """Create a CandidateExperience entity with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-5y', end_date='-1y'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        return CandidateExperience.create(
            id=experience_id or CandidateExperienceId.from_string("01HQ7K8NZFT7QK3SR3VEF05S10"),
            candidate_id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08"),
            job_title=job_title or fake.job(),
            company=company or fake.company(),
            description=kwargs.get('description', fake.text(max_nb_chars=500)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_current_experience_entity(
        experience_id: Optional[CandidateExperienceId] = None,
        candidate_id: Optional[CandidateId] = None,
        **kwargs
    ) -> CandidateExperience:
        """Create a current CandidateExperience entity (no end date)"""
        return ExperienceMother.create_experience_entity(
            experience_id=experience_id,
            candidate_id=candidate_id,
            job_title=kwargs.get('job_title', 'Senior Software Engineer'),
            company=kwargs.get('company', 'TechCorp'),
            start_date=kwargs.get('start_date', fake.date_between(start_date='-2y', end_date='-6m')),
            end_date=None,
            **kwargs
        )

    @staticmethod
    def create_experience_command(
        experience_id: Optional[CandidateExperienceId] = None,
        candidate_id: Optional[CandidateId] = None,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        **kwargs
    ) -> CreateExperienceCommand:
        """Create a CreateExperienceCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-5y', end_date='-1y'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        return CreateExperienceCommand(
            id=experience_id or CandidateExperienceId.from_string("01HQ7K8NZFT7QK3SR3VEF05S10"),
            candidate_id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08"),
            job_title=job_title or fake.job(),
            company=company or fake.company(),
            description=kwargs.get('description', fake.text(max_nb_chars=500)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_update_experience_command(
        experience_id: CandidateExperienceId,
        **kwargs
    ) -> UpdateExperienceCommand:
        """Create an UpdateExperienceCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-3y', end_date='-6m'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        return UpdateExperienceCommand(
            id=experience_id,
            job_title=kwargs.get('job_title', 'Lead Software Engineer'),
            company=kwargs.get('company', 'Updated TechCorp'),
            description=kwargs.get('description', 'Updated experience description with new responsibilities'),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_invalid_date_command(
        experience_id: Optional[CandidateExperienceId] = None,
        candidate_id: Optional[CandidateId] = None
    ) -> CreateExperienceCommand:
        """Create a CreateExperienceCommand with invalid dates for testing validation"""
        start_date = date.today()
        end_date = start_date - timedelta(days=365)  # End date before start date

        return CreateExperienceCommand(
            id=experience_id or CandidateExperienceId.from_string("01HQ7K8NZFT7QK3SR3VEF05S10"),
            candidate_id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08"),
            job_title="Software Engineer",
            company="Test Company",
            description="Invalid date range experience",
            start_date=start_date,
            end_date=end_date
        )