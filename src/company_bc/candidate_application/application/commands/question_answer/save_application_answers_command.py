from dataclasses import dataclass
from typing import Dict, Any, List
import ulid

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.candidate_application.domain.entities.application_question_answer import (
    ApplicationQuestionAnswer
)
from src.company_bc.candidate_application.domain.repositories.application_question_answer_repository_interface import (
    ApplicationQuestionAnswerRepositoryInterface
)
from src.company_bc.candidate_application.domain.value_objects.application_question_answer_id import (
    ApplicationQuestionAnswerId
)
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import (
    CandidateApplicationId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class AnswerInput:
    """Input for a single question answer."""
    question_id: str
    answer_value: Any


@dataclass
class SaveApplicationAnswersCommand(Command):
    """
    Command to save question answers for an application.

    This command saves multiple answers at once, creating new answers
    or updating existing ones for the given application.
    """
    application_id: str
    answers: List[AnswerInput]


class SaveApplicationAnswersCommandHandler(CommandHandler[SaveApplicationAnswersCommand]):
    """Handler for SaveApplicationAnswersCommand."""

    def __init__(self, repository: ApplicationQuestionAnswerRepositoryInterface):
        self.repository = repository

    def execute(self, command: SaveApplicationAnswersCommand) -> None:
        """Execute the command - saves all answers for the application."""
        application_id = CandidateApplicationId(command.application_id)

        answers_to_save: List[ApplicationQuestionAnswer] = []

        for answer_input in command.answers:
            question_id = ApplicationQuestionId(answer_input.question_id)

            # Check if answer already exists
            existing = self.repository.get_by_application_and_question(
                application_id=application_id,
                question_id=question_id
            )

            if existing:
                # Update existing answer
                existing.update_answer(answer_input.answer_value)
                answers_to_save.append(existing)
            else:
                # Create new answer
                answer = ApplicationQuestionAnswer.create(
                    id=ApplicationQuestionAnswerId(str(ulid.new())),
                    application_id=application_id,
                    question_id=question_id,
                    answer_value=answer_input.answer_value
                )
                answers_to_save.append(answer)

        # Save all answers
        if answers_to_save:
            self.repository.save_many(answers_to_save)
