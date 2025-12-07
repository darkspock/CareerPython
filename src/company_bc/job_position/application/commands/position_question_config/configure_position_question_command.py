from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.job_position.domain.entities.position_question_config import (
    PositionQuestionConfig
)
from src.company_bc.job_position.domain.repositories.position_question_config_repository_interface import (
    PositionQuestionConfigRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.position_question_config_id import (
    PositionQuestionConfigId
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


@dataclass
class ConfigurePositionQuestionCommand(Command):
    """
    Command to configure a question for a specific position.

    This command creates or updates the position question config.
    If a config already exists for the position/question pair, it updates it.
    Otherwise, it creates a new config.
    """
    position_id: str
    question_id: str
    enabled: bool
    is_required_override: Optional[bool] = None
    sort_order_override: Optional[int] = None


class ConfigurePositionQuestionCommandHandler(CommandHandler[ConfigurePositionQuestionCommand]):
    """Handler for ConfigurePositionQuestionCommand."""

    def __init__(self, repository: PositionQuestionConfigRepositoryInterface):
        self.repository = repository

    def execute(self, command: ConfigurePositionQuestionCommand) -> None:
        """Execute the command - creates or updates the config."""
        position_id = JobPositionId(command.position_id)
        question_id = ApplicationQuestionId(command.question_id)

        # Check if config already exists
        existing = self.repository.get_by_position_and_question(position_id, question_id)

        if existing:
            # Update existing config
            existing.update(
                enabled=command.enabled,
                is_required_override=command.is_required_override,
                sort_order_override=command.sort_order_override
            )
            self.repository.save(existing)
        else:
            # Create new config
            import ulid
            config = PositionQuestionConfig.create(
                id=PositionQuestionConfigId(str(ulid.new())),
                position_id=position_id,
                question_id=question_id,
                enabled=command.enabled,
                is_required_override=command.is_required_override,
                sort_order_override=command.sort_order_override
            )
            self.repository.save(config)
