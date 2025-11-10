from dataclasses import dataclass
from typing import Optional, Dict, List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.company_candidate.domain.entities.company_candidate import CompanyCandidate
from src.company_bc.company_candidate.domain.enums.candidate_priority import CandidatePriority
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_bc.company_candidate.domain.value_objects.visibility_settings import VisibilitySettings
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.interfaces import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class CreateCompanyCandidateCommand(Command):
    """Command to create a new company candidate relationship"""
    id: CompanyCandidateId
    company_id: CompanyId
    candidate_id: CandidateId
    created_by_user_id: CompanyUserId
    source: str
    position: Optional[str] = None
    department: Optional[str] = None
    priority: CandidatePriority = CandidatePriority.MEDIUM
    visibility_settings: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    lead_id: Optional[str] = None
    resume_url: Optional[str] = None
    resume_uploaded_by: Optional[CompanyUserId] = None


class CreateCompanyCandidateCommandHandler(CommandHandler):
    """Handler for creating a new company candidate relationship"""

    def __init__(
            self,
            repository: CompanyCandidateRepositoryInterface,
            workflow_repository: WorkflowRepositoryInterface,
            stage_repository: WorkflowStageRepositoryInterface
    ):
        self._repository = repository
        self._workflow_repository = workflow_repository
        self._stage_repository = stage_repository

    def execute(self, command: CreateCompanyCandidateCommand) -> None:
        """Handle the create company candidate command"""
        # Parse visibility settings or use default
        visibility_settings = VisibilitySettings.from_dict(
            command.visibility_settings) if command.visibility_settings else VisibilitySettings.default()

        # Try to get default workflow and initial stage for automatic assignment
        workflow_id = None
        initial_stage_id = None
        phase_id = None

        try:
            # Get default workflow for the company
            default_workflow = self._workflow_repository.get_default_by_company(command.company_id)
            if default_workflow:
                workflow_id = WorkflowId.from_string(str(default_workflow.id))
                phase_id = default_workflow.phase_id

                # Get initial stage of the workflow
                initial_stage = self._stage_repository.get_initial_stage(workflow_id)
                if initial_stage:
                    initial_stage_id = initial_stage.id
        except Exception as e:
            # Log the error but don't fail the candidate creation
            # This ensures candidates are still created even if workflow assignment fails
            print(f"Warning: Could not assign workflow automatically: {e}")

        # Create the company candidate entity
        company_candidate = CompanyCandidate.create(
            id=command.id,
            company_id=command.company_id,
            candidate_id=command.candidate_id,
            created_by_user_id=command.created_by_user_id,
            source=command.source,
            position=command.position,
            department=command.department,
            priority=command.priority,
            visibility_settings=visibility_settings,
            tags=command.tags or [],
            lead_id=command.lead_id,
            resume_url=command.resume_url,
            resume_uploaded_by=command.resume_uploaded_by,
            phase_id=phase_id
        )

        # If we found a workflow and initial stage, assign them
        if workflow_id and initial_stage_id:
            company_candidate = company_candidate.assign_workflow(workflow_id, initial_stage_id, phase_id)

        # Save to repository
        self._repository.save(company_candidate)
