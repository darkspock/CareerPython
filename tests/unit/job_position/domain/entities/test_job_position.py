"""
Unit tests for JobPosition entity - Publishing Flow
Tests status transitions, field locking, budget validation, and custom fields
"""
import pytest
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import (
    JobPositionStatusEnum,
    JobPositionVisibilityEnum,
    ClosedReasonEnum
)
from src.company_bc.job_position.domain.exceptions import (
    JobPositionInvalidStatusTransitionError,
    JobPositionFieldLockedError,
    JobPositionBudgetExceededError
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.framework.domain.enums.job_category import JobCategoryEnum


class JobPositionMother:
    """Factory for creating test JobPosition instances"""

    @staticmethod
    def create_draft_position(
        title: str = "Software Engineer",
        company_id: Optional[CompanyId] = None,
        budget_max: Optional[Decimal] = None,
        salary_max: Optional[Decimal] = None,
        custom_fields_config: Optional[list] = None,
        description: str = "A great position for a software engineer"
    ) -> JobPosition:
        """Create a job position in DRAFT status"""
        return JobPosition.create(
            id=JobPositionId.generate(),
            title=title,
            company_id=company_id or CompanyId.generate(),
            job_category=JobCategoryEnum.TECHNOLOGY,
            budget_max=budget_max,
            salary_max=salary_max,
            custom_fields_config=custom_fields_config or [],
            description=description
        )

    @staticmethod
    def create_pending_approval_position() -> JobPosition:
        """Create a job position in PENDING_APPROVAL status"""
        position = JobPositionMother.create_draft_position()
        position.request_approval()
        return position

    @staticmethod
    def create_approved_position(approver_id: str = "approver-123") -> JobPosition:
        """Create a job position in APPROVED status"""
        position = JobPositionMother.create_draft_position(budget_max=Decimal("100000"))
        position.request_approval()
        position.approve(approver_id)
        return position

    @staticmethod
    def create_published_position() -> JobPosition:
        """Create a job position in PUBLISHED status"""
        position = JobPositionMother.create_approved_position()
        position.publish()
        return position

    @staticmethod
    def create_on_hold_position() -> JobPosition:
        """Create a job position in ON_HOLD status"""
        position = JobPositionMother.create_published_position()
        position.put_on_hold()
        return position

    @staticmethod
    def create_closed_position(reason: ClosedReasonEnum = ClosedReasonEnum.FILLED) -> JobPosition:
        """Create a job position in CLOSED status"""
        position = JobPositionMother.create_published_position()
        position.close(reason)
        return position


# ==================== 8.1.1 STATUS TRANSITIONS - VALID PATHS ====================

class TestStatusTransitionsValidPaths:
    """Test valid status transition paths"""

    def test_draft_to_pending_approval(self):
        """DRAFT -> PENDING_APPROVAL"""
        position = JobPositionMother.create_draft_position()
        assert position.status == JobPositionStatusEnum.DRAFT

        position.request_approval()

        assert position.status == JobPositionStatusEnum.PENDING_APPROVAL

    def test_pending_approval_to_approved(self):
        """PENDING_APPROVAL -> APPROVED"""
        # Need budget_max to capture approver info
        position = JobPositionMother.create_draft_position(budget_max=Decimal("100000"))
        position.request_approval()
        assert position.status == JobPositionStatusEnum.PENDING_APPROVAL

        position.approve("approver-123")

        assert position.status == JobPositionStatusEnum.APPROVED
        assert position.financial_approver_id == "approver-123"
        assert position.approved_at is not None

    def test_pending_approval_to_rejected(self):
        """PENDING_APPROVAL -> REJECTED"""
        position = JobPositionMother.create_pending_approval_position()

        position.reject("Budget too high")

        assert position.status == JobPositionStatusEnum.REJECTED

    def test_pending_approval_to_draft_withdraw(self):
        """PENDING_APPROVAL -> DRAFT (withdraw)"""
        position = JobPositionMother.create_pending_approval_position()

        position.withdraw_approval_request()

        assert position.status == JobPositionStatusEnum.DRAFT

    def test_approved_to_published(self):
        """APPROVED -> PUBLISHED"""
        position = JobPositionMother.create_approved_position()
        assert position.status == JobPositionStatusEnum.APPROVED

        position.publish()

        assert position.status == JobPositionStatusEnum.PUBLISHED
        assert position.published_at is not None
        assert position.visibility == JobPositionVisibilityEnum.PUBLIC

    def test_approved_to_draft_revert(self):
        """APPROVED -> DRAFT (revert)"""
        position = JobPositionMother.create_approved_position()

        position.revert_to_draft()

        assert position.status == JobPositionStatusEnum.DRAFT

    def test_draft_to_published_quick_mode(self):
        """DRAFT -> PUBLISHED (quick mode - no approval required)"""
        position = JobPositionMother.create_draft_position()

        position.publish()

        assert position.status == JobPositionStatusEnum.PUBLISHED
        assert position.published_at is not None

    def test_published_to_on_hold(self):
        """PUBLISHED -> ON_HOLD"""
        position = JobPositionMother.create_published_position()

        position.put_on_hold()

        assert position.status == JobPositionStatusEnum.ON_HOLD

    def test_on_hold_to_published_resume(self):
        """ON_HOLD -> PUBLISHED (resume)"""
        position = JobPositionMother.create_on_hold_position()

        position.resume()

        assert position.status == JobPositionStatusEnum.PUBLISHED

    def test_published_to_closed(self):
        """PUBLISHED -> CLOSED"""
        position = JobPositionMother.create_published_position()

        position.close(ClosedReasonEnum.FILLED)

        assert position.status == JobPositionStatusEnum.CLOSED
        assert position.closed_reason == ClosedReasonEnum.FILLED
        assert position.closed_at is not None

    def test_on_hold_to_closed(self):
        """ON_HOLD -> CLOSED"""
        position = JobPositionMother.create_on_hold_position()

        position.close(ClosedReasonEnum.CANCELLED)

        assert position.status == JobPositionStatusEnum.CLOSED

    def test_closed_to_archived(self):
        """CLOSED -> ARCHIVED"""
        position = JobPositionMother.create_closed_position()

        position.archive()

        assert position.status == JobPositionStatusEnum.ARCHIVED

    def test_closed_to_draft_reopen(self):
        """CLOSED -> DRAFT (reopen)"""
        position = JobPositionMother.create_closed_position()

        position.revert_to_draft()

        assert position.status == JobPositionStatusEnum.DRAFT

    def test_rejected_to_draft(self):
        """REJECTED -> DRAFT (revise)"""
        position = JobPositionMother.create_pending_approval_position()
        position.reject("Needs changes")

        position.revert_to_draft()

        assert position.status == JobPositionStatusEnum.DRAFT


# ==================== 8.1.2 STATUS TRANSITIONS - INVALID PATHS ====================

class TestStatusTransitionsInvalidPaths:
    """Test invalid status transition paths - should fail"""

    def test_draft_to_approved_fails(self):
        """DRAFT -> APPROVED should fail (must go through PENDING_APPROVAL)"""
        position = JobPositionMother.create_draft_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.approve("approver-123")

    def test_draft_to_closed_fails(self):
        """DRAFT -> CLOSED should fail"""
        position = JobPositionMother.create_draft_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.close(ClosedReasonEnum.FILLED)

    def test_draft_to_on_hold_fails(self):
        """DRAFT -> ON_HOLD should fail"""
        position = JobPositionMother.create_draft_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.put_on_hold()

    def test_pending_approval_to_published_fails(self):
        """PENDING_APPROVAL -> PUBLISHED should fail (must approve first)"""
        position = JobPositionMother.create_pending_approval_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.publish()

    def test_pending_approval_to_closed_fails(self):
        """PENDING_APPROVAL -> CLOSED should fail"""
        position = JobPositionMother.create_pending_approval_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.close(ClosedReasonEnum.CANCELLED)

    def test_approved_to_on_hold_fails(self):
        """APPROVED -> ON_HOLD should fail (must publish first)"""
        position = JobPositionMother.create_approved_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.put_on_hold()

    def test_rejected_to_approved_fails(self):
        """REJECTED -> APPROVED should fail (must go back to draft first)"""
        position = JobPositionMother.create_pending_approval_position()
        position.reject("Not good")

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.approve("approver-123")

    def test_closed_to_published_fails(self):
        """CLOSED -> PUBLISHED should fail (must reopen to draft first)"""
        position = JobPositionMother.create_closed_position()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.publish()

    def test_archived_to_draft_fails(self):
        """ARCHIVED -> DRAFT should fail (archived is final)"""
        position = JobPositionMother.create_closed_position()
        position.archive()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.revert_to_draft()

    def test_archived_to_published_fails(self):
        """ARCHIVED -> PUBLISHED should fail"""
        position = JobPositionMother.create_closed_position()
        position.archive()

        with pytest.raises(JobPositionInvalidStatusTransitionError):
            position.publish()


# ==================== 8.1.3 FIELD LOCKING PER STATUS ====================

class TestFieldLockingPerStatus:
    """Test field locking based on status"""

    def test_draft_all_fields_editable(self):
        """In DRAFT, all fields should be editable"""
        position = JobPositionMother.create_draft_position()

        # All fields should not be locked
        assert not position.is_field_locked("title")
        assert not position.is_field_locked("budget_max")
        assert not position.is_field_locked("custom_fields_config")
        assert not position.is_field_locked("salary_max")

    def test_approved_budget_locked(self):
        """In APPROVED, budget_max should be locked"""
        position = JobPositionMother.create_approved_position()

        assert position.is_field_locked("budget_max")
        assert not position.is_field_locked("title")

    def test_published_budget_and_custom_fields_locked(self):
        """In PUBLISHED, budget_max and custom_fields_config should be locked"""
        position = JobPositionMother.create_published_position()

        assert position.is_field_locked("budget_max")
        assert position.is_field_locked("custom_fields_config")
        assert not position.is_field_locked("title")

    def test_on_hold_budget_and_custom_fields_locked(self):
        """In ON_HOLD, budget_max and custom_fields_config should be locked"""
        position = JobPositionMother.create_on_hold_position()

        assert position.is_field_locked("budget_max")
        assert position.is_field_locked("custom_fields_config")

    def test_closed_additional_fields_locked(self):
        """In CLOSED, budget, custom_fields, and salary should be locked"""
        position = JobPositionMother.create_closed_position()

        assert position.is_field_locked("budget_max")
        assert position.is_field_locked("custom_fields_config")
        assert position.is_field_locked("salary_max")
        assert position.is_field_locked("salary_min")

    def test_archived_all_fields_locked(self):
        """In ARCHIVED, all fields should be locked"""
        position = JobPositionMother.create_closed_position()
        position.archive()

        assert position.is_field_locked("title")
        assert position.is_field_locked("budget_max")
        assert position.is_field_locked("custom_fields_config")
        assert position.is_field_locked("salary_max")
        assert position.is_field_locked("description")


# ==================== 8.1.4 BUDGET VALIDATION ====================

class TestBudgetValidation:
    """Test salary vs budget validation"""

    def test_salary_within_budget_allowed(self):
        """Salary within budget should be allowed"""
        position = JobPositionMother.create_draft_position(
            budget_max=Decimal("100000"),
            salary_max=Decimal("90000")
        )

        # Should not raise
        position.validate_salary_against_budget()

    def test_salary_equals_budget_allowed(self):
        """Salary equal to budget should be allowed"""
        position = JobPositionMother.create_draft_position(
            budget_max=Decimal("100000"),
            salary_max=Decimal("100000")
        )

        # Should not raise
        position.validate_salary_against_budget()

    def test_salary_exceeds_budget_fails(self):
        """Salary exceeding budget should fail"""
        position = JobPositionMother.create_draft_position(
            budget_max=Decimal("100000"),
            salary_max=Decimal("110000")
        )

        with pytest.raises(JobPositionBudgetExceededError):
            position.validate_salary_against_budget()

    def test_no_budget_allows_any_salary(self):
        """Without budget limit, any salary is allowed"""
        position = JobPositionMother.create_draft_position(
            budget_max=None,
            salary_max=Decimal("999999")
        )

        # Should not raise
        position.validate_salary_against_budget()

    def test_is_within_budget_true(self):
        """is_within_budget should return True when amount is within budget"""
        position = JobPositionMother.create_approved_position()
        position.approved_budget_max = Decimal("100000")

        assert position.is_within_budget(Decimal("90000")) is True

    def test_is_within_budget_false(self):
        """is_within_budget should return False when amount exceeds budget"""
        position = JobPositionMother.create_approved_position()
        position.approved_budget_max = Decimal("100000")

        assert position.is_within_budget(Decimal("110000")) is False


# ==================== 8.1.5 CUSTOM FIELDS SNAPSHOT ====================

class TestCustomFieldsSnapshot:
    """Test custom fields snapshot on creation"""

    def test_custom_fields_copied_on_create(self):
        """Custom fields should be set on creation"""
        custom_fields = [
            CustomFieldDefinition(
                field_key="years_experience",
                label="Years of Experience",
                field_type="NUMBER",
                options=None,
                is_required=True,
                candidate_visible=True,
                validation_rules=None,
                sort_order=1,
                is_active=True
            )
        ]

        position = JobPositionMother.create_draft_position(
            custom_fields_config=custom_fields
        )

        assert len(position.custom_fields_config) == 1
        assert position.custom_fields_config[0].field_key == "years_experience"

    def test_custom_fields_stored_on_create(self):
        """Custom fields should be stored on creation"""
        custom_fields = [
            CustomFieldDefinition(
                field_key="test_field",
                label="Test Field",
                field_type="TEXT",
                options=None,
                is_required=False,
                candidate_visible=True,
                validation_rules=None,
                sort_order=1,
                is_active=True
            )
        ]

        position = JobPositionMother.create_draft_position(
            custom_fields_config=custom_fields
        )

        # Verify the field was stored
        assert len(position.custom_fields_config) == 1
        assert position.custom_fields_config[0].field_key == "test_field"
        assert position.custom_fields_config[0].label == "Test Field"


# ==================== 8.1.6 CUSTOM FIELDS FREEZE ON PUBLISH ====================

class TestCustomFieldsFreezeOnPublish:
    """Test custom fields freeze after publish"""

    def test_custom_fields_editable_in_draft(self):
        """Custom fields config should be editable in DRAFT"""
        position = JobPositionMother.create_draft_position()

        assert not position.is_field_locked("custom_fields_config")

    def test_custom_fields_editable_in_pending_approval(self):
        """Custom fields config should be editable in PENDING_APPROVAL"""
        position = JobPositionMother.create_pending_approval_position()

        assert not position.is_field_locked("custom_fields_config")

    def test_custom_fields_editable_in_approved(self):
        """Custom fields config should still be editable in APPROVED"""
        position = JobPositionMother.create_approved_position()

        assert not position.is_field_locked("custom_fields_config")

    def test_custom_fields_locked_in_published(self):
        """Custom fields config should be locked after PUBLISHED"""
        position = JobPositionMother.create_published_position()

        assert position.is_field_locked("custom_fields_config")

    def test_custom_fields_locked_in_on_hold(self):
        """Custom fields config should be locked in ON_HOLD"""
        position = JobPositionMother.create_on_hold_position()

        assert position.is_field_locked("custom_fields_config")

    def test_custom_fields_locked_in_closed(self):
        """Custom fields config should be locked in CLOSED"""
        position = JobPositionMother.create_closed_position()

        assert position.is_field_locked("custom_fields_config")

    def test_custom_field_values_always_editable(self):
        """Custom field values should always be editable (not locked)"""
        # Values can be updated at any status (for candidate data)
        position = JobPositionMother.create_published_position()

        # custom_fields_values is not in the locked list
        assert not position.is_field_locked("custom_fields_values")


# ==================== APPROVAL FLOW TESTS ====================

class TestApprovalFlow:
    """Test the approval flow specifics"""

    def test_approve_captures_budget(self):
        """Approve should capture approved_budget_max from budget_max"""
        position = JobPositionMother.create_draft_position(
            budget_max=Decimal("100000")
        )
        position.request_approval()

        position.approve("approver-123")

        assert position.approved_budget_max == Decimal("100000")

    def test_approve_sets_approver_id(self):
        """Approve should set financial_approver_id when budget_max is set"""
        position = JobPositionMother.create_draft_position(budget_max=Decimal("100000"))
        position.request_approval()

        position.approve("approver-456")

        assert position.financial_approver_id == "approver-456"

    def test_approve_sets_approved_at(self):
        """Approve should set approved_at timestamp when budget_max is set"""
        position = JobPositionMother.create_draft_position(budget_max=Decimal("100000"))
        position.request_approval()

        position.approve("approver-123")

        assert position.approved_at is not None
        assert isinstance(position.approved_at, datetime)


# ==================== CLONE TESTS ====================

class TestClone:
    """Test job position cloning"""

    def test_clone_creates_draft(self):
        """Cloned position should start in DRAFT"""
        position = JobPositionMother.create_published_position()

        cloned = position.clone(JobPositionId.generate())

        assert cloned.status == JobPositionStatusEnum.DRAFT

    def test_clone_preserves_content(self):
        """Clone should preserve content fields"""
        position = JobPositionMother.create_draft_position(title="Original Title")
        position.description = "Original Description"

        cloned = position.clone(JobPositionId.generate())

        assert "Original Title" in cloned.title  # Will have " (Copy)" suffix
        assert cloned.description == "Original Description"

    def test_clone_clears_lifecycle_fields(self):
        """Clone should clear lifecycle fields"""
        position = JobPositionMother.create_closed_position()

        cloned = position.clone(JobPositionId.generate())

        assert cloned.closed_at is None
        assert cloned.closed_reason is None
        assert cloned.published_at is None
        assert cloned.approved_at is None
        assert cloned.approved_budget_max is None

    def test_clone_has_new_id(self):
        """Clone should have a new ID"""
        position = JobPositionMother.create_draft_position()
        new_id = JobPositionId.generate()

        cloned = position.clone(new_id)

        assert cloned.id == new_id
        assert cloned.id != position.id
