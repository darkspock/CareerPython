"""
Test data builder for CandidateProject domain
"""
from typing import Optional
from faker import Faker

from src.candidate_bc.candidate.application.commands.create_project import CreateProjectCommand
from src.candidate_bc.candidate.application.commands.update_project import UpdateProjectCommand
from src.candidate_bc.candidate.domain.entities.candidate_project import CandidateProject
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId

fake = Faker()


class ProjectMother:
    """Object Mother for creating CandidateProject test data"""

    @staticmethod
    def create_project_entity(
        project_id: Optional[CandidateProjectId] = None,
        candidate_id: Optional[CandidateId] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> CandidateProject:
        """Create a CandidateProject entity with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-3y', end_date='-1y'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        project_names = [
            "E-commerce Platform",
            "Task Management System",
            "Mobile Banking App",
            "Inventory Management System",
            "Social Media Dashboard",
            "API Gateway Service",
            "Data Analytics Platform",
            "Customer Support Portal"
        ]

        return CandidateProject.create(
            id=project_id or CandidateProjectId.generate(),
            candidate_id=candidate_id or CandidateId.generate(),
            name=name or fake.random_element(project_names),
            description=kwargs.get('description', fake.text(max_nb_chars=400)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_ongoing_project_entity(
        project_id: Optional[CandidateProjectId] = None,
        candidate_id: Optional[CandidateId] = None,
        **kwargs
    ) -> CandidateProject:
        """Create an ongoing CandidateProject entity (no end date)"""
        return ProjectMother.create_project_entity(
            project_id=project_id,
            candidate_id=candidate_id,
            name=kwargs.get('name', 'AI-Powered Career Platform'),
            start_date=kwargs.get('start_date', fake.date_between(start_date='-1y', end_date='-3m')),
            end_date=None,
            description=kwargs.get(
                'description',
                'Ongoing development of a comprehensive career management platform with AI features'
            ),
            **kwargs
        )

    @staticmethod
    def create_project_command(
        project_id: Optional[CandidateProjectId] = None,
        candidate_id: Optional[CandidateId] = None,
        name: Optional[str] = None,
        **kwargs
    ) -> CreateProjectCommand:
        """Create a CreateProjectCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-3y', end_date='-1y'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        project_names = [
            "E-commerce Platform",
            "Task Management System",
            "Mobile Banking App",
            "Inventory Management System",
            "Social Media Dashboard",
            "API Gateway Service"
        ]

        return CreateProjectCommand(
            id=project_id or CandidateProjectId.generate(),
            candidate_id=candidate_id or CandidateId.generate(),
            name=name or fake.random_element(project_names),
            description=kwargs.get('description', fake.text(max_nb_chars=400)),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_update_project_command(
        project_id: CandidateProjectId,
        **kwargs
    ) -> UpdateProjectCommand:
        """Create an UpdateProjectCommand with test data"""
        start_date = kwargs.get('start_date', fake.date_between(start_date='-2y', end_date='-6m'))
        end_date = kwargs.get('end_date', fake.date_between(start_date=start_date, end_date='today'))

        return UpdateProjectCommand(
            id=project_id,
            name=kwargs.get('name', 'Updated Project Name'),
            description=kwargs.get('description', 'Updated project description with enhanced features'),
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def create_github_project_command(
        project_id: Optional[CandidateProjectId] = None,
        candidate_id: Optional[CandidateId] = None
    ) -> CreateProjectCommand:
        """Create a CreateProjectCommand for a GitHub project"""
        return CreateProjectCommand(
            id=project_id or CandidateProjectId.generate(),
            candidate_id=candidate_id or CandidateId.generate(),
            name="Open Source Library",
            description="Developed and maintained an open source Python library for data processing with 1000+ GitHub stars",
            start_date=fake.date_between(start_date='-2y', end_date='-1y'),
            end_date=fake.date_between(start_date='-1y', end_date='-2m')
        )