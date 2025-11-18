"""Auth Container - Authentication and User Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.auth.controllers.user import UserController
from adapters.http.auth.invitations.controllers.invitation_controller import InvitationController

# Auth Infrastructure
from src.auth_bc.user.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from src.auth_bc.staff.infrastructure.repositories.staff_repository import SQLAlchemyStaffRepository
from src.auth_bc.user.infrastructure.repositories.user_asset_repository import SQLAlchemyUserAssetRepository

# Auth Application Layer - Commands
from src.auth_bc.user.application.commands.create_user_command import CreateUserCommandHandler
from src.auth_bc.user.application.commands.create_user_automatically_command import CreateUserAutomaticallyCommandHandler
from src.auth_bc.user.application import CreateUserFromLandingCommandHandler
from src.auth_bc.user.application.commands.request_password_reset_command import RequestPasswordResetCommandHandler
from src.auth_bc.user.application import ResetPasswordWithTokenCommandHandler
from src.auth_bc.user.application import UpdateUserPasswordCommandHandler
from src.auth_bc.user.application import UpdateUserLanguageCommandHandler

# Auth Application Layer - Queries
from src.auth_bc.user.application import AuthenticateUserQueryHandler
from src.auth_bc.user.application.queries.check_user_exists_query import CheckUserExistsQueryHandler
from src.auth_bc.user.application import CreateAccessTokenQueryHandler
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQueryHandler
from src.auth_bc.user.application.queries.get_user_language_query import GetUserLanguageQueryHandler
from src.auth_bc.user.application import GetUserByEmailQueryHandler


class AuthContainer(containers.DeclarativeContainer):
    """Container para Auth Bounded Context"""
    
    # Dependencias compartidas (se inyectarán desde MainContainer)
    shared = providers.DependenciesContainer()
    
    # Repositories
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        database=shared.database
    )
    
    staff_repository = providers.Factory(
        SQLAlchemyStaffRepository,
        database=shared.database
    )
    
    user_asset_repository = providers.Factory(
        SQLAlchemyUserAssetRepository,
        database=shared.database
    )
    
    # Query Handlers
    authenticate_user_query_handler = providers.Factory(
        AuthenticateUserQueryHandler,
        user_repository=user_repository
    )
    
    check_user_exists_query_handler = providers.Factory(
        CheckUserExistsQueryHandler,
        user_repository=user_repository
    )
    
    get_current_user_from_token_query_handler = providers.Factory(
        GetCurrentUserFromTokenQueryHandler,
        user_repository=user_repository
    )
    
    create_access_token_query_handler = providers.Factory(
        CreateAccessTokenQueryHandler
    )
    
    get_user_language_query_handler = providers.Factory(
        GetUserLanguageQueryHandler,
        user_repository=user_repository
    )
    
    get_user_by_email_query_handler = providers.Factory(
        GetUserByEmailQueryHandler,
        user_repository=user_repository
    )
    
    # Command Handlers
    create_user_command_handler = providers.Factory(
        CreateUserCommandHandler,
        user_repository=user_repository
    )
    
    create_user_automatically_command_handler = providers.Factory(
        CreateUserAutomaticallyCommandHandler,
        user_repository=user_repository
    )
    
    create_user_from_landing_command_handler = providers.Factory(
        CreateUserFromLandingCommandHandler,
        user_repository=user_repository
    )
    
    request_password_reset_command_handler = providers.Factory(
        RequestPasswordResetCommandHandler,
        user_repository=user_repository,
        email_service=shared.email_service
    )
    
    reset_password_with_token_command_handler = providers.Factory(
        ResetPasswordWithTokenCommandHandler,
        user_repository=user_repository
    )
    
    update_user_password_command_handler = providers.Factory(
        UpdateUserPasswordCommandHandler,
        user_repository=user_repository
    )
    
    update_user_language_command_handler = providers.Factory(
        UpdateUserLanguageCommandHandler,
        user_repository=user_repository
    )
    
    # Controllers
    user_controller = providers.Factory(
        UserController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    invitation_controller = providers.Factory(
        InvitationController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

