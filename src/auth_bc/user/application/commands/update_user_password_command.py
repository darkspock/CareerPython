from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.auth_bc.user.domain.exceptions import UserNotFoundError
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass
class UpdateUserPasswordCommand(Command):
    """Command to update user password"""
    user_id: UserId
    new_password: str
    updated_by_admin_id: str


class UpdateUserPasswordCommandHandler(CommandHandler[UpdateUserPasswordCommand]):
    """Handler to update user password"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, command: UpdateUserPasswordCommand) -> None:
        """Update user password"""

        # Get the user
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(f"User with id {command.user_id.value} not found")

        # Hash the new password using PasswordService
        hashed_password = PasswordService.hash_password(command.new_password)

        # Update password using repository
        user_data = {"hashed_password": hashed_password}
        self.user_repository.update(command.user_id, user_data)
