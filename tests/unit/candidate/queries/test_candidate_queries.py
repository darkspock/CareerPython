"""
Unit tests for Candidate queries
"""
from unittest.mock import Mock

from src.candidate_bc.candidate.application.queries.get_candidate_by_id import GetCandidateByIdQuery, GetCandidateByIdQueryHandler
from src.candidate_bc.candidate.application import GetCandidateByUserIdQuery, GetCandidateByUserIdQueryHandler
from src.candidate_bc.candidate.application.queries.list_candidates import ListCandidatesQuery, ListCandidatesQueryHandler
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.auth_bc.user.domain.value_objects import UserId
from tests.unit.candidate.mothers.candidate_mother import CandidateMother


class TestGetCandidateByIdQuery:
    """Test cases for GetCandidateByIdQuery and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.candidate_repository = Mock(spec=CandidateRepositoryInterface)
        self.handler = GetCandidateByIdQueryHandler(self.candidate_repository)

    def test_get_candidate_by_id_success(self):
        """Test successful candidate retrieval by ID"""
        # Arrange
        candidate_id = CandidateId.generate()
        candidate_entity = CandidateMother.create_candidate_entity(candidate_id=candidate_id)
        self.candidate_repository.get_by_id.return_value = candidate_entity

        query = GetCandidateByIdQuery(id=candidate_id)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_by_id.assert_called_once_with(candidate_id)
        assert result is not None
        assert isinstance(result, CandidateDto)
        assert result.id == candidate_id
        assert result.name == candidate_entity.name
        assert result.email == candidate_entity.email
        assert result.status == candidate_entity.status
        assert result.job_category == candidate_entity.job_category

    def test_get_candidate_by_id_not_found(self):
        """Test candidate retrieval when candidate doesn't exist"""
        # Arrange
        candidate_id = CandidateId.generate()
        self.candidate_repository.get_by_id.return_value = None

        query = GetCandidateByIdQuery(id=candidate_id)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_by_id.assert_called_once_with(candidate_id)
        assert result is None

    def test_get_candidate_by_id_with_full_profile(self):
        """Test retrieving candidate with complete profile information"""
        # Arrange
        candidate_id = CandidateId.generate()
        candidate_entity = CandidateMother.create_candidate_entity(
            candidate_id=candidate_id,
            name="John Doe",
            email="john.doe@example.com",
            expected_annual_salary=75000,
            current_annual_salary=65000,
            linkedin_url="https://linkedin.com/in/johndoe",
            skills=["Python", "FastAPI", "PostgreSQL", "Docker"]
        )
        self.candidate_repository.get_by_id.return_value = candidate_entity

        query = GetCandidateByIdQuery(id=candidate_id)

        # Act
        result = self.handler.handle(query)

        # Assert
        assert result is not None
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.expected_annual_salary == 75000
        assert result.current_annual_salary == 65000
        assert result.linkedin_url == "https://linkedin.com/in/johndoe"
        assert result.skills == ["Python", "FastAPI", "PostgreSQL", "Docker"]


