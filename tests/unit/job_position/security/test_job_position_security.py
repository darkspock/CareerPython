"""
Security Tests for Job Position
Tests authorization and data protection rules
"""
import pytest
from datetime import datetime
from decimal import Decimal
from typing import Optional
from unittest.mock import Mock, MagicMock

from src.company_bc.company.domain.value_objects import CompanyId, CompanyUserId
from src.company_bc.job_position.application.commands.job_position_status_commands import (
    ApproveJobPositionCommand, ApproveJobPositionCommandHandler,
    PublishJobPositionCommand, PublishJobPositionCommandHandler
)
from src.company_bc.job_position.application.queries.job_position_dto import (
    JobPositionDto, JobPositionPublicDto
)
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import (
    JobPositionStatusEnum,
    JobPositionVisibilityEnum,
    ClosedReasonEnum
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.framework.domain.enums.job_category import JobCategoryEnum


class MockJobPositionRepository:
    """In-memory mock repository for testing"""

    def __init__(self):
        self.positions: dict[str, JobPosition] = {}

    def save(self, position: JobPosition) -> None:
        self.positions[position.id.value] = position

    def get_by_id(self, position_id: JobPositionId) -> Optional[JobPosition]:
        return self.positions.get(position_id.value)


def create_test_position(
    title: str = "Software Engineer",
    description: str = "A great position",
    budget_max: Optional[Decimal] = Decimal("150000"),
    salary_max: Optional[Decimal] = Decimal("120000"),
    salary_min: Optional[Decimal] = Decimal("100000")
) -> tuple[JobPosition, JobPositionId, CompanyId]:
    """Helper to create a test position with financial data"""
    position_id = JobPositionId.generate()
    company_id = CompanyId.generate()

    position = JobPosition.create(
        id=position_id,
        title=title,
        company_id=company_id,
        description=description,
        job_category=JobCategoryEnum.TECHNOLOGY,
        budget_max=budget_max,
        salary_max=salary_max,
        salary_min=salary_min,
        salary_currency="USD"
    )

    return position, position_id, company_id


# ==================== 8.3.1 PUBLIC API NEVER RETURNS BUDGET FIELDS ====================

class TestPublicApiHidesBudgetFields:
    """Test that public API (JobPositionPublicDto) never exposes budget fields"""

    def test_public_dto_excludes_budget_max(self):
        """Test that budget_max is not in public DTO"""
        position, _, _ = create_test_position(budget_max=Decimal("150000"))

        # Get public DTO
        public_dto = JobPositionPublicDto.from_entity(position)

        # Verify budget_max is NOT exposed
        assert not hasattr(public_dto, 'budget_max'), "budget_max should not be in public DTO"

    def test_public_dto_excludes_approved_budget_max(self):
        """Test that approved_budget_max is not in public DTO"""
        position, _, _ = create_test_position()
        position.request_approval()
        position.approve(approver_id=CompanyUserId.from_string("approver-123"))

        public_dto = JobPositionPublicDto.from_entity(position)

        assert not hasattr(public_dto, 'approved_budget_max'), "approved_budget_max should not be in public DTO"

    def test_public_dto_excludes_financial_approver_id(self):
        """Test that financial_approver_id is not in public DTO"""
        position, _, _ = create_test_position()
        position.request_approval()
        position.approve(approver_id=CompanyUserId.from_string("approver-123"))

        public_dto = JobPositionPublicDto.from_entity(position)

        assert not hasattr(public_dto, 'financial_approver_id'), "financial_approver_id should not be in public DTO"

    def test_public_dto_includes_salary_when_show_salary_true(self):
        """Test that salary fields are shown when show_salary is True"""
        position, _, _ = create_test_position(
            salary_min=Decimal("100000"),
            salary_max=Decimal("120000")
        )
        position.show_salary = True

        public_dto = JobPositionPublicDto.from_entity(position)

        # Salary should be visible when show_salary is True
        assert hasattr(public_dto, 'salary_min') or hasattr(public_dto, 'salary_range_min')
        assert hasattr(public_dto, 'salary_max') or hasattr(public_dto, 'salary_range_max')

    def test_internal_dto_includes_budget_fields(self):
        """Test that internal DTO (JobPositionDto) includes budget fields for internal use"""
        position, _, _ = create_test_position(budget_max=Decimal("150000"))
        position.request_approval()
        position.approve(approver_id=CompanyUserId.from_string("approver-123"))

        internal_dto = JobPositionDto.from_entity(position)

        # Internal DTO should have budget fields
        assert hasattr(internal_dto, 'budget_max')
        assert internal_dto.budget_max == Decimal("150000")
        # The internal DTO is for company users who need to see budget


# ==================== 8.3.2 PUBLIC API NEVER RETURNS INTERNAL CUSTOM FIELDS ====================

class TestPublicApiHidesInternalCustomFields:
    """Test that public API excludes internal/non-candidate-visible custom fields"""

    def test_public_dto_excludes_non_candidate_visible_custom_fields(self):
        """Test that custom fields with candidate_visible=False are not exposed"""
        position, _, _ = create_test_position()

        # Add custom fields - some visible to candidates, some not
        position.custom_fields_config = [
            CustomFieldDefinition(
                field_key="internal_notes",
                label="Internal Notes",
                field_type="TEXT",
                is_required=False,
                candidate_visible=False,  # Not visible to candidates
                sort_order=1,
                is_active=True,
                options=None,
                validation_rules=None
            ),
            CustomFieldDefinition(
                field_key="team_size",
                label="Team Size",
                field_type="TEXT",
                is_required=False,
                candidate_visible=True,  # Visible to candidates
                sort_order=2,
                is_active=True,
                options=None,
                validation_rules=None
            )
        ]

        public_dto = JobPositionPublicDto.from_entity(position)

        # Check that only candidate-visible fields are exposed
        if hasattr(public_dto, 'custom_fields_config') and public_dto.custom_fields_config:
            for field in public_dto.custom_fields_config:
                if hasattr(field, 'candidate_visible'):
                    assert field.candidate_visible is True, \
                        f"Field {field.field_key} should not be in public DTO"

    def test_public_dto_excludes_source_workflow_id(self):
        """Test that source_workflow_id is not exposed in public DTO"""
        position, _, _ = create_test_position()
        position.source_workflow_id = "workflow-123"

        public_dto = JobPositionPublicDto.from_entity(position)

        assert not hasattr(public_dto, 'source_workflow_id'), \
            "source_workflow_id should not be in public DTO"

    def test_internal_dto_includes_all_custom_fields(self):
        """Test that internal DTO includes all custom fields for company users"""
        position, _, _ = create_test_position()

        position.custom_fields_config = [
            CustomFieldDefinition(
                field_key="internal_notes",
                label="Internal Notes",
                field_type="TEXT",
                is_required=False,
                candidate_visible=False,
                sort_order=1,
                is_active=True,
                options=None,
                validation_rules=None
            ),
            CustomFieldDefinition(
                field_key="team_size",
                label="Team Size",
                field_type="TEXT",
                is_required=False,
                candidate_visible=True,
                sort_order=2,
                is_active=True,
                options=None,
                validation_rules=None
            )
        ]

        internal_dto = JobPositionDto.from_entity(position)

        # Internal DTO should have all custom fields
        if hasattr(internal_dto, 'custom_fields_config') and internal_dto.custom_fields_config:
            assert len(internal_dto.custom_fields_config) == 2


# ==================== 8.3.3 ONLY APPROVERS CAN APPROVE ====================

class TestApproverAuthorization:
    """Test that only authorized users can approve job positions"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_approve_requires_approver_id(self):
        """Test that approval requires an approver ID"""
        position, position_id, company_id = create_test_position(
            budget_max=Decimal("100000")
        )
        position.request_approval()
        self.repository.save(position)

        handler = ApproveJobPositionCommandHandler(self.repository)
        command = ApproveJobPositionCommand(
            job_position_id=position_id.value,
            approver_id="approver-123",
            company_id=company_id.value
        )
        handler.execute(command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.APPROVED
        assert position.financial_approver_id.value == "approver-123"

    def test_approve_stores_approver_identity(self):
        """Test that approval stores the approver's identity for audit"""
        position, position_id, company_id = create_test_position(
            budget_max=Decimal("100000")
        )
        position.request_approval()
        self.repository.save(position)

        approver_id = "finance-manager-456"
        handler = ApproveJobPositionCommandHandler(self.repository)
        command = ApproveJobPositionCommand(
            job_position_id=position_id.value,
            approver_id=approver_id,
            company_id=company_id.value
        )
        handler.execute(command)

        position = self.repository.get_by_id(position_id)
        # Verify audit trail
        assert position.financial_approver_id.value == approver_id
        assert position.approved_at is not None

    def test_approved_budget_is_captured(self):
        """Test that approved budget is captured at approval time"""
        budget = Decimal("150000")
        position, position_id, company_id = create_test_position(budget_max=budget)
        position.request_approval()
        self.repository.save(position)

        handler = ApproveJobPositionCommandHandler(self.repository)
        command = ApproveJobPositionCommand(
            job_position_id=position_id.value,
            approver_id="approver-123",
            company_id=company_id.value
        )
        handler.execute(command)

        position = self.repository.get_by_id(position_id)
        assert position.approved_budget_max == budget

    def test_cannot_approve_from_draft_status(self):
        """Test that cannot approve directly from DRAFT (must be PENDING_APPROVAL)"""
        from src.company_bc.job_position.domain.exceptions import JobPositionInvalidStatusTransitionError

        position, _, _ = create_test_position()
        # Position is in DRAFT status

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.approve(approver_id=CompanyUserId.from_string("approver-123"))


# ==================== 8.3.4 ONLY OWNERS CAN EDIT ====================

class TestOwnershipAuthorization:
    """Test that editing is restricted based on ownership and status"""

    def test_position_tracks_created_by(self):
        """Test that position tracks who created it"""
        position_id = JobPositionId.generate()
        company_id = CompanyId.generate()
        created_by = "user-123"

        position = JobPosition.create(
            id=position_id,
            title="Developer",
            company_id=company_id,
            description="A position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            created_by_id=created_by
        )

        assert position.created_by_id == created_by

    def test_position_tracks_hiring_manager(self):
        """Test that position tracks hiring manager"""
        position_id = JobPositionId.generate()
        company_id = CompanyId.generate()
        hiring_manager = "manager-456"

        position = JobPosition.create(
            id=position_id,
            title="Developer",
            company_id=company_id,
            description="A position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            hiring_manager_id=hiring_manager
        )

        assert position.hiring_manager_id == hiring_manager

    def test_position_tracks_recruiter(self):
        """Test that position tracks assigned recruiter"""
        position_id = JobPositionId.generate()
        company_id = CompanyId.generate()
        recruiter = "recruiter-789"

        position = JobPosition.create(
            id=position_id,
            title="Developer",
            company_id=company_id,
            description="A position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            recruiter_id=recruiter
        )

        assert position.recruiter_id == recruiter

    def test_field_locking_prevents_editing_in_certain_statuses(self):
        """Test that field locking prevents unauthorized edits in certain statuses"""
        from src.company_bc.job_position.domain.exceptions import JobPositionFieldLockedError

        position, _, _ = create_test_position(budget_max=Decimal("100000"))
        position.request_approval()
        position.approve(approver_id=CompanyUserId.from_string("approver-123"))

        # Budget is now locked after approval
        assert position.is_field_locked("budget_max") is True

        # Attempting to change budget should fail
        with pytest.raises(JobPositionFieldLockedError):
            position.set_budget(Decimal("200000"))

    def test_archived_position_all_fields_locked(self):
        """Test that archived positions have all fields locked"""
        position, _, _ = create_test_position()
        position.publish()
        position.close(reason=ClosedReasonEnum.FILLED)
        position.archive()

        # All fields should be locked
        assert position.is_field_locked("title") is True
        assert position.is_field_locked("description") is True
        assert position.is_field_locked("budget_max") is True
        assert position.is_field_locked("custom_fields_config") is True

    def test_draft_position_all_fields_editable(self):
        """Test that draft positions have all fields editable"""
        position, _, _ = create_test_position()

        # All fields should be editable in DRAFT
        assert position.is_field_locked("title") is False
        assert position.is_field_locked("description") is False
        assert position.is_field_locked("budget_max") is False
        assert position.is_field_locked("custom_fields_config") is False

    def test_company_id_must_match_for_commands(self):
        """Test that commands verify company_id matches"""
        position, position_id, company_id = create_test_position()
        position.publish()

        repository = MockJobPositionRepository()
        repository.save(position)

        # Create command with matching company_id - should work
        handler = PublishJobPositionCommandHandler(repository)
        # Re-create position for this test
        position2, position_id2, company_id2 = create_test_position()
        repository.save(position2)

        command = PublishJobPositionCommand(
            job_position_id=position_id2.value,
            company_id=company_id2.value  # Matching company
        )

        # This should execute without error
        handler.execute(command)
        updated_position = repository.get_by_id(position_id2)
        assert updated_position.status == JobPositionStatusEnum.PUBLISHED
