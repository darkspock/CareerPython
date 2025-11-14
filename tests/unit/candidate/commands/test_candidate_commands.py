"""
Unit tests for Candidate commands
"""
import pytest
from datetime import date
from unittest.mock import Mock

from core.event_bus import EventBus
from src.candidate_bc.candidate.application.commands.create_candidate import CreateCandidateCommand, CreateCandidateCommandHandler
from src.candidate_bc.candidate.application.commands.update_candidate import UpdateCandidateCommand, UpdateCandidateCommandHandler
from src.candidate_bc.candidate.domain.entities.candidate import Candidate
from src.candidate_bc.candidate.domain.enums.candidate_enums import CandidateStatusEnum, CandidateTypeEnum, WorkModalityEnum, LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.candidate_bc.candidate.domain.events.candidate_created_event import CandidateCreatedEvent
from src.candidate_bc.candidate.domain.exceptions.candidate_exceptions import CandidateNotFoundException
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.auth_bc.user.domain.value_objects import UserId
from tests.unit.candidate.mothers.candidate_mother import CandidateMother


class TestCreateCandidateCommand:
    """Test cases for CreateCandidateCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.candidate_repository = Mock(spec=CandidateRepositoryInterface)
        self.event_bus = Mock(spec=EventBus)
        self.handler = CreateCandidateCommandHandler(self.candidate_repository, self.event_bus)

    def test_create_candidate_command_success(self):
        """Test successful candidate creation"""
        # Arrange
        command = CandidateMother.create_candidate_command()

        # Act
        self.handler.execute(command)

        # Assert
        self.candidate_repository.create.assert_called_once()
        created_candidate = self.candidate_repository.create.call_args[0][0]

        assert isinstance(created_candidate, Candidate)
        assert created_candidate.id == command.id
        assert created_candidate.name == command.name
        assert created_candidate.email == command.email
        assert created_candidate.user_id == command.user_id
        assert created_candidate.status == CandidateStatusEnum.DRAFT

        # Verify event was dispatched
        self.event_bus.dispatch.assert_called_once()
        event = self.event_bus.dispatch.call_args[0][0]
        assert isinstance(event, CandidateCreatedEvent)

    def test_create_candidate_with_minimal_data(self):
        """Test candidate creation with only required fields"""
        # Arrange
        candidate_id = CandidateId.generate()
        user_id = UserId.generate()

        command = CreateCandidateCommand(
            id=candidate_id,
            name="John Doe",
            date_of_birth=date(1990, 1, 1),
            city="Madrid",
            country="Spain",
            phone="+34123456789",
            email="john.doe@example.com",
            user_id=user_id
        )

        # Act
        self.handler.execute(command)

        # Assert
        self.candidate_repository.create.assert_called_once()
        created_candidate = self.candidate_repository.create.call_args[0][0]

        assert created_candidate.id == candidate_id
        assert created_candidate.name == "John Doe"
        assert created_candidate.email == "john.doe@example.com"
        assert created_candidate.user_id == user_id
        assert created_candidate.job_category == JobCategoryEnum.OTHER  # Default value
        assert created_candidate.candidate_type == CandidateTypeEnum.BASIC  # Default value

    def test_create_candidate_with_full_data(self):
        """Test candidate creation with all optional fields"""
        # Arrange
        command = CandidateMother.create_candidate_command(
            job_category=JobCategoryEnum.TECHNOLOGY,
            candidate_type=CandidateTypeEnum.PREMIUM,
            expected_annual_salary=75000,
            current_annual_salary=60000,
            currency='USD',
            relocation=True,
            work_modality=[WorkModalityEnum.REMOTE, WorkModalityEnum.HYBRID],
            languages={
                LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL,
                LanguageEnum.SPANISH: LanguageLevelEnum.PROFESSIONAL,
                LanguageEnum.FRENCH: LanguageLevelEnum.CONVERSATIONAL
            },
            other_languages='Portuguese (Beginner)',
            linkedin_url='https://linkedin.com/in/johndoe',
            data_consent=True,
            data_consent_on=date.today(),
            current_roles=[PositionRoleEnum.TECHNOLOGY],
            expected_roles=[PositionRoleEnum.LEAD_INITIATIVES, PositionRoleEnum.EXECUTIVE],
            current_job_level=JobPositionLevelEnum.MID,
            expected_job_level=JobPositionLevelEnum.SENIOR,
            skills=['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'AWS'],
            timezone='Europe/Madrid',
            candidate_notes='Experienced developer with leadership aspirations'
        )

        # Act
        self.handler.execute(command)

        # Assert
        self.candidate_repository.create.assert_called_once()
        created_candidate = self.candidate_repository.create.call_args[0][0]

        assert created_candidate.job_category == JobCategoryEnum.TECHNOLOGY
        assert created_candidate.candidate_type == CandidateTypeEnum.PREMIUM
        assert created_candidate.expected_annual_salary == 75000
        assert created_candidate.current_annual_salary == 60000
        assert created_candidate.currency == 'USD'
        assert created_candidate.relocation is True
        assert WorkModalityEnum.REMOTE in created_candidate.work_modality
        assert WorkModalityEnum.HYBRID in created_candidate.work_modality
        assert created_candidate.languages[LanguageEnum.ENGLISH] == LanguageLevelEnum.PROFESSIONAL
        assert created_candidate.languages[LanguageEnum.SPANISH] == LanguageLevelEnum.PROFESSIONAL
        assert created_candidate.other_languages == 'Portuguese (Beginner)'
        assert created_candidate.linkedin_url == 'https://linkedin.com/in/johndoe'
        assert created_candidate.data_consent is True
        assert PositionRoleEnum.TECHNOLOGY in created_candidate.current_roles
        assert PositionRoleEnum.LEAD_INITIATIVES in created_candidate.expected_roles
        assert PositionRoleEnum.EXECUTIVE in created_candidate.expected_roles
        assert created_candidate.current_job_level == JobPositionLevelEnum.MID
        assert created_candidate.expected_job_level == JobPositionLevelEnum.SENIOR
        assert 'Python' in created_candidate.skills
        assert 'FastAPI' in created_candidate.skills
        assert created_candidate.timezone == 'Europe/Madrid'
        assert created_candidate.candidate_notes == 'Experienced developer with leadership aspirations'


class TestUpdateCandidateCommand:
    """Test cases for UpdateCandidateCommand and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.candidate_repository = Mock(spec=CandidateRepositoryInterface)
        self.handler = UpdateCandidateCommandHandler(self.candidate_repository)

    def test_update_candidate_command_success(self):
        """Test successful candidate update"""
        # Arrange
        candidate_id = CandidateId.generate()
        existing_candidate = CandidateMother.create_candidate_entity(candidate_id=candidate_id)
        self.candidate_repository.get_by_id.return_value = existing_candidate

        command = CandidateMother.create_update_candidate_command(candidate_id)

        # Act
        self.handler.execute(command)

        # Assert
        self.candidate_repository.get_by_id.assert_called_once_with(candidate_id)
        self.candidate_repository.update.assert_called_once_with(existing_candidate)

        # Verify candidate was updated
        assert existing_candidate.name == command.name
        assert existing_candidate.email == command.email
        assert existing_candidate.city == command.city
        assert existing_candidate.country == command.country
        assert existing_candidate.phone == command.phone
        assert existing_candidate.job_category == command.job_category

    def test_update_candidate_not_found(self):
        """Test update command when candidate doesn't exist"""
        # Arrange
        candidate_id = CandidateId.generate()
        self.candidate_repository.get_by_id.return_value = None

        command = CandidateMother.create_update_candidate_command(candidate_id)

        # Act & Assert
        with pytest.raises(CandidateNotFoundException) as exc_info:
            self.handler.execute(command)

        assert f"Candidate with id {candidate_id} not found" in str(exc_info.value)
        self.candidate_repository.get_by_id.assert_called_once_with(candidate_id)
        self.candidate_repository.update.assert_not_called()

    def test_update_candidate_partial_data(self):
        """Test candidate update with partial data changes"""
        # Arrange
        candidate_id = CandidateId.generate()
        existing_candidate = CandidateMother.create_candidate_entity(
            candidate_id=candidate_id,
            name="Original Name",
            email="original@example.com",
            current_annual_salary=50000,
            expected_annual_salary=60000
        )
        self.candidate_repository.get_by_id.return_value = existing_candidate

        # Update command with different values
        command = UpdateCandidateCommand(
            id=candidate_id,
            name="Updated Name",
            date_of_birth=existing_candidate.date_of_birth,
            city=existing_candidate.city,
            country=existing_candidate.country,
            phone=existing_candidate.phone,
            email="updated@example.com",
            job_category=existing_candidate.job_category,
            candidate_type=existing_candidate.candidate_type,
            expected_annual_salary=70000,  # Changed
            currency='USD',  # Changed
            relocation=False,  # Changed
            work_modality=[WorkModalityEnum.ON_SITE],  # Changed
            languages={LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL},  # Changed
            other_languages=None,
            current_annual_salary=55000,  # Changed
            linkedin_url=existing_candidate.linkedin_url,
            current_roles=[PositionRoleEnum.TECHNOLOGY],  # Changed
            expected_roles=[PositionRoleEnum.LEAD_INITIATIVES],  # Changed
            skills=['React', 'Node.js', 'MongoDB'],  # Changed
            current_job_level=JobPositionLevelEnum.SENIOR,  # Changed
            expected_job_level=JobPositionLevelEnum.LEAD,  # Changed
            timezone='America/New_York',  # Changed
            candidate_notes='Updated notes'  # Changed
        )

        # Act
        self.handler.execute(command)

        # Assert
        assert existing_candidate.name == "Updated Name"
        assert existing_candidate.email == "updated@example.com"
        assert existing_candidate.expected_annual_salary == 70000
        assert existing_candidate.current_annual_salary == 55000
        assert existing_candidate.currency == 'USD'
        assert existing_candidate.relocation is False
        assert existing_candidate.work_modality == [WorkModalityEnum.ON_SITE]
        assert existing_candidate.languages == {LanguageEnum.ENGLISH: LanguageLevelEnum.PROFESSIONAL}
        assert existing_candidate.current_roles == [PositionRoleEnum.TECHNOLOGY]
        assert existing_candidate.expected_roles == [PositionRoleEnum.LEAD_INITIATIVES]
        assert existing_candidate.skills == ['React', 'Node.js', 'MongoDB']
        assert existing_candidate.current_job_level == JobPositionLevelEnum.SENIOR
        assert existing_candidate.expected_job_level == JobPositionLevelEnum.LEAD
        assert existing_candidate.timezone == 'America/New_York'
        assert existing_candidate.candidate_notes == 'Updated notes'

        self.candidate_repository.update.assert_called_once_with(existing_candidate)

    def test_update_candidate_with_empty_lists(self):
        """Test candidate update with empty lists for optional fields"""
        # Arrange
        candidate_id = CandidateId.generate()
        existing_candidate = CandidateMother.create_candidate_entity(
            candidate_id=candidate_id,
            work_modality=[WorkModalityEnum.REMOTE, WorkModalityEnum.HYBRID],
            current_roles=[PositionRoleEnum.TECHNOLOGY],
            expected_roles=[PositionRoleEnum.LEAD_INITIATIVES],
            skills=['Python', 'FastAPI']
        )
        self.candidate_repository.get_by_id.return_value = existing_candidate

        command = UpdateCandidateCommand(
            id=candidate_id,
            name=existing_candidate.name,
            date_of_birth=existing_candidate.date_of_birth,
            city=existing_candidate.city,
            country=existing_candidate.country,
            phone=existing_candidate.phone,
            email=existing_candidate.email,
            job_category=existing_candidate.job_category,
            candidate_type=existing_candidate.candidate_type,
            expected_annual_salary=existing_candidate.expected_annual_salary,
            currency=existing_candidate.currency,
            relocation=existing_candidate.relocation,
            work_modality=[],  # Empty list
            languages={},  # Empty dict
            other_languages=None,
            current_annual_salary=existing_candidate.current_annual_salary,
            linkedin_url=existing_candidate.linkedin_url,
            current_roles=[],  # Empty list
            expected_roles=[],  # Empty list
            skills=[],  # Empty list
            current_job_level=existing_candidate.current_job_level,
            expected_job_level=existing_candidate.expected_job_level,
            timezone=existing_candidate.timezone,
            candidate_notes=existing_candidate.candidate_notes
        )

        # Act
        self.handler.execute(command)

        # Assert
        assert existing_candidate.work_modality == []
        assert existing_candidate.languages == {}
        assert existing_candidate.current_roles == []
        assert existing_candidate.expected_roles == []
        assert existing_candidate.skills == []

        self.candidate_repository.update.assert_called_once_with(existing_candidate)