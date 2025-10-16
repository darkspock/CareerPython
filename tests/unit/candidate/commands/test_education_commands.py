"""
Unit tests for Education commands
"""
import pytest
from datetime import date
from unittest.mock import Mock

from src.candidate.application.commands.create_education import CreateEducationCommand, CreateEducationCommandHandler
from src.candidate.application.commands.update_education import UpdateEducationCommand, UpdateEducationCommandHandler
from src.candidate.domain.entities.candidate_education import CandidateEducation
from src.candidate.domain.exceptions.candidate_exceptions import EducationNotFoundError
from src.candidate.domain.repositories.candidate_education_repository_interface import CandidateEducationRepositoryInterface
from src.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from tests.unit.candidate.mothers.education_mother import EducationMother


class TestCreateEducationCommand:
    """Test cases for CreateEducationCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.education_repository = Mock(spec=CandidateEducationRepositoryInterface)
        self.handler = CreateEducationCommandHandler(self.education_repository)

    def test_create_education_success(self):
        """Test successful education creation"""
        # Arrange
        command = EducationMother.create_education_command()

        # Act
        self.handler.execute(command)

        # Assert
        self.education_repository.create.assert_called_once()
        created_education = self.education_repository.create.call_args[0][0]

        assert isinstance(created_education, CandidateEducation)
        assert created_education.id == command.id
        assert created_education.candidate_id == command.candidate_id
        assert created_education.degree == command.degree
        assert created_education.institution == command.institution
        assert created_education.description == command.description
        assert created_education.start_date == command.start_date
        assert created_education.end_date == command.end_date

    def test_create_education_bachelors_degree(self):
        """Test creating bachelor's degree education"""
        # Arrange
        command = EducationMother.create_education_command(
            degree="Bachelor's in Computer Science",
            institution="University of Technology",
            start_date=date(2018, 9, 1),
            end_date=date(2022, 6, 30),
            description="Coursework in algorithms, data structures, software engineering, and database systems"
        )

        # Act
        self.handler.execute(command)

        # Assert
        created_education = self.education_repository.create.call_args[0][0]
        assert created_education.degree == "Bachelor's in Computer Science"
        assert created_education.institution == "University of Technology"
        assert "algorithms" in created_education.description

    def test_create_education_ongoing(self):
        """Test creating ongoing education (no end date)"""
        # Arrange
        command = EducationMother.create_education_command(
            degree="Master's in Data Science",
            institution="Graduate School",
            start_date=date(2023, 9, 1),
            end_date=None  # Ongoing
        )

        # Act
        self.handler.execute(command)

        # Assert
        created_education = self.education_repository.create.call_args[0][0]
        assert created_education.degree == "Master's in Data Science"
        assert created_education.end_date is None


class TestUpdateEducationCommand:
    """Test cases for UpdateEducationCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.education_repository = Mock(spec=CandidateEducationRepositoryInterface)
        self.handler = UpdateEducationCommandHandler(self.education_repository)

    def test_update_education_success(self):
        """Test successful education update"""
        # Arrange
        education_id = CandidateEducationId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08")
        existing_education = EducationMother.create_education_entity(education_id=education_id)
        self.education_repository.get_by_id.return_value = existing_education

        command = EducationMother.create_update_education_command(education_id)

        # Act
        self.handler.execute(command)

        # Assert
        self.education_repository.get_by_id.assert_called_once_with(education_id)
        self.education_repository.update.assert_called_once_with(education_id, existing_education)

        # Verify education was updated
        assert existing_education.degree == command.degree
        assert existing_education.institution == command.institution
        assert existing_education.description == command.description
        assert existing_education.start_date == command.start_date
        assert existing_education.end_date == command.end_date

    def test_update_education_not_found(self):
        """Test update command when education doesn't exist"""
        # Arrange
        education_id = CandidateEducationId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08")
        self.education_repository.get_by_id.return_value = None

        command = EducationMother.create_update_education_command(education_id)

        # Act & Assert
        with pytest.raises(EducationNotFoundError):
            self.handler.execute(command)

        self.education_repository.get_by_id.assert_called_once_with(education_id)
        self.education_repository.update.assert_not_called()

    def test_update_education_from_ongoing_to_completed(self):
        """Test updating ongoing education to completed (adding end date)"""
        # Arrange
        education_id = CandidateEducationId.from_string("01HQ7K8NZFT7QK3SR3VEF05S08")
        existing_education = EducationMother.create_ongoing_education_entity(education_id=education_id)
        self.education_repository.get_by_id.return_value = existing_education

        command = UpdateEducationCommand(
            id=education_id,
            degree=existing_education.degree,
            institution=existing_education.institution,
            description="Completed with honors",
            start_date=existing_education.start_date,
            end_date=date(2024, 5, 15)  # Now completed
        )

        # Act
        self.handler.execute(command)

        # Assert
        assert existing_education.end_date == date(2024, 5, 15)
        assert existing_education.description == "Completed with honors"