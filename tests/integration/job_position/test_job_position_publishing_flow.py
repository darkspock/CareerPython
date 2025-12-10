"""
Integration tests for Job Position Publishing Flow
Tests the complete workflows for job position status transitions
"""
import pytest
from datetime import datetime
from decimal import Decimal
from typing import Optional
from unittest.mock import Mock, MagicMock

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.application.commands.create_job_position import (
    CreateJobPositionCommand, CreateJobPositionCommandHandler
)
from src.company_bc.job_position.application.commands.job_position_status_commands import (
    RequestJobPositionApprovalCommand, RequestJobPositionApprovalCommandHandler,
    ApproveJobPositionCommand, ApproveJobPositionCommandHandler,
    RejectJobPositionCommand, RejectJobPositionCommandHandler,
    PublishJobPositionCommand, PublishJobPositionCommandHandler,
    HoldJobPositionCommand, HoldJobPositionCommandHandler,
    ResumeJobPositionCommand, ResumeJobPositionCommandHandler,
    CloseJobPositionCommand, CloseJobPositionCommandHandler,
    CloneJobPositionCommand, CloneJobPositionCommandHandler
)
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import (
    JobPositionStatusEnum,
    JobPositionVisibilityEnum,
    ClosedReasonEnum
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import (
    JobPositionRepositoryInterface
)
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum,
    InterviewTemplateScopeEnum
)
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import (
    InterviewTemplateRepositoryInterface
)
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId


class MockJobPositionRepository:
    """In-memory mock repository for testing"""

    def __init__(self):
        self.positions: dict[str, JobPosition] = {}

    def save(self, position: JobPosition) -> None:
        self.positions[position.id.value] = position

    def get_by_id(self, position_id: JobPositionId) -> Optional[JobPosition]:
        return self.positions.get(position_id.value)


class MockInterviewTemplateRepository:
    """In-memory mock repository for interview templates"""

    def __init__(self):
        self.templates: dict[str, InterviewTemplate] = {}

    def get_by_id(self, template_id: InterviewTemplateId) -> Optional[InterviewTemplate]:
        return self.templates.get(template_id.value)

    def create(self, template: InterviewTemplate) -> InterviewTemplate:
        self.templates[template.id.value] = template
        return template

    def add(self, template: InterviewTemplate) -> None:
        """Add a template for testing"""
        self.templates[template.id.value] = template


def create_test_position(
    title: str = "Software Engineer",
    description: str = "A great position",
    budget_max: Optional[Decimal] = None
) -> tuple[JobPosition, JobPositionId, CompanyId]:
    """Helper to create a test position"""
    position_id = JobPositionId.generate()
    company_id = CompanyId.generate()

    position = JobPosition.create(
        id=position_id,
        title=title,
        company_id=company_id,
        description=description,
        job_category=JobCategoryEnum.TECHNOLOGY,
        budget_max=budget_max
    )

    return position, position_id, company_id


def create_test_screening_template(company_id: CompanyId) -> InterviewTemplate:
    """Helper to create a test screening template with APPLICATION scope"""
    return InterviewTemplate.create(
        id=InterviewTemplateId.generate(),
        company_id=company_id,
        name="Screening Template",
        intro="Welcome to the screening",
        prompt="Please answer the questions",
        goal="Evaluate candidate fit",
        status=InterviewTemplateStatusEnum.ENABLED,
        template_type=InterviewTemplateTypeEnum.SCREENING,
        scope=InterviewTemplateScopeEnum.APPLICATION,
        job_category=JobCategoryEnum.TECHNOLOGY
    )


# ==================== 8.2.1 FULL PUBLISHING FLOW ====================

