"""
Test data builder for CandidateEducation domain
"""
from datetime import date
from typing import Optional
from faker import Faker

from src.candidate.application.commands.create_education import CreateEducationCommand
from src.candidate.application.commands.update_education import UpdateEducationCommand
from src.candidate.domain.entities.candidate_education import CandidateEducation
from src.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate.domain.value_objects.candidate_id import CandidateId

fake = Faker()


class EducationMother:
    """Object Mother for creating CandidateEducation test data"""

    @staticmethod
    def create_education_entity(
        education_id: Optional[CandidateEducationId] = None,
        candidate_id: Optional[CandidateId] = None,
        degree: Optional[str] = None,
        institution: Optional[str] = None,
        **kwargs
    ) -> CandidateEducation:
        """Create a CandidateEducation entity with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-10y', end_date='-6y'))
        if 'end_date' in kwargs:
            end_date = kwargs['end_date']
        else:
            # Generate end_date after start_date, but not later than 1 year ago
            import datetime
            max_end_date = min(start_date + datetime.timedelta(days=365*4), date.today() - datetime.timedelta(days=365))
            end_date = fake.date_between(start_date=start_date, end_date=max_end_date)

        degrees = [
            "Bachelor's in Computer Science",
            "Master's in Software Engineering",
            "Bachelor's in Information Technology",
            "Master's in Data Science",
            "Bachelor's in Mathematics"
        ]

        institutions = [
            "University of Technology",
            "State University",
            "Technical Institute",
            "Engineering College",
            "Computer Science University"
        ]

        return CandidateEducation.create(
            id=education_id or CandidateEducationId.from_string("01HQ7K8NZFT7QK3SR3VEF05S09"),
            candidate_id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S10"),
            degree=degree or fake.random_element(degrees),
            institution=institution or fake.random_element(institutions),
            description=kwargs.get('description', fake.text(max_nb_chars=300)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_ongoing_education_entity(
        education_id: Optional[CandidateEducationId] = None,
        candidate_id: Optional[CandidateId] = None,
        **kwargs
    ) -> CandidateEducation:
        """Create an ongoing CandidateEducation entity (no end date)"""
        return EducationMother.create_education_entity(
            education_id=education_id,
            candidate_id=candidate_id,
            degree=kwargs.get('degree', "Master's in Artificial Intelligence"),
            institution=kwargs.get('institution', "Advanced Technology Institute"),
            start_date=kwargs.get('start_date', fake.date_between(start_date='-2y', end_date='-1y')),
            end_date=None,
            **kwargs
        )

    @staticmethod
    def create_education_command(
        education_id: Optional[CandidateEducationId] = None,
        candidate_id: Optional[CandidateId] = None,
        degree: Optional[str] = None,
        institution: Optional[str] = None,
        **kwargs
    ) -> CreateEducationCommand:
        """Create a CreateEducationCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-10y', end_date='-6y'))
        if 'end_date' in kwargs:
            end_date = kwargs['end_date']
        else:
            # Generate end_date after start_date, but not later than 1 year ago
            import datetime
            max_end_date = min(start_date + datetime.timedelta(days=365*4), date.today() - datetime.timedelta(days=365))
            end_date = fake.date_between(start_date=start_date, end_date=max_end_date)

        degrees = [
            "Bachelor's in Computer Science",
            "Master's in Software Engineering",
            "Bachelor's in Information Technology",
            "Master's in Data Science"
        ]

        institutions = [
            "University of Technology",
            "State University",
            "Technical Institute",
            "Engineering College"
        ]

        return CreateEducationCommand(
            id=education_id or CandidateEducationId.from_string("01HQ7K8NZFT7QK3SR3VEF05S09"),
            candidate_id=candidate_id or CandidateId.from_string("01HQ7K8NZFT7QK3SR3VEF05S10"),
            degree=degree or fake.random_element(degrees),
            institution=institution or fake.random_element(institutions),
            description=kwargs.get('description', fake.text(max_nb_chars=300)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_update_education_command(
        education_id: CandidateEducationId,
        **kwargs
    ) -> UpdateEducationCommand:
        """Create an UpdateEducationCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-8y', end_date='-4y'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='-1y'))

        return UpdateEducationCommand(
            id=education_id,
            degree=kwargs.get('degree', "Master's in Computer Science"),
            institution=kwargs.get('institution', "Updated University"),
            description=kwargs.get('description', 'Updated education description with additional coursework'),
            start_date=start_date,
            end_date=end_date
        )