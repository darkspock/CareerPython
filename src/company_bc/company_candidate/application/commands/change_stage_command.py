from dataclasses import dataclass
from typing import Optional, List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.company_candidate.domain.exceptions import CompanyCandidateNotFoundError
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.framework.application.command_bus import Command, CommandHandler, CommandBus
from src.interview_bc.interview.application.commands.create_interview import CreateInterviewCommand
from src.interview_bc.interview.domain.enums.interview_enums import InterviewModeEnum
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.shared_bc.customization.field_validation.application.services.interview_validation_service import \
    InterviewValidationService
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.entities.workflow_stage import WorkflowStage
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.services.stage_phase_validation_service import \
    StagePhaseValidationService
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class ChangeStageCommand(Command):
    """Command to change the workflow stage of a company candidate"""
    id: CompanyCandidateId
    new_stage_id: WorkflowStageId


class ChangeStageCommandHandler(CommandHandler[ChangeStageCommand]):
    """Handler for changing the workflow stage of a company candidate with automatic phase transition support"""

    def __init__(
            self,
            repository: CompanyCandidateRepositoryInterface,
            workflow_stage_repository: WorkflowStageRepositoryInterface,
            workflow_repository: WorkflowRepositoryInterface,
            validation_service: StagePhaseValidationService,
            interview_validation_service: InterviewValidationService,
            candidate_application_repository: CandidateApplicationRepositoryInterface,
            interview_template_repository: InterviewTemplateRepositoryInterface,
            command_bus: CommandBus
    ):
        self._repository = repository
        self._workflow_stage_repository = workflow_stage_repository
        self._workflow_repository = workflow_repository
        self._validation_service = validation_service
        self._interview_validation_service = interview_validation_service
        self._candidate_application_repository = candidate_application_repository
        self._interview_template_repository = interview_template_repository
        self._command_bus = command_bus

    def execute(self, command: ChangeStageCommand) -> None:
        """Handle the change stage command with automatic phase transition
        
        If the target stage is SUCCESS and has a next_phase_id configured,
        automatically transitions the candidate to the next phase.
        """
        # Get existing company candidate
        company_candidate_id = command.id
        company_candidate = self._repository.get_by_id(company_candidate_id)

        if not company_candidate:
            raise CompanyCandidateNotFoundError(f"Company candidate with id {command.id} not found")

        # Get the target workflow stage
        target_stage = self._workflow_stage_repository.get_by_id(command.new_stage_id)
        if not target_stage:
            raise ValueError(f"Stage {command.new_stage_id.value} not found")

        # Validate no pending interviews in current stage before allowing stage change
        current_stage_id = company_candidate.current_stage_id
        if current_stage_id:
            candidate_id = CandidateId.from_string(company_candidate.candidate_id.value)
            has_pending = self._interview_validation_service.has_pending_interviews(
                candidate_id=candidate_id,
                workflow_stage_id=current_stage_id
            )
            if has_pending:
                pending_count = self._interview_validation_service.get_pending_interviews_count(
                    candidate_id=candidate_id,
                    workflow_stage_id=current_stage_id
                )
                raise ValueError(
                    f"Cannot change stage: There are {pending_count} pending interview(s) in the current stage. "
                    "Please complete or cancel all pending interviews before changing stages."
                )

        # Validate workflow has phase_id using Domain Service
        try:
            target_phase_id = self._validation_service.validate_workflow_has_phase(target_stage.workflow_id)
        except ValueError as e:
            raise ValueError(f"Cannot change stage: {e}")

        # Get the workflow of the target stage (already validated by Domain Service)
        # target_workflow = self._workflow_repository.get_by_id(target_stage.workflow_id)  # Not used currently

        # Check if the target stage belongs to a different phase than the candidate's current phase
        # If so, update phase_id and workflow_id as well
        # target_phase_id was already validated and obtained from Domain Service above
        current_phase_id = PhaseId.from_string(company_candidate.phase_id) if company_candidate.phase_id else None

        # Change stage (and phase/workflow if needed)
        if target_phase_id and (not current_phase_id or current_phase_id.value != target_phase_id.value):
            # The target stage belongs to a different phase, update phase_id and workflow_id
            updated_candidate = company_candidate.assign_workflow(
                workflow_id=target_stage.workflow_id,
                initial_stage_id=command.new_stage_id,
                phase_id=target_phase_id
            )
        else:
            # Same phase, just change the stage
            updated_candidate = company_candidate.change_stage(new_stage_id=command.new_stage_id)

        # Check if this is a SUCCESS stage with next_phase_id configured
        if target_stage.stage_type == WorkflowStageTypeEnum.SUCCESS and target_stage.next_phase_id:
            # Get workflows for the next phase (filter by CANDIDATE_APPLICATION type)
            next_phase_workflows = self._workflow_repository.list_by_phase_id(
                target_stage.next_phase_id,
                workflow_type=WorkflowTypeEnum.CANDIDATE_APPLICATION
            )

            if not next_phase_workflows:
                # No workflow found for next phase, just update the stage
                self._repository.save(updated_candidate)
                return

            # Use the first workflow (or default if available)
            next_phase_workflow = next((w for w in next_phase_workflows if w.is_default), None) or next_phase_workflows[
                0]

            # Get the initial stage of the next phase's workflow
            initial_stage = self._workflow_stage_repository.get_initial_stage(next_phase_workflow.id)
            if not initial_stage:
                # No initial stage found, just update the stage
                self._repository.save(updated_candidate)
                return

            # Automatically transition to the next phase
            # Use updated_candidate to preserve the stage change, then move to next phase
            updated_candidate = updated_candidate.move_to_next_phase(
                next_phase_id=target_stage.next_phase_id,
                next_workflow_id=next_phase_workflow.id,
                initial_stage_id=initial_stage.id
            )

        # Save to repository
        self._repository.save(updated_candidate)

        # Create interviews if the stage has interview configurations
        self._create_interviews_for_stage(
            candidate_id=company_candidate.candidate_id,
            stage=target_stage,
            company_id=company_candidate.company_id.value
        )

    def _create_interviews_for_stage(
            self,
            candidate_id: CandidateId,
            stage:WorkflowStage,
            company_id: str
    ) -> None:
        """
        Create interviews automatically for a stage if it has interview configurations.
        
        Args:
            candidate_id: ID of the candidate
            stage: WorkflowStage entity with interview configurations
            company_id: ID of the company
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"[AUTO INTERVIEW] Checking stage {stage.name} for interview configurations")
        
        # Check if stage has interview configurations
        if not stage.interview_configurations or len(stage.interview_configurations) == 0:
            logger.info(f"[AUTO INTERVIEW] No interview configurations found for stage {stage.name}")
            return

        logger.info(f"[AUTO INTERVIEW] Found {len(stage.interview_configurations)} interview configurations")

        # Get candidate applications to find job_position_id
        applications = self._candidate_application_repository.get_applications_by_candidate(candidate_id)
        
        if not applications:
            logger.warning(f"[AUTO INTERVIEW] No applications found for candidate {candidate_id.value}")
            return

        logger.info(f"[AUTO INTERVIEW] Found {len(applications)} applications for candidate")

        # Use the first active application's job_position_id
        # TODO: In the future, we might want to filter by active status or use a different strategy
        job_position_id = applications[0].job_position_id
        logger.info(f"[AUTO INTERVIEW] Using job_position_id: {job_position_id.value}")

        # Create interviews for each configuration
        for config in stage.interview_configurations:
            logger.info(f"[AUTO INTERVIEW] Processing config - template_id: {config.template_id}, mode: {config.mode}")
            
            # Only create interviews for AUTOMATIC mode
            if config.mode != InterviewModeEnum.AUTOMATIC:
                logger.info(f"[AUTO INTERVIEW] Skipping - mode is {config.mode}, not AUTOMATIC")
                continue

            # Get interview template to extract required information
            template = self._interview_template_repository.get_by_id(
                InterviewTemplateId.from_string(config.template_id)
            )
            
            if not template:
                logger.warning(f"[AUTO INTERVIEW] Template {config.template_id} not found")
                continue

            logger.info(f"[AUTO INTERVIEW] Template found: {template.name}")

            # Get default_role_ids from stage or use empty list
            required_roles = stage.default_role_ids if stage.default_role_ids else []
            
            if not required_roles:
                logger.warning(f"[AUTO INTERVIEW] No required roles defined for stage {stage.name}")
                continue

            logger.info(f"[AUTO INTERVIEW] Required roles: {required_roles}")

            # Create interview using command bus
            logger.info(f"[AUTO INTERVIEW] Creating interview with template {template.name}")
            
            create_interview_command = CreateInterviewCommand(
                candidate_id=candidate_id.value,
                job_position_id=job_position_id.value,
                workflow_stage_id=stage.id.value,
                interview_template_id=config.template_id,
                interview_mode=config.mode.value,
                required_roles=required_roles,
                title=template.name,
                description=template.intro,
                interview_type="CUSTOM",  # Default type
                created_by=company_id
            )

            logger.info(f"[AUTO INTERVIEW] Executing CreateInterviewCommand")
            
            try:
                # Execute command to create interview
                self._command_bus.execute(create_interview_command)
                logger.info(f"[AUTO INTERVIEW] Interview created successfully!")
            except Exception as e:
                logger.error(f"[AUTO INTERVIEW] Error creating interview: {e}", exc_info=True)
