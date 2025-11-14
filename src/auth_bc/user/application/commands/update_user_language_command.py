from dataclasses import dataclass

from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class UpdateUserLanguageCommand(Command):
    """Command to update user's preferred language"""
    user_id: str
    language_code: str


class UpdateUserLanguageCommandHandler(CommandHandler[UpdateUserLanguageCommand]):
    """Handler for updating user's preferred language"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, command: UpdateUserLanguageCommand) -> None:
        """Execute the update user language command"""
        # Get user by ID
        user_id = UserId.from_string(command.user_id)
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError(f"User with id {command.user_id} not found")

        # Validate the language code using domain logic
        user.update_preferred_language(command.language_code)

        # Update the user using the repository interface
        user_data = {"preferred_language": command.language_code}
        self.user_repository.update(user_id, user_data)
