from dataclasses import dataclass

from core.event_bus import EventBus
from src.candidate.domain.events.candidate_experience_deleted_event import CandidateExperienceDeletedEvent
from src.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeleteExperienceCommand(Command):
    id: CandidateExperienceId


class DeleteExperienceCommandHandler(CommandHandler[DeleteExperienceCommand]):
    def __init__(self, experience_repository: CandidateExperienceRepositoryInterface, event_bus: EventBus):
        self.experience_repository = experience_repository
        self.event_bus = event_bus

    def execute(self, command: DeleteExperienceCommand) -> None:
        # Get experience to store candidate_id before deletion
        experience = self.experience_repository.get_by_id(command.id)
        if not experience:
            # Experience doesn't exist - operation is idempotent, just return
            return

        # Delete the experience
        deleted = self.experience_repository.delete(command.id)

        # Dispatch domain event if deletion was successful
        if deleted:
            self.event_bus.dispatch(CandidateExperienceDeletedEvent.create(id=command.id))
