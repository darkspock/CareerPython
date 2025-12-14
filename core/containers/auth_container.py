"""Auth Container - Authentication and User Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.auth.controllers.user import UserController
from adapters.http.auth.invitations.controllers.invitation_controller import InvitationController
from adapters.http.candidate_app.controllers.registration_controller import RegistrationController

# Auth Infrastructure
from src.auth_bc.user.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from src.auth_bc.staff.infrastructure.repositories.staff_repository import SQLAlchemyStaffRepository
from src.auth_bc.user.infrastructure.repositories.user_asset_repository import SQLAlchemyUserAssetRepository
from src.auth_bc.user_registration.infrastructure.repositories import UserRegistrationRepository

# Auth Application Layer - Commands
from src.auth_bc.user.application.commands.create_user_command import CreateUserCommandHandler
from src.auth_bc.user.application.commands.create_user_automatically_command import CreateUserAutomaticallyCommandHandler
from src.auth_bc.user.application.commands.request_password_reset_command import RequestPasswordResetCommandHandler
from src.auth_bc.user.application import ResetPasswordWithTokenCommandHandler
from src.auth_bc.user.application import UpdateUserPasswordCommandHandler
from src.auth_bc.user.application import UpdateUserLanguageCommandHandler

# User Registration Commands
from src.auth_bc.user_registration.application.commands import (
    InitiateRegistrationCommandHandler,
    ProcessRegistrationPdfCommandHandler,
    SendVerificationEmailCommandHandler,
    VerifyRegistrationCommandHandler,
)
from src.auth_bc.user_registration.application.commands.cleanup_expired_registrations_command import (
    CleanupExpiredRegistrationsCommandHandler
)

# PDF Processing Service
from src.auth_bc.user.infrastructure.services.pdf_processing_service import PDFProcessingService

# Auth Application Layer - Queries
from src.auth_bc.user.application import AuthenticateUserQueryHandler
from src.auth_bc.user.application.queries.check_user_exists_query import CheckUserExistsQueryHandler
from src.auth_bc.user.application import CreateAccessTokenQueryHandler
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQueryHandler
from src.auth_bc.user.application.queries.get_user_language_query import GetUserLanguageQueryHandler
from src.auth_bc.user.application import GetUserByEmailQueryHandler
from src.auth_bc.user.application.queries.get_user_by_id_query import GetUserByIdQueryHandler


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

    user_registration_repository = providers.Factory(
        UserRegistrationRepository,
        session=shared.database.provided.session
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
        user_repository=user_repository,
        staff_repository=staff_repository
    )

    get_user_by_id_query_handler = providers.Factory(
        GetUserByIdQueryHandler,
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

    # PDF Processing Service
    pdf_processing_service = providers.Factory(PDFProcessingService)

    # User Registration Handlers
    initiate_registration_command_handler = providers.Factory(
        InitiateRegistrationCommandHandler,
        user_registration_repository=user_registration_repository,
        user_repository=user_repository,
        command_bus=shared.command_bus
    )

    process_registration_pdf_command_handler = providers.Factory(
        ProcessRegistrationPdfCommandHandler,
        user_registration_repository=user_registration_repository,
        pdf_processing_service=pdf_processing_service,
        ai_service=shared.ai_service
    )

    send_verification_email_command_handler = providers.Factory(
        SendVerificationEmailCommandHandler,
        user_registration_repository=user_registration_repository,
        command_bus=shared.command_bus
    )

    verify_registration_command_handler = providers.Factory(
        VerifyRegistrationCommandHandler,
        user_registration_repository=user_registration_repository,
        user_repository=user_repository,
        user_asset_repository=user_asset_repository,
        command_bus=shared.command_bus
    )

    cleanup_expired_registrations_command_handler = providers.Factory(
        CleanupExpiredRegistrationsCommandHandler,
        repository=user_registration_repository
    )

    # Registration Controller
    registration_controller = providers.Factory(
        RegistrationController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus,
        user_registration_repository=user_registration_repository
    )