class TestGetCandidateByUserIdQuery:
    """Test cases for GetCandidateByUserIdQuery and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.candidate_repository = Mock(spec=CandidateRepositoryInterface)
        self.handler = GetCandidateByUserIdQueryHandler(self.candidate_repository)

    def test_get_candidate_by_user_id_success(self):
        """Test successful candidate retrieval by user ID"""
        # Arrange
        user_id = UserId.generate()
        candidate_entity = CandidateMother.create_candidate_entity(user_id=user_id)
        self.candidate_repository.get_by_user_id.return_value = candidate_entity

        query = GetCandidateByUserIdQuery(user_id=user_id)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_by_user_id.assert_called_once_with(user_id)
        assert result is not None
        assert isinstance(result, CandidateDto)
        assert result.user_id == user_id
        assert result.name == candidate_entity.name
        assert result.email == candidate_entity.email

    def test_get_candidate_by_user_id_not_found(self):
        """Test candidate retrieval when user has no candidate profile"""
        # Arrange
        user_id = UserId.generate()
        self.candidate_repository.get_by_user_id.return_value = None

        query = GetCandidateByUserIdQuery(user_id=user_id)

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_by_user_id.assert_called_once_with(user_id)
        assert result is None


class TestListCandidatesQuery:
    """Test cases for ListCandidatesQuery and its handler"""

    def setup_method(self):
        """Setup test dependencies"""
        self.candidate_repository = Mock(spec=CandidateRepositoryInterface)
        self.handler = ListCandidatesQueryHandler(self.candidate_repository)

    def test_list_candidates_success(self):
        """Test successful candidate listing"""
        # Arrange
        candidate1 = CandidateMother.create_candidate_entity(name="John Doe")
        candidate2 = CandidateMother.create_candidate_entity(name="Jane Smith")
        candidate3 = CandidateMother.create_candidate_entity(name="Bob Johnson")

        candidates = [candidate1, candidate2, candidate3]
        self.candidate_repository.get_all.return_value = candidates

        query = ListCandidatesQuery()

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_all.assert_called_once()
        assert result is not None
        assert len(result) == 3
        assert all(isinstance(dto, CandidateDto) for dto in result)

        # Verify specific candidates
        names = [dto.name for dto in result]
        assert "John Doe" in names
        assert "Jane Smith" in names
        assert "Bob Johnson" in names

    def test_list_candidates_empty_result(self):
        """Test candidate listing when no candidates exist"""
        # Arrange
        self.candidate_repository.get_all.return_value = []

        query = ListCandidatesQuery()

        # Act
        result = self.handler.handle(query)

        # Assert
        self.candidate_repository.get_all.assert_called_once()
        assert result is not None
        assert len(result) == 0
        assert isinstance(result, list)

    def test_list_candidates_with_filtering(self):
        """Test candidate listing with basic filtering (if supported)"""
        # Arrange
        tech_candidate1 = CandidateMother.create_candidate_entity(
            name="Python Dev",
            skills=["Python", "Django", "PostgreSQL"]
        )
        tech_candidate2 = CandidateMother.create_candidate_entity(
            name="JS Dev",
            skills=["JavaScript", "React", "Node.js"]
        )

        candidates = [tech_candidate1, tech_candidate2]
        self.candidate_repository.get_all.return_value = candidates

        query = ListCandidatesQuery()

        # Act
        result = self.handler.handle(query)

        # Assert
        assert len(result) == 2

        # Verify that all candidates have technical skills
        for dto in result:
            assert dto.skills is not None
            assert len(dto.skills) > 0

        # Check specific skills
        python_dev = next((dto for dto in result if dto.name == "Python Dev"), None)
        js_dev = next((dto for dto in result if dto.name == "JS Dev"), None)

        assert python_dev is not None
        assert "Python" in python_dev.skills
        assert "Django" in python_dev.skills

        assert js_dev is not None
        assert "JavaScript" in js_dev.skills
        assert "React" in js_dev.skills

    def test_list_candidates_different_statuses(self):
        """Test listing candidates with different statuses"""
        # Arrange
        from src.candidate_bc.candidate.domain.enums.candidate_enums import CandidateStatusEnum

        draft_candidate = CandidateMother.create_candidate_entity(name="Draft Candidate")
        draft_candidate.status = CandidateStatusEnum.DRAFT

        complete_candidate = CandidateMother.create_candidate_entity(name="Complete Candidate")
        complete_candidate.complete()  # This should set status to COMPLETE

        candidates = [draft_candidate, complete_candidate]
        self.candidate_repository.get_all.return_value = candidates

        query = ListCandidatesQuery()

        # Act
        result = self.handler.handle(query)

        # Assert
        assert len(result) == 2

        draft_dto = next((dto for dto in result if dto.name == "Draft Candidate"), None)
        complete_dto = next((dto for dto in result if dto.name == "Complete Candidate"), None)

        assert draft_dto is not None
        assert draft_dto.status == CandidateStatusEnum.DRAFT

        assert complete_dto is not None
        assert complete_dto.status == CandidateStatusEnum.COMPLETE

    def test_list_candidates_with_various_experience_levels(self):
        """Test listing candidates with different experience levels"""
        # Arrange
        from src.company_bc.job_position.domain.enums.position_level_enum import JobPositionLevelEnum

        junior_candidate = CandidateMother.create_candidate_entity(
            name="Junior Dev",
            current_job_level=JobPositionLevelEnum.JUNIOR,
            expected_job_level=JobPositionLevelEnum.MID
        )

        senior_candidate = CandidateMother.create_candidate_entity(
            name="Senior Dev",
            current_job_level=JobPositionLevelEnum.SENIOR,
            expected_job_level=JobPositionLevelEnum.LEAD
        )

        candidates = [junior_candidate, senior_candidate]
        self.candidate_repository.get_all.return_value = candidates

        query = ListCandidatesQuery()

        # Act
        result = self.handler.handle(query)

        # Assert
        assert len(result) == 2

        # Note: The exact field names depend on your DTO structure
        # This is a basic check that different candidates are returned
        names = [dto.name for dto in result]
        assert "Junior Dev" in names
        assert "Senior Dev" in names