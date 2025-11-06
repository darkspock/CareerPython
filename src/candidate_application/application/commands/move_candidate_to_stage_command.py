"""Move candidate to workflow stage with automatic phase transition support

Phase 12.12: This command handles moving candidates through workflow stages and
automatically transitions them to the next phase when they reach a SUCCESS stage.
"""
from dataclasses import dataclass
from typing import Optional

from src.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.candidate_stage.domain.entities.candidate_stage import CandidateStage
from src.candidate_stage.domain.infrastructure.candidate_stage_repository_interface import \
    CandidateStageRepositoryInterface
from src.candidate_stage.domain.value_objects.candidate_stage_id import CandidateStageId
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class MoveCandidateToStageCommand(Command):
    """Command to move a candidate application to a new workflow stage

    Phase 12.12: This command handles stage transitions and automatically
    triggers phase transitions when the target stage is of type SUCCESS.
    """
    application_id: str
    new_stage_id: str
    time_limit_hours: Optional[int] = None
    changed_by: Optional[str] = None
    comments: Optional[str] = None


class MoveCandidateToStageCommandHandler(CommandHandler[MoveCandidateToStageCommand]):
    """Handler for moving candidates through workflow stages with automatic phase transitions"""

    def __init__(
            self,
            candidate_application_repository: CandidateApplicationRepositoryInterface,
            candidate_stage_repository: CandidateStageRepositoryInterface,
            workflow_stage_repository: WorkflowStageRepositoryInterface,
            job_position_repository: JobPositionRepositoryInterface
    ):
        self.candidate_application_repository = candidate_application_repository
        self.candidate_stage_repository = candidate_stage_repository
        self.workflow_stage_repository = workflow_stage_repository
        self.job_position_repository = job_position_repository

    def execute(self, command: MoveCandidateToStageCommand) -> None:
        """Execute stage transition with automatic phase transition support

        Phase 12.12: When moving to a SUCCESS stage that has a next_phase_id configured,
        this will automatically transition the candidate to the next phase.
        """
        # 1. Get the candidate application
        application = self.candidate_application_repository.get_by_id(
            CandidateApplicationId.from_string(command.application_id)
        )
        if not application:
            raise ValueError(f"Application {command.application_id} not found")

        # 2. Get the target workflow stage
        target_stage = self.workflow_stage_repository.get_by_id(
            WorkflowStageId.from_string(command.new_stage_id)
        )
        if not target_stage:
            raise ValueError(f"Stage {command.new_stage_id} not found")

        # 3. Complete the current candidate_stage record (if exists)
        current_stage_record = self.candidate_stage_repository.get_current_stage(
            application.id
        )
        if current_stage_record:
            completed_stage = current_stage_record.complete(comments=command.comments)
            self.candidate_stage_repository.save(completed_stage)

        # 4. Move the application to the new stage
        application.move_to_stage(
            new_stage_id=command.new_stage_id,
            time_limit_hours=command.time_limit_hours,
            changed_by=command.changed_by
        )

        # 5. Create new candidate_stage record for the new stage
        new_stage_record = CandidateStage.create(
            id=CandidateStageId.generate(),
            candidate_application_id=application.id,
            phase_id=PhaseId.from_string(application.current_phase_id) if application.current_phase_id else None,
            workflow_id=CompanyWorkflowId.from_string(target_stage.workflow_id.value),
            stage_id=WorkflowStageId.from_string(command.new_stage_id),
            deadline=application.stage_deadline,
            estimated_cost=target_stage.estimated_cost,
            comments=command.comments
        )
        self.candidate_stage_repository.save(new_stage_record)

        # 6. Phase 12.12: Check if this is a SUCCESS stage with next_phase_id
        if target_stage.stage_type == StageType.SUCCESS and target_stage.next_phase_id:
            # Get the job position to determine the workflow for the next phase
            job_position = self.job_position_repository.get_by_id(application.job_position_id)
            if not job_position:
                raise ValueError(f"Job position {application.job_position_id.value} not found")

            # Get the workflow configured for the next phase
            next_phase_workflow_id = job_position.get_workflow_for_phase(target_stage.next_phase_id)
            if not next_phase_workflow_id:
                raise ValueError(
                    f"No workflow configured for phase {target_stage.next_phase_id} "
                    f"in position {job_position.id.value}"
                )

            # Get the initial stage of the next phase's workflow
            next_workflow_stages = self.workflow_stage_repository.list_by_workflow(
                CompanyWorkflowId.from_string(next_phase_workflow_id)
            )
            initial_stage = next((s for s in next_workflow_stages if s.stage_type == StageType.INITIAL), None)
            if not initial_stage:
                raise ValueError(f"No INITIAL stage found in workflow {next_phase_workflow_id}")

            # Automatically transition to the next phase
            application.move_to_next_phase(
                next_phase_id=target_stage.next_phase_id,
                initial_stage_id=initial_stage.id.value,
                time_limit_hours=initial_stage.deadline_days * 24 if initial_stage.deadline_days else None
            )

            # Create candidate_stage record for the new phase's initial stage
            next_phase_stage_record = CandidateStage.create(
                id=CandidateStageId.generate(),
                candidate_application_id=application.id,
                phase_id=PhaseId.from_string(target_stage.next_phase_id),
                workflow_id=CompanyWorkflowId.from_string(next_phase_workflow_id),
                stage_id=initial_stage.id,
                deadline=application.stage_deadline,
                estimated_cost=initial_stage.estimated_cost,
                comments=f"Auto-transitioned from phase {application.current_phase_id}"
            )
            self.candidate_stage_repository.save(next_phase_stage_record)

        # 7. Save the updated application
        self.candidate_application_repository.save(application)
