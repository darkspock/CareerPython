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

        # Evaluate killer questions from job position
        killer_rejection_reason = None
        if job_position.killer_questions:
            killer_rejection_reason = self._evaluate_killer_questions(
                job_position.killer_questions,
                prepared_answers
            )

        # Trigger auto-actions if enabled
        if command.trigger_auto_actions:
            # Killer question rejection takes priority
            if killer_rejection_reason:
                application.reject(notes=killer_rejection_reason)
                self.application_repository.save(application)
            elif result.should_auto_reject:
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

    def _evaluate_killer_questions(
        self,
        killer_questions: List[Dict[str, Any]],
        answers: Dict[str, Any]
    ) -> Optional[str]:
        """
        Evaluate answers against killer questions.

        Returns the rejection reason if a killer question was answered incorrectly,
        or None if all answers are acceptable.

        Killer questions have the format:
        {
            "name": str,
            "description": str,
            "data_type": str,  # "boolean", "single_choice", etc.
            "is_killer": bool,
            "scoring_values": [
                {"label": str, "value": any, "scoring": int, "is_disqualifying": bool}
            ],
            "correct_answer": any  # For simple boolean killer questions
        }
        """
        for kq in killer_questions:
            if not kq.get("is_killer", False):
                continue

            question_name = kq.get("name", "")
            # Try to find the answer by question name (normalized as field key)
            field_key = question_name.lower().replace(" ", "_")

            # Check various possible keys
            answer = answers.get(field_key) or answers.get(question_name)
            if answer is None:
                continue

            # Check if answer is disqualifying
            data_type = kq.get("data_type", "")

            if data_type == "boolean":
                # For boolean killer questions, check correct_answer
                correct_answer = kq.get("correct_answer")
                if correct_answer is not None and answer != correct_answer:
                    return f"Disqualified: Answer to '{question_name}' does not meet requirements"

            # Check scoring_values for disqualifying answers
            scoring_values = kq.get("scoring_values", [])
            for sv in scoring_values:
                sv_value = sv.get("value")
                is_disqualifying = sv.get("is_disqualifying", False)

                # Match the answer
                if sv_value is not None and str(answer).lower() == str(sv_value).lower():
                    if is_disqualifying:
                        return f"Disqualified: Answer to '{question_name}' is disqualifying"
                    break

                # Also check by label for text-based answers
                sv_label = sv.get("label", "")
                if sv_label and str(answer).lower() == sv_label.lower():
                    if is_disqualifying:
                        return f"Disqualified: Answer to '{question_name}' is disqualifying"
                    break

        return None

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
