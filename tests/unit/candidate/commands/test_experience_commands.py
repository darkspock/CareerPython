"""
Unit tests for Experience commands
"""
import pytest
from datetime import date, timedelta
from unittest.mock import Mock

from src.candidate.application.commands.create_experience import CreateExperienceCommand, CreateExperienceCommandHandler
from src.candidate.application.commands.update_experience import UpdateExperienceCommand, UpdateExperienceCommandHandler
from src.candidate.domain.entities.candidate_experience import CandidateExperience
from src.candidate.domain.exceptions.candidate_exceptions import ExperienceNotFoundError
from src.candidate.domain.repositories.candiadate_experience_repository_interface import CandidateExperienceRepositoryInterface
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from tests.unit.candidate.mothers.experience_mother import ExperienceMother


class TestCreateExperienceCommand:
    """Test cases for CreateExperienceCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.experience_repository = Mock(spec=CandidateExperienceRepositoryInterface)
        self.handler = CreateExperienceCommandHandler(self.experience_repository)

    def test_create_experience_success(self):
        """Test successful experience creation"""
        # Arrange
        command = ExperienceMother.create_experience_command()

        # Act
        self.handler.execute(command)

        # Assert
        self.experience_repository.create.assert_called_once()
        created_experience = self.experience_repository.create.call_args[0][0]

        assert isinstance(created_experience, CandidateExperience)
        assert created_experience.id == command.id
        assert created_experience.candidate_id == command.candidate_id
        assert created_experience.job_title == command.job_title
        assert created_experience.company == command.company
        assert created_experience.description == command.description
        assert created_experience.start_date == command.start_date
        assert created_experience.end_date == command.end_date

    def test_create_experience_with_current_position(self):
        """Test creating experience for current position (no end date)"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        candidate_id = CandidateId.generate()
        start_date = date(2023, 1, 1)

        command = CreateExperienceCommand(
            id=experience_id,
            candidate_id=candidate_id,
            job_title="Senior Software Engineer",
            company="TechCorp Inc.",
            description="Leading development of microservices architecture",
            start_date=start_date,
            end_date=None  # Current position
        )

        # Act
        self.handler.execute(command)

        # Assert
        self.experience_repository.create.assert_called_once()
        created_experience = self.experience_repository.create.call_args[0][0]

        assert created_experience.job_title == "Senior Software Engineer"
        assert created_experience.company == "TechCorp Inc."
        assert created_experience.start_date == start_date
        assert created_experience.end_date is None

    def test_create_experience_with_past_position(self):
        """Test creating experience for past position (with end date)"""
        # Arrange
        start_date = date(2020, 6, 1)
        end_date = date(2022, 12, 31)

        command = ExperienceMother.create_experience_command(
            job_title="Software Developer",
            company="StartupXYZ",
            start_date=start_date,
            end_date=end_date,
            description="Full-stack development using React and Node.js"
        )

        # Act
        self.handler.execute(command)

        # Assert
        self.experience_repository.create.assert_called_once()
        created_experience = self.experience_repository.create.call_args[0][0]

        assert created_experience.job_title == "Software Developer"
        assert created_experience.company == "StartupXYZ"
        assert created_experience.start_date == start_date
        assert created_experience.end_date == end_date
        assert "Full-stack development" in created_experience.description

    def test_create_experience_invalid_date_range(self):
        """Test creating experience with invalid date range (end before start)"""
        # Arrange
        command = ExperienceMother.create_invalid_date_command()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.handler.execute(command)

        assert "End date cannot be before start date" in str(exc_info.value)
        self.experience_repository.create.assert_not_called()

    def test_create_experience_with_long_description(self):
        """Test creating experience with detailed description"""
        # Arrange
        long_description = """
        • Led a team of 5 developers in designing and implementing a microservices architecture
        • Improved system performance by 40% through database optimization and caching strategies
        • Implemented CI/CD pipelines using Jenkins and Docker, reducing deployment time by 60%
        • Mentored junior developers and conducted code reviews to maintain high code quality standards
        • Collaborated with product managers and designers to deliver features on time and within budget
        """

        command = ExperienceMother.create_experience_command(
            job_title="Technical Lead",
            company="Enterprise Solutions Ltd",
            description=long_description.strip()
        )

        # Act
        self.handler.execute(command)

        # Assert
        self.experience_repository.create.assert_called_once()
        created_experience = self.experience_repository.create.call_args[0][0]

        assert created_experience.job_title == "Technical Lead"
        assert "Led a team of 5 developers" in created_experience.description
        assert "40% through database optimization" in created_experience.description


