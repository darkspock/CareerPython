"""
Command to evaluate application answers against automation rules.

This command:
1. Gets the application's question answers
2. Gets the automation rules from the workflow
3. Evaluates answers against rules using JsonLogic
4. Triggers auto-reject or auto-approve if configured
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.candidate_application.domain.repositories.application_question_answer_repository_interface import (
    ApplicationQuestionAnswerRepositoryInterface
)
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import (
    CandidateApplicationRepositoryInterface
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import (
    CandidateApplicationId
)
from src.company_bc.candidate_application.application.services.application_answer_evaluation_service import (
    ApplicationAnswerEvaluationService,
    AnswerEvaluationResult
)
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import (
    WorkflowRepositoryInterface
)
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import (
    JobPositionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId


@dataclass(frozen=True)
class EvaluationResultDto:
    """DTO for evaluation result."""
    is_valid: bool
    should_auto_reject: bool
    auto_reject_reason: Optional[str]
    should_auto_approve: bool
    auto_approve_reason: Optional[str]
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    action_taken: Optional[str]  # "rejected", "approved", or None


@dataclass
class EvaluateApplicationAnswersCommand(Command):
    """
    Command to evaluate application answers against automation rules.

    This is typically called after SaveApplicationAnswersCommand to check
    if any automation actions should be triggered.
    """
    application_id: str
    trigger_auto_actions: bool = True  # Whether to actually perform auto-reject/approve


class EvaluateApplicationAnswersCommandHandler(CommandHandler[EvaluateApplicationAnswersCommand]):
    """Handler for EvaluateApplicationAnswersCommand."""

    def __init__(
        self,
        answer_repository: ApplicationQuestionAnswerRepositoryInterface,
        application_repository: CandidateApplicationRepositoryInterface,
        question_repository: ApplicationQuestionRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface,
        job_position_repository: JobPositionRepositoryInterface
    ):
        self.answer_repository = answer_repository
        self.application_repository = application_repository
        self.question_repository = question_repository
        self.workflow_repository = workflow_repository
        self.job_position_repository = job_position_repository
        self.evaluation_service = ApplicationAnswerEvaluationService()

    def execute(self, command: EvaluateApplicationAnswersCommand) -> None:
        """
        Execute the command - evaluates answers and optionally triggers auto-actions.

        Note: This handler stores the evaluation result but doesn't return it.
        Use the EvaluateApplicationAnswersQuery to get the result without side effects.
        """
        application_id = CandidateApplicationId(command.application_id)

        # Get the application
        application = self.application_repository.get_by_id(application_id)
        if not application:
            return

        # Get the job position to find the workflow
        job_position = self.job_position_repository.get_by_id(application.job_position_id)
        if not job_position or not job_position.job_position_workflow_id:
            return

        workflow_id = WorkflowId(job_position.job_position_workflow_id.value)

        # Get the workflow to access automation rules
        workflow = self.workflow_repository.get_by_id(workflow_id)
        if not workflow:
            return

        # Get answers as dictionary
        answers = self.answer_repository.get_answers_as_dict(application_id)
        if not answers:
            return

        # Get questions for type metadata
        questions = self.question_repository.list_by_workflow(workflow_id, active_only=True)
        questions_metadata = [
            {
                "field_key": q.field_key,
                "field_type": q.field_type.value,
                "validation_rules": q.validation_rules
            }
            for q in questions
        ]

        # Prepare answers with type coercion
        prepared_answers = self.evaluation_service.get_answers_for_evaluation(
            answers,
            questions_metadata
        )

        # Collect all rules to evaluate
        all_rules = self._collect_rules(workflow, questions)

        if not all_rules:
            return

        # Get position data for comparisons
        position_data = self._get_position_data(job_position)

        # Evaluate answers against rules
        result = self.evaluation_service.evaluate_answers(
            prepared_answers,
            all_rules,
            position_data
        )

        # Trigger auto-actions if enabled
        if command.trigger_auto_actions:
            if result.should_auto_reject:
                application.reject(notes=result.auto_reject_reason or "Auto-rejected by screening rules")
                self.application_repository.save(application)
            elif result.should_auto_approve:
                # For auto-approve, we might move to next stage or mark as reviewed
                # This depends on business logic - for now just log
                pass

    def _collect_rules(self, workflow: Any, questions: List[Any]) -> Optional[Dict[str, Any]]:
        """Collect all automation rules from workflow and questions."""
        all_rules: List[Dict[str, Any]] = []

        # Get workflow-level automation rules (if any exist on workflow entity)
        # Note: This would require adding an 'automation_rules' field to Workflow

        # Get question-level validation rules
        for question in questions:
            if question.validation_rules:
                # If the question has validation_rules, add them
                if "rules" in question.validation_rules:
                    for rule in question.validation_rules["rules"]:
                        # Ensure field is set
                        if "field" not in rule:
                            rule = dict(rule)
                            rule["field"] = question.field_key
                        all_rules.append(rule)
                else:
                    # Simple rule format - wrap it
                    all_rules.append({
                        "rule": question.validation_rules,
                        "field": question.field_key,
                        "message": f"Validation failed for {question.label}",
                        "severity": "error"
                    })

        if not all_rules:
            return None

        return {"rules": all_rules}

    def _get_position_data(self, job_position: Any) -> Dict[str, Any]:
        """Extract position data for rule comparisons."""
        position_data: Dict[str, Any] = {
            "id": str(job_position.id.value),
            "title": job_position.title if hasattr(job_position, 'title') else None,
        }

        # Include custom fields from position
        if hasattr(job_position, 'custom_fields_values') and job_position.custom_fields_values:
            position_data.update(job_position.custom_fields_values)

        return position_data
