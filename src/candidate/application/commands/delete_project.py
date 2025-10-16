from dataclasses import dataclass

from core.event_bus import EventBus
from src.candidate.domain.events.candidate_project_deleted_event import CandidateProjectDeletedEvent
from src.candidate.domain.repositories.candidate_project_repository_interface import CandidateProjectRepositoryInterface
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeleteProjectCommand(Command):
    id: CandidateProjectId


class DeleteProjectCommandHandler(CommandHandler[DeleteProjectCommand]):
    def __init__(self, project_repository: CandidateProjectRepositoryInterface, event_bus: EventBus):
        self.project_repository = project_repository
        self.event_bus = event_bus

    def execute(self, command: DeleteProjectCommand) -> None:
        project = self.project_repository.get_by_id(command.id)
        if not project:
            # Project doesn't exist - operation is idempotent, just return
            return

        # Delete the project
        deleted = self.project_repository.delete(command.id)
        if deleted:
            self.event_bus.dispatch(CandidateProjectDeletedEvent.create(id=command.id))
