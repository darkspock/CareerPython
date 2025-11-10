from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.exceptions.user_exceptions import EmailAlreadyExistException
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId


@dataclass(frozen=True)
class CreateUserAutomaticallyCommand(Command):
    """Command to create a user automatically with random password"""
    id: UserId
    email: str


class CreateUserAutomaticallyCommandHandler(CommandHandler[CreateUserAutomaticallyCommand]):
    """Handler for creating a user automatically"""

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, command: CreateUserAutomaticallyCommand) -> None:
        """
            Create user automatically with random password for PDF upload users
            Returns user data and the plain password for email sending
            """
        existing_user = self.user_repository.get_by_email(command.email)
        if existing_user:
            raise EmailAlreadyExistException(command.email)

        plain_password = User.generate_random_password()
        # Hash the password using the same method as AuthUseCase
        hashed_password = PasswordService.hash_password(plain_password)

        user = User(
            id=command.id,
            email=command.email,
            hashed_password=hashed_password,
            is_active=True,

        )
        self.user_repository.create(user)
