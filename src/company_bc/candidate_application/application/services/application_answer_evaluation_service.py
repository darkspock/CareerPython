"""
Service for evaluating application question answers against automation rules.

This service uses JsonLogic to evaluate candidate answers and determine:
- Whether the application should be auto-rejected
- Whether the application should be auto-approved
- Validation warnings/errors to display
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.shared_bc.customization.field_validation.domain.services.jsonlogic_evaluator import (
    jsonlogic_apply
)


@dataclass(frozen=True)
class EvaluationIssue:
    """Represents an issue found during answer evaluation."""
    field_key: str
    message: str
    severity: str  # "error" or "warning"
    rule_id: Optional[str] = None


@dataclass(frozen=True)
class AnswerEvaluationResult:
    """Result of evaluating application answers against automation rules."""
    is_valid: bool
    should_auto_reject: bool
    auto_reject_reason: Optional[str]
    should_auto_approve: bool
    auto_approve_reason: Optional[str]
    errors: List[EvaluationIssue]
    warnings: List[EvaluationIssue]


class ApplicationAnswerEvaluationService:
    """
    Service for evaluating application answers against automation rules.

    Rules can be defined at:
    1. Workflow level (validation_rules on the workflow)
    2. Question level (validation_rules on individual questions)
    3. Stage level (validation_rules on workflow stages)

    Rule format (JsonLogic structured):
    {
        "rules": [
            {
                "rule": {">=": [{"var": "expected_salary"}, {"var": "min_salary"}]},
                "field": "expected_salary",
                "message": "Expected salary is below our minimum",
                "severity": "error",  # or "warning"
                "auto_reject": false,
                "auto_approve": false
            }
        ]
    }

    Or simple JsonLogic format:
    {">=": [{"var": "expected_salary"}, 50000]}
    """

    def evaluate_answers(
        self,
        answers: Dict[str, Any],
        rules: Optional[Dict[str, Any]],
        position_data: Optional[Dict[str, Any]] = None
    ) -> AnswerEvaluationResult:
        """
        Evaluate application answers against automation rules.

        Args:
            answers: Dictionary mapping question field_key to answer values
            rules: JsonLogic rules to evaluate (structured or simple format)
            position_data: Optional position data for comparisons (e.g., salary ranges)

        Returns:
            AnswerEvaluationResult with validation status and any auto-actions
        """
        if not rules:
            return AnswerEvaluationResult(
                is_valid=True,
                should_auto_reject=False,
                auto_reject_reason=None,
                should_auto_approve=False,
                auto_approve_reason=None,
                errors=[],
                warnings=[]
            )

        # Merge answers with position data for evaluation
        # This allows rules like {">=": [{"var": "expected_salary"}, {"var": "position.max_salary"}]}
        evaluation_data = dict(answers)
        if position_data:
            evaluation_data["position"] = position_data

        errors: List[EvaluationIssue] = []
        warnings: List[EvaluationIssue] = []
        should_auto_reject = False
        auto_reject_reason: Optional[str] = None
        should_auto_approve = False
        auto_approve_reason: Optional[str] = None

        # Handle structured rules format
        if "rules" in rules and isinstance(rules["rules"], list):
            for rule_def in rules["rules"]:
                result = self._evaluate_single_rule(rule_def, evaluation_data)
                if result:
                    issue, is_auto_reject, reject_reason, is_auto_approve, approve_reason = result

                    if issue:
                        if issue.severity == "error":
                            errors.append(issue)
                        else:
                            warnings.append(issue)

                    if is_auto_reject:
                        should_auto_reject = True
                        auto_reject_reason = reject_reason

                    if is_auto_approve:
                        should_auto_approve = True
                        auto_approve_reason = approve_reason

        # Handle simple JsonLogic format (single rule that must be true)
        else:
            try:
                result = jsonlogic_apply(rules, evaluation_data)
                if not result:
                    errors.append(EvaluationIssue(
                        field_key="__all__",
                        message="Validation rule failed",
                        severity="error"
                    ))
            except Exception as e:
                errors.append(EvaluationIssue(
                    field_key="__all__",
                    message=f"Error evaluating rule: {str(e)}",
                    severity="error"
                ))

        is_valid = len(errors) == 0

        return AnswerEvaluationResult(
            is_valid=is_valid,
            should_auto_reject=should_auto_reject,
            auto_reject_reason=auto_reject_reason,
            should_auto_approve=should_auto_approve,
            auto_approve_reason=auto_approve_reason,
            errors=errors,
            warnings=warnings
        )

    def _evaluate_single_rule(
        self,
        rule_def: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Optional[tuple]:
        """
        Evaluate a single rule definition.

        Returns tuple of (issue, should_auto_reject, reject_reason, should_auto_approve, approve_reason)
        or None if rule passes.
        """
        rule = rule_def.get("rule")
        field = rule_def.get("field", "__unknown__")
        message = rule_def.get("message", "Validation failed")
        severity = rule_def.get("severity", "error")
        auto_reject = rule_def.get("auto_reject", False)
        auto_approve = rule_def.get("auto_approve", False)
        rule_id = rule_def.get("id")

        if not rule:
            return None

        try:
            result = jsonlogic_apply(rule, data)

            # Rule should evaluate to True to pass
            if result:
                # Rule passed - check for auto-approve
                if auto_approve:
                    return (None, False, None, True, message)
                return None

            # Rule failed
            issue = EvaluationIssue(
                field_key=field,
                message=self._format_message(message, field, data),
                severity=severity,
                rule_id=rule_id
            )

            reject_reason = self._format_message(message, field, data) if auto_reject else None

            return (issue, auto_reject, reject_reason, False, None)

        except Exception as e:
            # Error evaluating rule
            issue = EvaluationIssue(
                field_key=field,
                message=f"Error evaluating rule: {str(e)}",
                severity="error",
                rule_id=rule_id
            )
            return (issue, False, None, False, None)

    def _format_message(
        self,
        message: str,
        field: str,
        data: Dict[str, Any]
    ) -> str:
        """Format message template with actual values."""
        try:
            # Replace common placeholders
            formatted = message.replace("{field}", field)

            # Replace {var_name} with actual values from data
            for key, value in data.items():
                if isinstance(value, dict):
                    # Handle nested data like position.max_salary
                    for nested_key, nested_value in value.items():
                        formatted = formatted.replace(
                            f"{{{key}.{nested_key}}}",
                            str(nested_value) if nested_value is not None else "N/A"
                        )
                else:
                    formatted = formatted.replace(
                        f"{{{key}}}",
                        str(value) if value is not None else "N/A"
                    )

            return formatted
        except Exception:
            return message

    def get_answers_for_evaluation(
        self,
        answers_dict: Dict[str, Any],
        questions_metadata: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Prepare answers for evaluation with type coercion.

        Converts string answers to appropriate types based on question metadata.
        """
        if not questions_metadata:
            return answers_dict

        result = dict(answers_dict)

        # Build field_key -> question mapping
        question_map = {q.get("field_key"): q for q in questions_metadata if q.get("field_key")}

        for field_key, value in list(result.items()):
            question = question_map.get(field_key)
            if not question:
                continue

            field_type = question.get("field_type", "TEXT")

            # Type coercion based on field type
            if field_type == "NUMBER" and isinstance(value, str):
                try:
                    result[field_key] = float(value) if "." in value else int(value)
                except ValueError:
                    pass
            elif field_type == "BOOLEAN" and isinstance(value, str):
                result[field_key] = value.lower() in ("true", "yes", "1", "si", "sí")

        return result
