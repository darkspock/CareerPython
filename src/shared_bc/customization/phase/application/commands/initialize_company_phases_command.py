"""Initialize default phases for a new company"""
from dataclasses import dataclass

from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.phase.domain.entities.phase import Phase
from src.shared_bc.customization.phase.domain.enums.default_view_enum import DefaultView
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.entities.workflow import Workflow
from src.shared_bc.customization.workflow.domain.entities.workflow_stage import WorkflowStage
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_style import WorkflowStageStyle
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class InitializeCompanyPhasesCommand(Command):
    """Command to initialize default phases for a new company

    Creates phases and workflows for both workflow types:
    
    CANDIDATE_APPLICATION (3 phases):
    - Sourcing (Kanban view) - Screening and filtering
    - Evaluation (Kanban view) - Interview and assessment
    - Offer and Pre-Onboarding (List view) - Offer negotiation and documents
    
    JOB_POSITION_OPENING (1 phase):
    - Job Positions (Kanban view) - All job positions in one phase
    """
    company_id: CompanyId


class InitializeCompanyPhasesCommandHandler(CommandHandler):
    """Handler for InitializeCompanyPhasesCommand"""

    def __init__(
        self,
        phase_repository: PhaseRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface
    ):
        self.phase_repository = phase_repository
        self.workflow_repository = workflow_repository
        self.stage_repository = stage_repository

    def execute(self, command: InitializeCompanyPhasesCommand) -> None:
        """Execute the command to create default phases

        Creates phases and workflows for both workflow types:
        - CANDIDATE_APPLICATION: 3 phases (Sourcing, Evaluation, Offer)
        - JOB_POSITION_OPENING: 1 phase (Job Positions)

        Note: This will ARCHIVE all existing phases before creating the defaults.
        """
        # Archive all existing active phases for this company
        existing_phases = self.phase_repository.list_by_company(command.company_id)
        for phase in existing_phases:
            phase.archive()
            self.phase_repository.save(phase)

        # ============================================
        # CANDIDATE_APPLICATION Workflows
        # ============================================
        
        # Phase 1: Sourcing (Candidate Application)
        phase1_id = PhaseId.generate()
        phase1 = Phase.create(
            id=phase1_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=command.company_id,
            name="Sourcing",
            sort_order=0,
            default_view=DefaultView.KANBAN,
            objective="Screening and descarte process - identify qualified candidates"
        )
        self.phase_repository.save(phase1)

        # Create Sourcing workflow
        workflow1_id = WorkflowId.generate()
        self._create_sourcing_workflow(workflow1_id, command.company_id, phase1_id)

        # Phase 2: Evaluation (Candidate Application)
        phase2_id = PhaseId.generate()
        phase2 = Phase.create(
            id=phase2_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=command.company_id,
            name="Evaluation",
            sort_order=1,
            default_view=DefaultView.KANBAN,
            objective="Interview and assessment process"
        )
        self.phase_repository.save(phase2)

        # Create Evaluation workflow
        workflow2_id = WorkflowId.generate()
        self._create_evaluation_workflow(workflow2_id, command.company_id, phase2_id)

        # Phase 3: Offer and Pre-Onboarding (Candidate Application)
        phase3_id = PhaseId.generate()
        phase3 = Phase.create(
            id=phase3_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=command.company_id,
            name="Offer and Pre-Onboarding",
            sort_order=2,
            default_view=DefaultView.LIST,
            objective="Offer proposal, negotiation and document verification"
        )
        self.phase_repository.save(phase3)

        # Create Offer workflow
        workflow3_id = WorkflowId.generate()
        self._create_offer_workflow(workflow3_id, command.company_id, phase3_id)

        # Update workflows to set next_phase_id in SUCCESS stages
        self._update_success_stage_next_phase(workflow1_id, phase2_id)
        self._update_success_stage_next_phase(workflow2_id, phase3_id)
        # Phase 3 (Offer) is the final phase, no next phase transition

        # ============================================
        # JOB_POSITION_OPENING Workflows
        # ============================================
        
        # Single phase for Job Position Opening
        phase_jp_id = PhaseId.generate()
        phase_jp = Phase.create(
            id=phase_jp_id,
            workflow_type=WorkflowTypeEnum.JOB_POSITION_OPENING,
            company_id=command.company_id,
            name="Job Positions",
            sort_order=0,
            default_view=DefaultView.KANBAN,
            objective="All job positions in one workflow"
        )
        self.phase_repository.save(phase_jp)

        # Create workflow for Job Positions
        workflow_jp_id = WorkflowId.generate()
        self._create_job_position_workflow(workflow_jp_id, command.company_id, phase_jp_id)
        # No next phase transition needed (single phase)

    def _create_sourcing_workflow(self, workflow_id: WorkflowId, company_id: CompanyId, phase_id: PhaseId) -> None:
        """Create Sourcing workflow with 5 stages per WORKFLOW3.md"""
        workflow = Workflow.create(
            id=workflow_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=company_id,
            name="Sourcing Workflow",
            description="Screening and filtering candidates",
            display=WorkflowDisplayEnum.KANBAN,
            phase_id=phase_id,
            is_default=True
        )
        workflow.activate()
        self.workflow_repository.save(workflow)

        from src.shared_bc.customization.workflow.domain.enums.kanban_display_enum import KanbanDisplayEnum
        
        stages = [
            ("Pending", "Application pending review", WorkflowStageTypeEnum.INITIAL, 0, 
             WorkflowStageStyle(icon="📋", text_color="#92400e", background_color="#fef3c7"), KanbanDisplayEnum.COLUMN),  # amber
            ("Screening", "Initial screening in progress", WorkflowStageTypeEnum.PROGRESS, 1,
             WorkflowStageStyle(icon="🔍", text_color="#1e40af", background_color="#dbeafe"), KanbanDisplayEnum.COLUMN),  # blue
            ("Qualified", "Candidate is qualified", WorkflowStageTypeEnum.SUCCESS, 2,
             WorkflowStageStyle(icon="✅", text_color="#065f46", background_color="#d1fae5"), KanbanDisplayEnum.COLUMN),  # green
            ("Not Suitable", "Candidate not suitable for position", WorkflowStageTypeEnum.FAIL, 3,
             WorkflowStageStyle(icon="❌", text_color="#991b1b", background_color="#fee2e2"), KanbanDisplayEnum.ROW),  # red - ROW
            ("On Hold", "Application on hold", WorkflowStageTypeEnum.PROGRESS, 4,
             WorkflowStageStyle(icon="⏸️", text_color="#92400e", background_color="#fef3c7"), KanbanDisplayEnum.ROW),  # amber - ROW
        ]
        for name, desc, stage_type, order, style, kanban_display in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(),
                workflow_id=workflow_id,
                name=name,
                description=desc,
                stage_type=stage_type,
                order=order,
                allow_skip=False,
                is_active=True,
                style=style,
                kanban_display=kanban_display,
                validation_rules=None,
                recommended_rules=None
            )
            self.stage_repository.save(stage)

    def _create_evaluation_workflow(self, workflow_id: WorkflowId, company_id: CompanyId, phase_id: PhaseId) -> None:
        """Create Evaluation workflow with 6 stages per WORKFLOW3.md"""
        workflow = Workflow.create(
            id=workflow_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=company_id,
            name="Evaluation Workflow",
            description="Interview and assessment process",
            display=WorkflowDisplayEnum.KANBAN,
            phase_id=phase_id,
            is_default=True
        )
        workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("HR Interview", "Human Resources interview", WorkflowStageTypeEnum.INITIAL, 0,
             WorkflowStageStyle(icon="👥", text_color="#92400e", background_color="#fef3c7")),  # amber
            ("Manager Interview", "Manager interview", WorkflowStageTypeEnum.PROGRESS, 1,
             WorkflowStageStyle(icon="💼", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Assessment Test", "Technical or skills assessment", WorkflowStageTypeEnum.PROGRESS, 2,
             WorkflowStageStyle(icon="📝", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Executive Interview", "Executive level interview", WorkflowStageTypeEnum.PROGRESS, 3,
             WorkflowStageStyle(icon="🎯", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Selected", "Candidate selected for offer", WorkflowStageTypeEnum.SUCCESS, 4,
             WorkflowStageStyle(icon="✅", text_color="#065f46", background_color="#d1fae5")),  # green
            ("Rejected", "Candidate rejected", WorkflowStageTypeEnum.FAIL, 5,
             WorkflowStageStyle(icon="❌", text_color="#991b1b", background_color="#fee2e2")),  # red
        ]
        for name, desc, stage_type, order, style in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(),
                workflow_id=workflow_id,
                name=name,
                description=desc,
                stage_type=stage_type,
                order=order,
                allow_skip=False,
                is_active=True,
                style=style,
                validation_rules=None,
                recommended_rules=None
            )
            self.stage_repository.save(stage)

    def _create_offer_workflow(self, workflow_id: WorkflowId, company_id: CompanyId, phase_id: PhaseId) -> None:
        """Create Offer and Pre-Onboarding workflow with 5 stages per WORKFLOW3.md"""
        workflow = Workflow.create(
            id=workflow_id,
            workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION,
            company_id=company_id,
            name="Offer and Pre-Onboarding Workflow",
            description="Offer negotiation and document verification",
            display=WorkflowDisplayEnum.LIST,
            phase_id=phase_id,
            is_default=True
        )
        workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("Offer Proposal", "Offer proposed to candidate", WorkflowStageTypeEnum.INITIAL, 0,
             WorkflowStageStyle(icon="💌", text_color="#92400e", background_color="#fef3c7")),  # amber
            ("Negotiation", "Negotiating offer terms", WorkflowStageTypeEnum.PROGRESS, 1,
             WorkflowStageStyle(icon="🤝", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Document Submission", "Candidate submitting documents", WorkflowStageTypeEnum.PROGRESS, 2,
             WorkflowStageStyle(icon="📄", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Document Verification", "Verifying submitted documents", WorkflowStageTypeEnum.SUCCESS, 3,
             WorkflowStageStyle(icon="✅", text_color="#065f46", background_color="#d1fae5")),  # green
            ("Lost", "Candidate declined or withdrew", WorkflowStageTypeEnum.FAIL, 4,
             WorkflowStageStyle(icon="❌", text_color="#991b1b", background_color="#fee2e2")),  # red
        ]
        for name, desc, stage_type, order, style in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(),
                workflow_id=workflow_id,
                name=name,
                description=desc,
                stage_type=stage_type,
                order=order,
                allow_skip=False,
                is_active=True,
                style=style,
                validation_rules=None,
                recommended_rules=None
            )
            self.stage_repository.save(stage)

    def _update_success_stage_next_phase(self, workflow_id: WorkflowId, next_phase_id: PhaseId) -> None:
        """Update the SUCCESS stage of a workflow to set next_phase_id"""
        stages = self.stage_repository.list_by_workflow(workflow_id)

        for stage in stages:
            if stage.stage_type == WorkflowStageTypeEnum.SUCCESS:
                # Update stage with next_phase_id using update method
                stage.update(
                    name=stage.name,
                    description=stage.description,
                    stage_type=stage.stage_type,
                    allow_skip=stage.allow_skip,
                    estimated_duration_days=stage.estimated_duration_days,
                    default_role_ids=stage.default_role_ids,
                    default_assigned_users=stage.default_assigned_users,
                    email_template_id=stage.email_template_id,
                    custom_email_text=stage.custom_email_text,
                    deadline_days=stage.deadline_days,
                    estimated_cost=stage.estimated_cost,
                    next_phase_id=next_phase_id,
                    kanban_display=stage.kanban_display
                )
                self.stage_repository.save(stage)
                break

    def _create_job_position_workflow(self, workflow_id: WorkflowId, company_id: CompanyId, phase_id: PhaseId) -> None:
        """Create workflow for Job Position Opening with stages covering the full lifecycle"""
        workflow = Workflow.create(
            id=workflow_id,
            workflow_type=WorkflowTypeEnum.JOB_POSITION_OPENING,
            company_id=company_id,
            name="Job Positions Workflow",
            description="Complete job position lifecycle from draft to published",
            display=WorkflowDisplayEnum.KANBAN,
            phase_id=phase_id,
            is_default=True
        )
        workflow.activate()
        self.workflow_repository.save(workflow)

        stages = [
            ("Draft", "Position being drafted", WorkflowStageTypeEnum.INITIAL, 0,
             WorkflowStageStyle(icon="📝", text_color="#92400e", background_color="#fef3c7")),  # amber
            ("Under Review", "Position under review", WorkflowStageTypeEnum.PROGRESS, 1,
             WorkflowStageStyle(icon="🔍", text_color="#1e40af", background_color="#dbeafe")),  # blue
            ("Approved", "Position approved", WorkflowStageTypeEnum.PROGRESS, 2,
             WorkflowStageStyle(icon="✅", text_color="#065f46", background_color="#d1fae5")),  # green
            ("Published", "Position is published", WorkflowStageTypeEnum.SUCCESS, 3,
             WorkflowStageStyle(icon="🌐", text_color="#065f46", background_color="#d1fae5")),  # green
            ("Closed", "Position closed", WorkflowStageTypeEnum.SUCCESS, 4,
             WorkflowStageStyle(icon="🔒", text_color="#6b7280", background_color="#f3f4f6")),  # gray
            ("Cancelled", "Position cancelled", WorkflowStageTypeEnum.FAIL, 5,
             WorkflowStageStyle(icon="❌", text_color="#991b1b", background_color="#fee2e2")),  # red
        ]
        for name, desc, stage_type, order, style in stages:
            stage = WorkflowStage.create(
                id=WorkflowStageId.generate(),
                workflow_id=workflow_id,
                name=name,
                description=desc,
                stage_type=stage_type,
                order=order,
                allow_skip=False,
                is_active=True,
                style=style,
                validation_rules=None,
                recommended_rules=None
            )
            self.stage_repository.save(stage)
