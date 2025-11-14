from dataclasses import dataclass

from core.event_bus import EventBus
from src.candidate_bc.candidate.domain.events.candidate_education_deleted_event import CandidateEducationDeletedEvent
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class DeleteEducationCommand(Command):
    id: CandidateEducationId


class DeleteEducationCommandHandler(CommandHandler[DeleteEducationCommand]):
    def __init__(self, education_repository: CandidateEducationRepositoryInterface, event_bus: EventBus):
        self.education_repository = education_repository
        self.event_bus = event_bus

    def execute(self, command: DeleteEducationCommand) -> None:
        education = self.education_repository.get_by_id(command.id)
        if not education:
            # Education doesn't exist - operation is idempotent, just return
            return

        # Delete the education
        deleted = self.education_repository.delete(command.id)
        if deleted:
            self.event_bus.dispatch(CandidateEducationDeletedEvent.create(id=command.id))
