"""User application module - exports queries and commands"""

# Commands
from .commands.reset_password_with_token_command import ResetPasswordWithTokenCommand, \
    ResetPasswordWithTokenCommandHandler
from .commands.update_user_language_command import UpdateUserLanguageCommand, UpdateUserLanguageCommandHandler
from .commands.update_user_password_command import UpdateUserPasswordCommand, UpdateUserPasswordCommandHandler
# Queries
from .queries.authenticate_user_query import AuthenticateUserQuery, AuthenticateUserQueryHandler
from .queries.create_access_token_query import CreateAccessTokenQuery, CreateAccessTokenQueryHandler
from .queries.get_user_by_email_query import GetUserByEmailQuery, GetUserByEmailQueryHandler

__all__ = [
    # Queries
    "AuthenticateUserQuery",
    "AuthenticateUserQueryHandler",
    "CreateAccessTokenQuery",
    "CreateAccessTokenQueryHandler",
    "GetUserByEmailQuery",
    "GetUserByEmailQueryHandler",
    # Commands
    "ResetPasswordWithTokenCommand",
    "ResetPasswordWithTokenCommandHandler",
    "UpdateUserPasswordCommand",
    "UpdateUserPasswordCommandHandler",
    "UpdateUserLanguageCommand",
    "UpdateUserLanguageCommandHandler",
]
