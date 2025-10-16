"""
Unit tests for Project commands
"""
import pytest
from datetime import date
from unittest.mock import Mock

from src.candidate.application.commands.create_project import CreateProjectCommand, CreateProjectCommandHandler
from src.candidate.application.commands.update_project import UpdateProjectCommand, UpdateProjectCommandHandler
from src.candidate.domain.entities.candidate_project import CandidateProject
from src.candidate.domain.exceptions.candidate_exceptions import ProjectNotFoundError
from src.candidate.domain.repositories.candidate_project_repository_interface import CandidateProjectRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from tests.unit.candidate.mothers.project_mother import ProjectMother


class TestCreateProjectCommand:
    """Test cases for CreateProjectCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.project_repository = Mock(spec=CandidateProjectRepositoryInterface)
        self.handler = CreateProjectCommandHandler(self.project_repository)

    def test_create_project_success(self):
        """Test successful project creation"""
        # Arrange
        command = ProjectMother.create_project_command()

        # Act
        self.handler.execute(command)

        # Assert
        self.project_repository.create.assert_called_once()
        created_project = self.project_repository.create.call_args[0][0]

        assert isinstance(created_project, CandidateProject)
        assert created_project.id == command.id
        assert created_project.candidate_id == command.candidate_id
        assert created_project.name == command.name
        assert created_project.description == command.description
        assert created_project.start_date == command.start_date
        assert created_project.end_date == command.end_date

    def test_create_ecommerce_project(self):
        """Test creating e-commerce project"""
        # Arrange
        command = ProjectMother.create_project_command(
            name="E-commerce Platform",
            start_date=date(2023, 1, 15),
            end_date=date(2023, 8, 30),
            description="Full-stack e-commerce platform with payment integration, inventory management, and admin dashboard"
        )

        # Act
        self.handler.execute(command)

        # Assert
        created_project = self.project_repository.create.call_args[0][0]
        assert created_project.name == "E-commerce Platform"
        assert "payment integration" in created_project.description
        assert "inventory management" in created_project.description

    def test_create_ongoing_project(self):
        """Test creating ongoing project (no end date)"""
        # Arrange
        command = ProjectMother.create_project_command(
            name="AI Research Platform",
            start_date=date(2024, 1, 1),
            end_date=None  # Ongoing
        )

        # Act
        self.handler.execute(command)

        # Assert
        created_project = self.project_repository.create.call_args[0][0]
        assert created_project.name == "AI Research Platform"
        assert created_project.end_date is None

    def test_create_github_project(self):
        """Test creating GitHub/open source project"""
        # Arrange
        command = ProjectMother.create_github_project_command()

        # Act
        self.handler.execute(command)

        # Assert
        created_project = self.project_repository.create.call_args[0][0]
        assert created_project.name == "Open Source Library"
        assert "GitHub stars" in created_project.description
        assert "Python library" in created_project.description


class TestUpdateProjectCommand:
    """Test cases for UpdateProjectCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.project_repository = Mock(spec=CandidateProjectRepositoryInterface)
        self.handler = UpdateProjectCommandHandler(self.project_repository)

    def test_update_project_success(self):
        """Test successful project update"""
        # Arrange
        project_id = CandidateProjectId.generate()
        existing_project = ProjectMother.create_project_entity(project_id=project_id)
        self.project_repository.get_by_id.return_value = existing_project

        command = ProjectMother.create_update_project_command(project_id)

        # Act
        self.handler.execute(command)

        # Assert
        self.project_repository.get_by_id.assert_called_once_with(project_id)
        self.project_repository.update.assert_called_once_with(project_id, existing_project)

        # Verify project was updated
        assert existing_project.name == command.name
        assert existing_project.description == command.description
        assert existing_project.start_date == command.start_date
        assert existing_project.end_date == command.end_date

    def test_update_project_not_found(self):
        """Test update command when project doesn't exist"""
        # Arrange
        project_id = CandidateProjectId.generate()
        self.project_repository.get_by_id.return_value = None

        command = ProjectMother.create_update_project_command(project_id)

        # Act & Assert
        with pytest.raises(ProjectNotFoundError):
            self.handler.execute(command)

        self.project_repository.get_by_id.assert_called_once_with(project_id)
        self.project_repository.update.assert_not_called()

    def test_update_project_from_ongoing_to_completed(self):
        """Test updating ongoing project to completed (adding end date)"""
        # Arrange
        project_id = CandidateProjectId.generate()
        existing_project = ProjectMother.create_ongoing_project_entity(project_id=project_id)
        self.project_repository.get_by_id.return_value = existing_project

        command = UpdateProjectCommand(
            id=project_id,
            name=existing_project.name,
            description="Project completed successfully with all features implemented",
            start_date=existing_project.start_date,
            end_date=date(2024, 6, 15)  # Now completed
        )

        # Act
        self.handler.execute(command)

        # Assert
        assert existing_project.end_date == date(2024, 6, 15)
        assert "completed successfully" in existing_project.description

    def test_update_project_scope_expansion(self):
        """Test updating project with expanded scope and extended timeline"""
        # Arrange
        project_id = CandidateProjectId.generate()
        existing_project = ProjectMother.create_project_entity(
            project_id=project_id,
            name="Simple Web App",
            end_date=date(2024, 3, 31)
        )
        self.project_repository.get_by_id.return_value = existing_project

        command = UpdateProjectCommand(
            id=project_id,
            name="Full-Stack Web Application with Microservices",  # Expanded name
            description="Expanded scope to include microservices architecture, containerization, and cloud deployment",
            start_date=existing_project.start_date,
            end_date=date(2024, 8, 31)  # Extended timeline
        )

        # Act
        self.handler.execute(command)

        # Assert
        assert existing_project.name == "Full-Stack Web Application with Microservices"
        assert existing_project.end_date == date(2024, 8, 31)
        assert "microservices architecture" in existing_project.description
        assert "cloud deployment" in existing_project.description