from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass
class ApplicationQuestion:
    """
    Application Question entity - defines screening questions for job applications.

    These questions are defined at the workflow level and can be enabled/disabled
    per job position. They support automation rules for candidate qualification.
    """
    id: ApplicationQuestionId
    workflow_id: WorkflowId
    company_id: CompanyId
    field_key: str  # Unique key for automation rules (e.g., "expected_salary")
    label: str  # Display label for candidates
    description: Optional[str]  # Help text for candidates
    field_type: ApplicationQuestionFieldType
    options: Optional[List[str]]  # For SELECT/MULTISELECT types
    is_required_default: bool  # Default required state
    validation_rules: Optional[Dict[str, Any]]  # Field-level validation (min/max, pattern, etc.)
    sort_order: int  # Display order
    is_active: bool  # Whether this question is active
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: ApplicationQuestionId,
        workflow_id: WorkflowId,
        company_id: CompanyId,
        field_key: str,
        label: str,
        field_type: ApplicationQuestionFieldType,
        description: Optional[str] = None,
        options: Optional[List[str]] = None,
        is_required_default: bool = False,
        validation_rules: Optional[Dict[str, Any]] = None,
        sort_order: int = 0
    ) -> "ApplicationQuestion":
        """Factory method to create a new application question."""
        if not field_key:
            raise ValueError("Field key cannot be empty")
        if not label:
            raise ValueError("Label cannot be empty")

        # Validate options for SELECT/MULTISELECT
        if field_type in [ApplicationQuestionFieldType.SELECT, ApplicationQuestionFieldType.MULTISELECT]:
            if not options or len(options) == 0:
                raise ValueError(f"Options are required for {field_type.value} field type")

        now = datetime.utcnow()
        return cls(
            id=id,
            workflow_id=workflow_id,
            company_id=company_id,
            field_key=field_key,
            label=label,
            description=description,
            field_type=field_type,
            options=options,
            is_required_default=is_required_default,
            validation_rules=validation_rules,
            sort_order=sort_order,
            is_active=True,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        label: str,
        description: Optional[str] = None,
        options: Optional[List[str]] = None,
        is_required_default: Optional[bool] = None,
        validation_rules: Optional[Dict[str, Any]] = None,
        sort_order: Optional[int] = None
    ) -> None:
        """Update application question details."""
        if not label:
            raise ValueError("Label cannot be empty")

        self.label = label
        self.description = description

        if options is not None:
            # Validate options for SELECT/MULTISELECT
            if self.field_type in [ApplicationQuestionFieldType.SELECT, ApplicationQuestionFieldType.MULTISELECT]:
                if len(options) == 0:
                    raise ValueError(f"Options are required for {self.field_type.value} field type")
            self.options = options

        if is_required_default is not None:
            self.is_required_default = is_required_default

        if validation_rules is not None:
            self.validation_rules = validation_rules

        if sort_order is not None:
            self.sort_order = sort_order

        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the question."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the question."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_sort_order(self, sort_order: int) -> None:
        """Update the sort order."""
        self.sort_order = sort_order
        self.updated_at = datetime.utcnow()