class TestFullPublishingFlow:
    """Test Draft → PendingApproval → Approved → Published flow"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_full_publishing_flow_with_approval(self):
        """Test complete flow: Draft → Approval → Published"""
        # Create position
        position, position_id, company_id = create_test_position(
            budget_max=Decimal("100000")
        )
        self.repository.save(position)

        # 1. Request Approval
        request_handler = RequestJobPositionApprovalCommandHandler(self.repository)
        request_command = RequestJobPositionApprovalCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        request_handler.execute(request_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.PENDING_APPROVAL

        # 2. Approve
        approve_handler = ApproveJobPositionCommandHandler(self.repository)
        approve_command = ApproveJobPositionCommand(
            job_position_id=position_id.value,
            approver_id="approver-123",
            company_id=company_id.value
        )
        approve_handler.execute(approve_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.APPROVED
        assert position.approved_budget_max == Decimal("100000")

        # 3. Publish
        publish_handler = PublishJobPositionCommandHandler(self.repository)
        publish_command = PublishJobPositionCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        publish_handler.execute(publish_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.PUBLISHED
        assert position.visibility == JobPositionVisibilityEnum.PUBLIC
        assert position.published_at is not None


# ==================== 8.2.2 SIMPLE PUBLISHING FLOW ====================

class TestSimplePublishingFlow:
    """Test Draft → Published flow (quick mode)"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_simple_publishing_flow(self):
        """Test quick flow: Draft → Published"""
        position, position_id, company_id = create_test_position()
        self.repository.save(position)

        # Direct publish from draft
        publish_handler = PublishJobPositionCommandHandler(self.repository)
        publish_command = PublishJobPositionCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        publish_handler.execute(publish_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.PUBLISHED
        assert position.published_at is not None


# ==================== 8.2.3 REJECTION FLOW ====================

class TestRejectionFlow:
    """Test Draft → PendingApproval → Rejected → Draft flow"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_rejection_and_resubmission_flow(self):
        """Test flow: Draft → Pending → Rejected → Draft"""
        position, position_id, company_id = create_test_position()
        self.repository.save(position)

        # 1. Request Approval
        request_handler = RequestJobPositionApprovalCommandHandler(self.repository)
        request_command = RequestJobPositionApprovalCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        request_handler.execute(request_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.PENDING_APPROVAL

        # 2. Reject
        reject_handler = RejectJobPositionCommandHandler(self.repository)
        reject_command = RejectJobPositionCommand(
            job_position_id=position_id.value,
            reason="Budget needs review",
            company_id=company_id.value
        )
        reject_handler.execute(reject_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.REJECTED

        # 3. Revert to Draft
        position.revert_to_draft()
        self.repository.save(position)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.DRAFT


# ==================== 8.2.4 CLOSE WITH REASON ====================

class TestCloseFlow:
    """Test closing a published position with reason"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_close_published_position(self):
        """Test closing a published position"""
        position, position_id, company_id = create_test_position()
        position.publish()
        self.repository.save(position)

        # Close position
        close_handler = CloseJobPositionCommandHandler(self.repository)
        close_command = CloseJobPositionCommand(
            job_position_id=position_id.value,
            closed_reason=ClosedReasonEnum.FILLED,
            company_id=company_id.value
        )
        close_handler.execute(close_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.CLOSED
        assert position.closed_reason == ClosedReasonEnum.FILLED
        assert position.closed_at is not None

    def test_close_on_hold_position(self):
        """Test closing an on-hold position"""
        position, position_id, company_id = create_test_position()
        position.publish()
        position.put_on_hold()
        self.repository.save(position)

        # Close position
        close_handler = CloseJobPositionCommandHandler(self.repository)
        close_command = CloseJobPositionCommand(
            job_position_id=position_id.value,
            closed_reason=ClosedReasonEnum.CANCELLED,
            company_id=company_id.value
        )
        close_handler.execute(close_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.CLOSED


# ==================== 8.2.5 CLONE POSITION ====================

class TestCloneFlow:
    """Test cloning a position"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_clone_published_position(self):
        """Test cloning a published position"""
        position, position_id, company_id = create_test_position(
            title="Senior Developer",
            description="Senior position"
        )
        position.publish()
        self.repository.save(position)

        # Clone position
        new_position_id = JobPositionId.generate()
        clone_handler = CloneJobPositionCommandHandler(self.repository)
        clone_command = CloneJobPositionCommand(
            source_job_position_id=position_id.value,
            company_id=company_id.value,
            new_job_position_id=new_position_id.value
        )
        clone_handler.execute(clone_command)

        # Verify original unchanged
        original = self.repository.get_by_id(position_id)
        assert original.status == JobPositionStatusEnum.PUBLISHED

        # Verify clone in DRAFT
        cloned = self.repository.get_by_id(new_position_id)
        assert cloned is not None
        assert cloned.status == JobPositionStatusEnum.DRAFT
        assert "Senior Developer" in cloned.title
        assert cloned.description == "Senior position"


# ==================== 8.2.6 SCREENING TEMPLATE LINK ====================

class TestScreeningTemplateLink:
    """Test linking screening template to position"""

    def setup_method(self):
        self.position_repository = MockJobPositionRepository()
        self.template_repository = MockInterviewTemplateRepository()

    def test_create_position_with_screening_template(self):
        """Test creating position with valid screening template"""
        company_id = CompanyId.generate()
        position_id = JobPositionId.generate()

        # Create screening template with APPLICATION scope
        template = create_test_screening_template(company_id)
        self.template_repository.add(template)

        # Create position with template link
        handler = CreateJobPositionCommandHandler(
            self.position_repository,
            self.template_repository
        )

        command = CreateJobPositionCommand(
            id=position_id,
            company_id=company_id,
            title="Developer Position",
            description="A developer position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            screening_template_id=template.id.value
        )

        handler.execute(command)

        position = self.position_repository.get_by_id(position_id)
        assert position is not None
        assert position.screening_template_id == template.id.value

    def test_create_position_with_invalid_screening_template_scope(self):
        """Test creating position with wrong scope template fails"""
        from src.company_bc.job_position.domain.exceptions import JobPositionInvalidScreeningTemplateError

        company_id = CompanyId.generate()
        position_id = JobPositionId.generate()

        # Create template with STANDALONE scope (not APPLICATION)
        template = InterviewTemplate.create(
            id=InterviewTemplateId.generate(),
            company_id=company_id,
            name="Standalone Template",
            intro="Welcome",
            prompt="Answer",
            goal="Evaluate",
            status=InterviewTemplateStatusEnum.ENABLED,
            template_type=InterviewTemplateTypeEnum.SCREENING,
            scope=InterviewTemplateScopeEnum.STANDALONE,  # Wrong scope
            job_category=JobCategoryEnum.TECHNOLOGY
        )
        self.template_repository.add(template)

        handler = CreateJobPositionCommandHandler(
            self.position_repository,
            self.template_repository
        )

        command = CreateJobPositionCommand(
            id=position_id,
            company_id=company_id,
            title="Developer Position",
            description="A developer position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            screening_template_id=template.id.value
        )

        with pytest.raises(JobPositionInvalidScreeningTemplateError):
            handler.execute(command)

    def test_create_position_with_nonexistent_template(self):
        """Test creating position with non-existent template fails"""
        from src.company_bc.job_position.domain.exceptions import JobPositionInvalidScreeningTemplateError

        company_id = CompanyId.generate()
        position_id = JobPositionId.generate()

        handler = CreateJobPositionCommandHandler(
            self.position_repository,
            self.template_repository
        )

        command = CreateJobPositionCommand(
            id=position_id,
            company_id=company_id,
            title="Developer Position",
            description="A developer position",
            job_category=JobCategoryEnum.TECHNOLOGY,
            screening_template_id="non-existent-id"
        )

        with pytest.raises(JobPositionInvalidScreeningTemplateError):
            handler.execute(command)


# ==================== HOLD/RESUME FLOW ====================

class TestHoldResumeFlow:
    """Test hold and resume flow"""

    def setup_method(self):
        self.repository = MockJobPositionRepository()

    def test_hold_and_resume_flow(self):
        """Test Published → OnHold → Published flow"""
        position, position_id, company_id = create_test_position()
        position.publish()
        self.repository.save(position)

        # Hold
        hold_handler = HoldJobPositionCommandHandler(self.repository)
        hold_command = HoldJobPositionCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        hold_handler.execute(hold_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.ON_HOLD

        # Resume
        resume_handler = ResumeJobPositionCommandHandler(self.repository)
        resume_command = ResumeJobPositionCommand(
            job_position_id=position_id.value,
            company_id=company_id.value
        )
        resume_handler.execute(resume_command)

        position = self.repository.get_by_id(position_id)
        assert position.status == JobPositionStatusEnum.PUBLISHED
