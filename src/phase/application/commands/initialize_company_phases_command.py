"""Initialize default phases for a new company"""
from dataclasses import dataclass
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.entities.phase import Phase
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.company_workflow.domain.entities.company_workflow import CompanyWorkflow
from src.company_workflow.domain.entities.workflow_stage import WorkflowStage
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class InitializeCompanyPhasesCommand(Command):
    """Command to initialize default phases for a new company

    Phase 12: This command creates 4 default phases with workflows:
    - Sourcing (Kanban view) - Screening and filtering
    - Evaluation (Kanban view) - Interview and assessment
    - Offer and Pre-Onboarding (List view) - Offer negotiation and documents
    - Talent Pool (List view) - Long-term candidate tracking
    """
    company_id: CompanyId


class InitializeCompanyPhasesCommandHandler(CommandHandler):
    """Handler for InitializeCompanyPhasesCommand"""

    def __init__(
        self,
        phase_repository: PhaseRepositoryInterface,
        workflow_repository: CompanyWorkflowRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        self.phase_repository = phase_repository
        self.workflow_repository = workflow_repository
        self.stage_repository = stage_repository

    def execute(self, command: InitializeCompanyPhasesCommand) -> None:
        """Execute the command to create default phases

        Creates 4 default phases with specific workflows:
        1. Sourcing (sort_order=0, Kanban) - Screening process
        2. Evaluation (sort_order=1, Kanban) - Interview and assessment
        3. Offer and Pre-Onboarding (sort_order=2, List) - Offer negotiation
        4. Talent Pool (sort_order=3, List) - Long-term tracking

        Note: This will only create phases if they don't already exist.
        """
        # Check if phases already exist for this company
        existing_phases = self.phase_repository.list_by_company(command.company_id)
        if existing_phases:
            # Phases already exist, skip initialization
            return

        # Phase 1: Sourcing
        phase1_id = PhaseId.generate()
        phase1 = Phase.create(
            id=phase1_id,
            company_id=command.company_id,
            name="Sourcing",
            sort_order=0,
            default_view=DefaultView.KANBAN,
            objective="Screening and descarte process - identify qualified candidates"
        )
        self.phase_repository.save(phase1)

        # Create Sourcing workflow
        workflow1_id = CompanyWorkflowId.generate()
        self._create_sourcing_workflow(workflow1_id, command.company_id, phase1_id.value)

        # Phase 2: Evaluation
        phase2_id = PhaseId.generate()
        phase2 = Phase.create(
            id=phase2_id,
            company_id=command.company_id,
            name="Evaluation",
            sort_order=1,
            default_view=DefaultView.KANBAN,
            objective="Interview and assessment process"
        )
        self.phase_repository.save(phase2)

        # Create Evaluation workflow
        workflow2_id = CompanyWorkflowId.generate()
        self._create_evaluation_workflow(workflow2_id, command.company_id, phase2_id.value)

        # Phase 3: Offer and Pre-Onboarding
        phase3_id = PhaseId.generate()
        phase3 = Phase.create(
            id=phase3_id,
            company_id=command.company_id,
            name="Offer and Pre-Onboarding",
            sort_order=2,
            default_view=DefaultView.LIST,
            objective="Offer proposal, negotiation and document verification"
        )
        self.phase_repository.save(phase3)

        # Create Offer workflow
        workflow3_id = CompanyWorkflowId.generate()
        self._create_offer_workflow(workflow3_id, command.company_id, phase3_id.value)

        # Phase 4: Talent Pool
        phase4_id = PhaseId.generate()
        phase4 = Phase.create(
            id=phase4_id,
            company_id=command.company_id,
            name="Talent Pool",
            sort_order=3,
            default_view=DefaultView.LIST,
            objective="Long-term candidate tracking and talent pipeline management"
        )
        self.phase_repository.save(phase4)

        # Create Talent Pool workflow
        workflow4_id = CompanyWorkflowId.generate()
        self._create_talent_pool_workflow(workflow4_id, command.company_id, phase4_id.value)

        # Update workflows to set next_phase_id in SUCCESS stages
        self._update_success_stage_next_phase(workflow1_id, phase2_id.value)
        self._update_success_stage_next_phase(workflow2_id, phase3_id.value)
        # Phase 3 success can transition to Talent Pool
        self._update_success_stage_next_phase(workflow3_id, phase4_id.value)

    def _create_sourcing_workflow(self, workflow_id: CompanyWorkflowId, company_id: CompanyId, phase_id: str) -> None:
        """Create Sourcing workflow with 5 stages per WORKFLOW3.md"""
        workflow = CompanyWorkflow.create(
            id=workflow_id, company_id=company_id, name="Sourcing Workflow",
            description="Screening and filtering candidates", phase_id=phase_id, is_default=True
        )
        workflow = workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("Pending", "Application pending review", StageType.INITIAL, 0),
            ("Screening", "Initial screening in progress", StageType.STANDARD, 1),
            ("Qualified", "Candidate is qualified", StageType.SUCCESS, 2),
            ("Not Suitable", "Candidate not suitable for position", StageType.FAIL, 3),
            ("On Hold", "Application on hold", StageType.STANDARD, 4),
        ]
        for name, desc, stage_type, order in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(), workflow_id=workflow_id, name=name,
                description=desc, stage_type=stage_type, order=order,
                allow_skip=False, is_active=True
            )
            self.stage_repository.save(stage)

    def _create_evaluation_workflow(self, workflow_id: CompanyWorkflowId, company_id: CompanyId, phase_id: str) -> None:
        """Create Evaluation workflow with 6 stages per WORKFLOW3.md"""
        workflow = CompanyWorkflow.create(
            id=workflow_id, company_id=company_id, name="Evaluation Workflow",
            description="Interview and assessment process", phase_id=phase_id, is_default=True
        )
        workflow = workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("HR Interview", "Human Resources interview", StageType.INITIAL, 0),
            ("Manager Interview", "Manager interview", StageType.STANDARD, 1),
            ("Assessment Test", "Technical or skills assessment", StageType.STANDARD, 2),
            ("Executive Interview", "Executive level interview", StageType.STANDARD, 3),
            ("Selected", "Candidate selected for offer", StageType.SUCCESS, 4),
            ("Rejected", "Candidate rejected", StageType.FAIL, 5),
        ]
        for name, desc, stage_type, order in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(), workflow_id=workflow_id, name=name,
                description=desc, stage_type=stage_type, order=order,
                allow_skip=False, is_active=True
            )
            self.stage_repository.save(stage)

    def _create_offer_workflow(self, workflow_id: CompanyWorkflowId, company_id: CompanyId, phase_id: str) -> None:
        """Create Offer and Pre-Onboarding workflow with 5 stages per WORKFLOW3.md"""
        workflow = CompanyWorkflow.create(
            id=workflow_id, company_id=company_id, name="Offer and Pre-Onboarding Workflow",
            description="Offer negotiation and document verification", phase_id=phase_id, is_default=True
        )
        workflow = workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("Offer Proposal", "Offer proposed to candidate", StageType.INITIAL, 0),
            ("Negotiation", "Negotiating offer terms", StageType.STANDARD, 1),
            ("Document Submission", "Candidate submitting documents", StageType.STANDARD, 2),
            ("Document Verification", "Verifying submitted documents", StageType.SUCCESS, 3),
            ("Lost", "Candidate declined or withdrew", StageType.FAIL, 4),
        ]
        for name, desc, stage_type, order in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(), workflow_id=workflow_id, name=name,
                description=desc, stage_type=stage_type, order=order,
                allow_skip=False, is_active=True
            )
            self.stage_repository.save(stage)

    def _create_talent_pool_workflow(self, workflow_id: CompanyWorkflowId, company_id: CompanyId, phase_id: str) -> None:
        """Create Talent Pool workflow with 3 stages per WORKFLOW3.md"""
        workflow = CompanyWorkflow.create(
            id=workflow_id, company_id=company_id, name="Talent Pool Workflow",
            description="Long-term candidate tracking", phase_id=phase_id, is_default=True
        )
        workflow = workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("Welcome", "Candidate added to talent pool", StageType.INITIAL, 0),
            ("Recovered", "Candidate re-engaged for new opportunity", StageType.SUCCESS, 1),
            ("Lost", "Candidate no longer interested", StageType.FAIL, 2),
        ]
        for name, desc, stage_type, order in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(), workflow_id=workflow_id, name=name,
                description=desc, stage_type=stage_type, order=order,
                allow_skip=False, is_active=True
            )
            self.stage_repository.save(stage)

    def _update_success_stage_next_phase(self, workflow_id: CompanyWorkflowId, next_phase_id: str) -> None:
        """Update the SUCCESS stage of a workflow to set next_phase_id"""
        stages = self.stage_repository.list_by_workflow(workflow_id)

        for stage in stages:
            if stage.stage_type == StageType.SUCCESS:
                # Update stage with next_phase_id
                updated_stage = WorkflowStage(
                    id=stage.id,
                    workflow_id=stage.workflow_id,
                    name=stage.name,
                    description=stage.description,
                    stage_type=stage.stage_type,
                    order=stage.order,
                    allow_skip=stage.allow_skip,
                    estimated_duration_days=stage.estimated_duration_days,
                    is_active=stage.is_active,
                    default_role_ids=stage.default_role_ids,
                    default_assigned_users=stage.default_assigned_users,
                    email_template_id=stage.email_template_id,
                    custom_email_text=stage.custom_email_text,
                    deadline_days=stage.deadline_days,
                    estimated_cost=stage.estimated_cost,
                    next_phase_id=next_phase_id,  # Set the next phase
                    created_at=stage.created_at,
                    updated_at=stage.updated_at
                )
                self.stage_repository.save(updated_stage)
                break
