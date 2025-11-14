import logging
from dataclasses import dataclass

from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.exceptions.user_exceptions import EmailAlreadyExistException
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.framework.application.command_bus import Command, CommandHandler

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUserCommand(Command):
    """Command to create a new user"""
    id: UserId
    email: str
    password: str
    is_active: bool = True


class CreateUserCommandHandler(CommandHandler[CreateUserCommand]):
    """Handler for creating a new user"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, command: CreateUserCommand) -> None:
        """
        Handle user creation

        Note: This is a command handler, so it doesn't return data.
        Use queries to retrieve the created user data.
        """
        log.info(f"CreateUserCommand called with email: {command.email}")

        try:
            # Check if user already exists
            existing_user = self.user_repository.get_by_email(command.email)
            if existing_user:
                raise EmailAlreadyExistException(command.email)

            # Hash password
            hashed_password = PasswordService.hash_password(command.password)

            user = User(id=command.id, email=command.email, hashed_password=hashed_password,
                        is_active=command.is_active)
            # Create user
            self.user_repository.create(user)
            log.info(f"User created successfully with email: {command.email}")

        except Exception as e:
            log.error(f"Error in CreateUserCommand: {str(e)}")
            raise
