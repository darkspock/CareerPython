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
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.services.stage_phase_validation_service import \
    StagePhaseValidationService
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
            phase_repository: PhaseRepositoryInterface,
            workflow_repository: WorkflowRepositoryInterface,
            stage_repository: WorkflowStageRepositoryInterface,
            validation_service: StagePhaseValidationService
    ):
        self._repository = repository
        self._phase_repository = phase_repository
        self._workflow_repository = workflow_repository
        self._stage_repository = stage_repository
        self._validation_service = validation_service

    def execute(self, command: CreateCompanyCandidateCommand) -> None:
        """Handle the create company candidate command"""
        # Parse visibility settings or use default
        visibility_settings = VisibilitySettings.from_dict(
            command.visibility_settings) if command.visibility_settings else VisibilitySettings.default()

        # Get first phase and initial stage for automatic assignment (REQUIRED)
        workflow_id = None
        initial_stage_id = None
        phase_id = None

        # Get all active phases for the company, ordered by sort_order
        phases = self._phase_repository.list_by_company(command.company_id)
        
        # Filter phases of type CA (Candidate Application) and get the first one
        ca_phases = [p for p in phases if p.workflow_type == WorkflowTypeEnum.CANDIDATE_APPLICATION]
        
        if not ca_phases:
            raise ValueError(
                f"Cannot create candidate: No Candidate Application phases found for company {command.company_id.value}. "
                "Please create at least one phase of type 'Candidate Application' before adding candidates."
            )
        
        # Get the first phase (already ordered by sort_order)
        first_phase = ca_phases[0]
        phase_id = first_phase.id
        
        # Get stages for this phase
        stages = self._stage_repository.list_by_phase(phase_id, WorkflowTypeEnum.CANDIDATE_APPLICATION)
        
        if not stages:
            raise ValueError(
                f"Cannot create candidate: Phase '{first_phase.name}' has no stages. "
                "Please add at least one stage to this phase before adding candidates."
            )
        
        # Get the first stage (stages are ordered by 'order' field)
        first_stage = stages[0]
        initial_stage_id = first_stage.id
        
        # Get the workflow_id from the first stage
        workflow_id = first_stage.workflow_id
        
        # Validate stage belongs to workflow using Domain Service
        self._validation_service.validate_stage_belongs_to_workflow(
            stage_id=initial_stage_id,
            workflow_id=workflow_id
        )

        # Create the company candidate entity with phase
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

        # Assign workflow and initial stage (always required)
        company_candidate = company_candidate.assign_workflow(workflow_id, initial_stage_id, phase_id)

        # Save to repository
        self._repository.save(company_candidate)