class TestUpdateExperienceCommand:
    """Test cases for UpdateExperienceCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.experience_repository = Mock(spec=CandidateExperienceRepositoryInterface)
        self.handler = UpdateExperienceCommandHandler(self.experience_repository)

    def test_update_experience_success(self):
        """Test successful experience update"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        existing_experience = ExperienceMother.create_experience_entity(experience_id=experience_id)
        self.experience_repository.get_by_id.return_value = existing_experience

        command = ExperienceMother.create_update_experience_command(experience_id)

        # Act
        self.handler.execute(command)

        # Assert
        self.experience_repository.get_by_id.assert_called_once_with(experience_id)
        self.experience_repository.update.assert_called_once()

        # Verify update data
        update_call = self.experience_repository.update.call_args
        updated_id = update_call[0][0]
        update_data = update_call[0][1]

        assert updated_id == experience_id
        assert update_data['job_title'] == command.job_title
        assert update_data['company'] == command.company
        assert update_data['description'] == command.description
        assert update_data['start_date'] == command.start_date
        assert update_data['end_date'] == command.end_date
        assert 'updated_at' in update_data

    def test_update_experience_not_found(self):
        """Test update command when experience doesn't exist"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        self.experience_repository.get_by_id.return_value = None

        command = ExperienceMother.create_update_experience_command(experience_id)

        # Act & Assert
        with pytest.raises(ExperienceNotFoundError) as exc_info:
            self.handler.execute(command)

        assert f"Experience with id {experience_id.value} not found" in str(exc_info.value)
        self.experience_repository.get_by_id.assert_called_once_with(experience_id)
        self.experience_repository.update.assert_not_called()

    def test_update_experience_change_to_current_position(self):
        """Test updating experience to remove end date (making it current position)"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        existing_experience = ExperienceMother.create_experience_entity(
            experience_id=experience_id,
            job_title="Junior Developer",
            end_date=date(2023, 6, 30)  # Had an end date
        )
        self.experience_repository.get_by_id.return_value = existing_experience

        command = UpdateExperienceCommand(
            id=experience_id,
            job_title="Senior Developer",  # Promoted
            company=existing_experience.company,
            description="Promoted to senior role with increased responsibilities",
            start_date=existing_experience.start_date,
            end_date=None  # Current position now
        )

        # Act
        self.handler.execute(command)

        # Assert
        update_call = self.experience_repository.update.call_args
        update_data = update_call[0][1]

        assert update_data['job_title'] == "Senior Developer"
        assert update_data['end_date'] is None
        assert "Promoted to senior role" in update_data['description']

    def test_update_experience_change_from_current_to_past(self):
        """Test updating current experience to add end date (no longer current)"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        existing_experience = ExperienceMother.create_current_experience_entity(experience_id=experience_id)
        self.experience_repository.get_by_id.return_value = existing_experience

        end_date = date(2024, 3, 15)
        command = UpdateExperienceCommand(
            id=experience_id,
            job_title=existing_experience.job_title,
            company=existing_experience.company,
            description="Completed tenure at company, moving to new opportunities",
            start_date=existing_experience.start_date,
            end_date=end_date  # Adding end date
        )

        # Act
        self.handler.execute(command)

        # Assert
        update_call = self.experience_repository.update.call_args
        update_data = update_call[0][1]

        assert update_data['end_date'] == end_date
        assert "Completed tenure" in update_data['description']

    def test_update_experience_partial_changes(self):
        """Test updating only some fields of experience"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        original_company = "Original Company"
        original_job_title = "Original Title"
        original_start_date = date(2022, 1, 1)
        original_end_date = date(2023, 12, 31)

        existing_experience = ExperienceMother.create_experience_entity(
            experience_id=experience_id,
            job_title=original_job_title,
            company=original_company,
            start_date=original_start_date,
            end_date=original_end_date
        )
        self.experience_repository.get_by_id.return_value = existing_experience

        # Update only job title and description
        command = UpdateExperienceCommand(
            id=experience_id,
            job_title="Updated Title",  # Changed
            company=original_company,   # Same
            description="Updated description with more details",  # Changed
            start_date=original_start_date,  # Same
            end_date=original_end_date       # Same
        )

        # Act
        self.handler.execute(command)

        # Assert
        update_call = self.experience_repository.update.call_args
        update_data = update_call[0][1]

        assert update_data['job_title'] == "Updated Title"
        assert update_data['company'] == original_company
        assert update_data['description'] == "Updated description with more details"
        assert update_data['start_date'] == original_start_date
        assert update_data['end_date'] == original_end_date

    def test_update_experience_with_extended_date_range(self):
        """Test updating experience with extended date range"""
        # Arrange
        experience_id = CandidateExperienceId.generate()
        original_start_date = date(2023, 6, 1)
        original_end_date = date(2023, 12, 31)

        existing_experience = ExperienceMother.create_experience_entity(
            experience_id=experience_id,
            start_date=original_start_date,
            end_date=original_end_date
        )
        self.experience_repository.get_by_id.return_value = existing_experience

        # Extend the experience period
        new_start_date = date(2023, 3, 1)  # Earlier start
        new_end_date = date(2024, 6, 30)   # Later end

        command = UpdateExperienceCommand(
            id=experience_id,
            job_title=existing_experience.job_title,
            company=existing_experience.company,
            description="Extended tenure due to project requirements",
            start_date=new_start_date,
            end_date=new_end_date
        )

        # Act
        self.handler.execute(command)

        # Assert
        update_call = self.experience_repository.update.call_args
        update_data = update_call[0][1]

        assert update_data['start_date'] == new_start_date
        assert update_data['end_date'] == new_end_date
        assert "Extended tenure" in update_data['description']