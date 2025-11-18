"""Company Container - Company Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.company_app.company.controllers.company_controller import CompanyController as CompanyManagementController
from adapters.http.company_app.company.controllers.company_user_controller import CompanyUserController
from adapters.http.company_app.company.controllers.company_role_controller import CompanyRoleController
from adapters.http.company_app.company_candidate.controllers.company_candidate_controller import CompanyCandidateController
from adapters.http.company_app.company.controllers.candidate_comment_controller import CandidateCommentController
from adapters.http.company_app.company.controllers.review_controller import ReviewController
from adapters.http.company_app.company.controllers.task_controller import TaskController
from adapters.http.company_app.company.controllers.email_template_controller import EmailTemplateController
from adapters.http.company_app.talent_pool.controllers.talent_pool_controller import TalentPoolController
from adapters.http.company_app.company_page.controllers.company_page_controller import CompanyPageController

# Company Infrastructure
from src.company_bc.company.infrastructure.repositories.company_repository import CompanyRepository
from src.company_bc.company.infrastructure.repositories.company_user_repository import CompanyUserRepository
from src.company_bc.company.infrastructure.repositories.company_user_invitation_repository import CompanyUserInvitationRepository
from src.company_bc.company_role.infrastructure.repositories.company_role_repository import CompanyRoleRepository
from src.company_bc.company_candidate.infrastructure.repositories.company_candidate_repository import CompanyCandidateRepository
from src.company_bc.company_candidate.infrastructure.repositories import CandidateCommentRepository
from src.company_bc.candidate_review.infrastructure.repositories.candidate_review_repository import CandidateReviewRepository

# Company Application Layer - Commands
from src.company_bc.company.application.commands.create_company_command import CreateCompanyCommandHandler
from src.company_bc.company.application.commands.register_company_with_user_command import RegisterCompanyWithUserCommandHandler
from src.company_bc.company.application.commands.link_user_to_company_command import LinkUserToCompanyCommandHandler
from src.company_bc.company.application.commands.update_company_command import UpdateCompanyCommandHandler
from src.company_bc.company.application.commands.initialize_sample_data_command import InitializeSampleDataCommandHandler
from src.company_bc.company.application.commands.initialize_onboarding_command import InitializeOnboardingCommandHandler
from src.company_bc.company.application.commands.upload_company_logo_command import UploadCompanyLogoCommandHandler
from src.company_bc.company.application.commands.suspend_company_command import SuspendCompanyCommandHandler
from src.company_bc.company.application.commands.activate_company_command import ActivateCompanyCommandHandler
from src.company_bc.company.application.commands.delete_company_command import DeleteCompanyCommandHandler
from src.company_bc.company.application.commands.delete_company_with_all_data_command import DeleteCompanyWithAllDataCommandHandler
from src.company_bc.company.application.commands.add_company_user_command import AddCompanyUserCommandHandler
from src.company_bc.company.application.commands.update_company_user_command import UpdateCompanyUserCommandHandler
from src.company_bc.company.application.commands.activate_company_user_command import ActivateCompanyUserCommandHandler
from src.company_bc.company.application.commands.deactivate_company_user_command import DeactivateCompanyUserCommandHandler
from src.company_bc.company.application.commands.remove_company_user_command import RemoveCompanyUserCommandHandler
from src.company_bc.company.application.commands.invite_company_user_command import InviteCompanyUserCommandHandler
from src.company_bc.company.application.commands.accept_user_invitation_command import AcceptUserInvitationCommandHandler
from src.company_bc.company.application.commands.assign_role_to_user_command import AssignRoleToUserCommandHandler

# Company Application Layer - Queries
from src.company_bc.company.application.queries.get_company_by_id import GetCompanyByIdQueryHandler
from src.company_bc.company.application.queries.get_company_by_domain import GetCompanyByDomainQueryHandler
from src.company_bc.company.application.queries.get_company_by_slug import GetCompanyBySlugQueryHandler
from src.company_bc.company.application.queries.list_companies import ListCompaniesQueryHandler
from src.company_bc.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQueryHandler
from src.company_bc.company.application.queries.get_company_user_by_company_and_user import GetCompanyUserByCompanyAndUserQueryHandler
from src.company_bc.company.application.queries.list_company_users_by_company import ListCompanyUsersByCompanyQueryHandler
from src.company_bc.company.application.queries.authenticate_company_user_query import AuthenticateCompanyUserQueryHandler
from src.company_bc.company.application.queries.get_user_invitation_query import GetUserInvitationQueryHandler
from src.company_bc.company.application.queries.get_user_permissions_query import GetUserPermissionsQueryHandler
from src.company_bc.company.application.queries.get_invitation_by_email_and_company_query import GetInvitationByEmailAndCompanyQueryHandler
from src.company_bc.company.application.queries.get_companies_stats import GetCompaniesStatsQueryHandler

# CompanyRole Application Layer
from src.company_bc.company_role.application import DeleteRoleCommandHandler, UpdateRoleCommandHandler, \
    ListRolesByCompanyQueryHandler, GetCompanyRoleByIdQueryHandler, CreateRoleCommandHandler

# CompanyCandidate Application Layer - Commands
from src.company_bc.company_candidate.application.commands.create_company_candidate_command import CreateCompanyCandidateCommandHandler
from src.company_bc.company_candidate.application.commands.update_company_candidate_command import UpdateCompanyCandidateCommandHandler
from src.company_bc.company_candidate.application.commands.confirm_company_candidate_command import ConfirmCompanyCandidateCommandHandler
from src.company_bc.company_candidate.application.commands.reject_company_candidate_command import RejectCompanyCandidateCommandHandler
from src.company_bc.company_candidate.application.commands.archive_company_candidate_command import ArchiveCompanyCandidateCommandHandler
from src.company_bc.company_candidate.application.commands.transfer_ownership_command import TransferOwnershipCommandHandler
from src.company_bc.company_candidate.application.commands.assign_workflow_command import AssignWorkflowCommandHandler
from src.company_bc.company_candidate.application.commands.change_stage_command import ChangeStageCommandHandler
from src.company_bc.company_candidate.application.commands.create_candidate_comment_command import CreateCandidateCommentCommandHandler
from src.company_bc.company_candidate.application.commands.update_candidate_comment_command import UpdateCandidateCommentCommandHandler
from src.company_bc.company_candidate.application.commands.delete_candidate_comment_command import DeleteCandidateCommentCommandHandler
from src.company_bc.company_candidate.application.commands.mark_comment_as_pending_command import MarkCommentAsPendingCommandHandler
from src.company_bc.company_candidate.application.commands.mark_comment_as_reviewed_command import MarkCandidateCommentAsReviewedCommandHandler

# CompanyCandidate Application Layer - Queries
from src.company_bc.company_candidate.application.queries.get_company_candidate_by_id import GetCompanyCandidateByIdQueryHandler
from src.company_bc.company_candidate.application.queries.get_company_candidate_by_id_with_candidate_info import GetCompanyCandidateByIdWithCandidateInfoQueryHandler
from src.company_bc.company_candidate.application.queries.get_company_candidate_by_company_and_candidate import GetCompanyCandidateByCompanyAndCandidateQueryHandler
from src.company_bc.company_candidate.application.queries.list_company_candidates_by_company import ListCompanyCandidatesByCompanyQueryHandler
from src.company_bc.company_candidate.application.queries.list_company_candidates_by_candidate import ListCompanyCandidatesByCandidateQueryHandler
from src.company_bc.company_candidate.application.queries.list_company_candidates_with_candidate_info import ListCompanyCandidatesWithCandidateInfoQueryHandler
from src.company_bc.company_candidate.application.queries.get_candidate_comment_by_id import GetCandidateCommentByIdQueryHandler
from src.company_bc.company_candidate.application.queries.list_candidate_comments_by_company_candidate import ListCandidateCommentsByCompanyCandidateQueryHandler
from src.company_bc.company_candidate.application.queries.list_candidate_comments_by_stage import ListCandidateCommentsByStageQueryHandler
from src.company_bc.company_candidate.application.queries.count_pending_comments_query import CountPendingCommentsQueryHandler

# CandidateReview Application Layer
from src.company_bc.candidate_review.application.commands.create_candidate_review_command import CreateCandidateReviewCommandHandler
from src.company_bc.candidate_review.application.commands.update_candidate_review_command import UpdateCandidateReviewCommandHandler
from src.company_bc.candidate_review.application.commands.delete_candidate_review_command import DeleteCandidateReviewCommandHandler
from src.company_bc.candidate_review.application.commands.mark_review_as_reviewed_command import MarkReviewAsReviewedCommandHandler
from src.company_bc.candidate_review.application.commands.mark_review_as_pending_command import MarkReviewAsPendingCommandHandler
from src.company_bc.candidate_review.application.queries.get_review_by_id_query import GetReviewByIdQueryHandler
from src.company_bc.candidate_review.application.queries.list_reviews_by_company_candidate_query import ListReviewsByCompanyCandidateQueryHandler
from src.company_bc.candidate_review.application.queries.list_reviews_by_stage_query import ListReviewsByStageQueryHandler
from src.company_bc.candidate_review.application.queries.list_global_reviews_query import ListGlobalReviewsQueryHandler


class CompanyContainer(containers.DeclarativeContainer):
    """Container para Company Bounded Context"""
    
    # Dependencias compartidas
    shared = providers.DependenciesContainer()
    
    # Repositories
    company_repository = providers.Factory(
        CompanyRepository,
        database=shared.database
    )
    
    company_user_repository = providers.Factory(
        CompanyUserRepository,
        database=shared.database
    )
    
    company_user_invitation_repository = providers.Factory(
        CompanyUserInvitationRepository,
        database=shared.database
    )
    
    company_role_repository = providers.Factory(
        CompanyRoleRepository,
        database=shared.database
    )
    
    company_candidate_repository = providers.Factory(
        CompanyCandidateRepository,
        database=shared.database
    )
    
    candidate_comment_repository = providers.Factory(
        CandidateCommentRepository,
        database=shared.database
    )
    
    candidate_review_repository = providers.Factory(
        CandidateReviewRepository,
        database=shared.database
    )
    
    # Company Query Handlers
    get_company_by_id_query_handler = providers.Factory(
        GetCompanyByIdQueryHandler,
        repository=company_repository
    )
    
    get_company_by_domain_query_handler = providers.Factory(
        GetCompanyByDomainQueryHandler,
        repository=company_repository
    )
    
    get_company_by_slug_query_handler = providers.Factory(
        GetCompanyBySlugQueryHandler,
        repository=company_repository
    )
    
    list_companies_query_handler = providers.Factory(
        ListCompaniesQueryHandler,
        repository=company_repository
    )
    
    get_company_user_by_id_query_handler = providers.Factory(
        GetCompanyUserByIdQueryHandler,
        repository=company_user_repository
    )
    
    get_company_user_by_company_and_user_query_handler = providers.Factory(
        GetCompanyUserByCompanyAndUserQueryHandler,
        repository=company_user_repository
    )
    
    list_company_users_by_company_query_handler = providers.Factory(
        ListCompanyUsersByCompanyQueryHandler,
        repository=company_user_repository
    )
    
    authenticate_company_user_query_handler = providers.Factory(
        AuthenticateCompanyUserQueryHandler,
        repository=company_user_repository
    )
    
    get_user_invitation_query_handler = providers.Factory(
        GetUserInvitationQueryHandler,
        repository=company_user_invitation_repository
    )
    
    get_user_permissions_query_handler = providers.Factory(
        GetUserPermissionsQueryHandler,
        company_user_repository=company_user_repository,
        company_role_repository=company_role_repository
    )
    
    get_invitation_by_email_and_company_query_handler = providers.Factory(
        GetInvitationByEmailAndCompanyQueryHandler,
        repository=company_user_invitation_repository
    )
    
    get_companies_stats_query_handler = providers.Factory(
        GetCompaniesStatsQueryHandler,
        repository=company_repository
    )
    
    # Company Command Handlers
    create_company_command_handler = providers.Factory(
        CreateCompanyCommandHandler,
        repository=company_repository,
        event_bus=shared.event_bus
    )
    
    register_company_with_user_command_handler = providers.Factory(
        RegisterCompanyWithUserCommandHandler,
        company_repository=company_repository,
        user_repository=shared.user_repository,
        company_user_repository=company_user_repository,
        event_bus=shared.event_bus,
        email_service=shared.email_service
    )
    
    link_user_to_company_command_handler = providers.Factory(
        LinkUserToCompanyCommandHandler,
        company_repository=company_repository,
        user_repository=shared.user_repository,
        company_user_repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    update_company_command_handler = providers.Factory(
        UpdateCompanyCommandHandler,
        repository=company_repository,
        event_bus=shared.event_bus
    )
    
    initialize_sample_data_command_handler = providers.Factory(
        InitializeSampleDataCommandHandler,
        company_repository=company_repository,
        workflow_repository=shared.workflow_repository,
        stage_repository=shared.workflow_stage_repository
    )
    
    initialize_onboarding_command_handler = providers.Factory(
        InitializeOnboardingCommandHandler,
        company_repository=company_repository,
        workflow_repository=shared.workflow_repository,
        stage_repository=shared.workflow_stage_repository
    )
    
    upload_company_logo_command_handler = providers.Factory(
        UploadCompanyLogoCommandHandler,
        repository=company_repository,
        storage_service=shared.storage_service,
        event_bus=shared.event_bus
    )
    
    suspend_company_command_handler = providers.Factory(
        SuspendCompanyCommandHandler,
        repository=company_repository,
        event_bus=shared.event_bus
    )
    
    activate_company_command_handler = providers.Factory(
        ActivateCompanyCommandHandler,
        repository=company_repository,
        event_bus=shared.event_bus
    )
    
    delete_company_command_handler = providers.Factory(
        DeleteCompanyCommandHandler,
        repository=company_repository,
        event_bus=shared.event_bus
    )
    
    delete_company_with_all_data_command_handler = providers.Factory(
        DeleteCompanyWithAllDataCommandHandler,
        company_repository=company_repository,
        job_position_repository=shared.job_position_repository,
        company_candidate_repository=company_candidate_repository,
        workflow_repository=shared.workflow_repository,
        stage_repository=shared.workflow_stage_repository,
        interview_repository=shared.interview_repository,
        event_bus=shared.event_bus
    )
    
    add_company_user_command_handler = providers.Factory(
        AddCompanyUserCommandHandler,
        company_repository=company_repository,
        user_repository=shared.user_repository,
        company_user_repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    update_company_user_command_handler = providers.Factory(
        UpdateCompanyUserCommandHandler,
        repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    activate_company_user_command_handler = providers.Factory(
        ActivateCompanyUserCommandHandler,
        repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    deactivate_company_user_command_handler = providers.Factory(
        DeactivateCompanyUserCommandHandler,
        repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    remove_company_user_command_handler = providers.Factory(
        RemoveCompanyUserCommandHandler,
        repository=company_user_repository,
        event_bus=shared.event_bus
    )
    
    invite_company_user_command_handler = providers.Factory(
        InviteCompanyUserCommandHandler,
        company_repository=company_repository,
        company_user_repository=company_user_repository,
        invitation_repository=company_user_invitation_repository,
        email_service=shared.email_service,
        event_bus=shared.event_bus
    )
    
    accept_user_invitation_command_handler = providers.Factory(
        AcceptUserInvitationCommandHandler,
        invitation_repository=company_user_invitation_repository,
        company_user_repository=company_user_repository,
        user_repository=shared.user_repository,
        event_bus=shared.event_bus
    )
    
    assign_role_to_user_command_handler = providers.Factory(
        AssignRoleToUserCommandHandler,
        company_user_repository=company_user_repository,
        company_role_repository=company_role_repository,
        event_bus=shared.event_bus
    )
    
    # CompanyRole Query Handlers
    list_roles_by_company_query_handler = providers.Factory(
        ListRolesByCompanyQueryHandler,
        repository=company_role_repository
    )
    
    get_company_role_by_id_query_handler = providers.Factory(
        GetCompanyRoleByIdQueryHandler,
        repository=company_role_repository
    )
    
    # CompanyRole Command Handlers
    create_role_command_handler = providers.Factory(
        CreateRoleCommandHandler,
        repository=company_role_repository,
        event_bus=shared.event_bus
    )
    
    update_role_command_handler = providers.Factory(
        UpdateRoleCommandHandler,
        repository=company_role_repository,
        event_bus=shared.event_bus
    )
    
    delete_role_command_handler = providers.Factory(
        DeleteRoleCommandHandler,
        repository=company_role_repository,
        event_bus=shared.event_bus
    )
    
    # CompanyCandidate Query Handlers
    get_company_candidate_by_id_query_handler = providers.Factory(
        GetCompanyCandidateByIdQueryHandler,
        repository=company_candidate_repository
    )
    
    get_company_candidate_by_id_with_candidate_info_query_handler = providers.Factory(
        GetCompanyCandidateByIdWithCandidateInfoQueryHandler,
        repository=company_candidate_repository,
        candidate_repository=shared.candidate_repository
    )
    
    get_company_candidate_by_company_and_candidate_query_handler = providers.Factory(
        GetCompanyCandidateByCompanyAndCandidateQueryHandler,
        repository=company_candidate_repository
    )
    
    list_company_candidates_by_company_query_handler = providers.Factory(
        ListCompanyCandidatesByCompanyQueryHandler,
        repository=company_candidate_repository
    )
    
    list_company_candidates_by_candidate_query_handler = providers.Factory(
        ListCompanyCandidatesByCandidateQueryHandler,
        repository=company_candidate_repository
    )
    
    list_company_candidates_with_candidate_info_query_handler = providers.Factory(
        ListCompanyCandidatesWithCandidateInfoQueryHandler,
        repository=company_candidate_repository,
        candidate_repository=shared.candidate_repository
    )
    
    get_candidate_comment_by_id_query_handler = providers.Factory(
        GetCandidateCommentByIdQueryHandler,
        repository=candidate_comment_repository
    )
    
    list_candidate_comments_by_company_candidate_query_handler = providers.Factory(
        ListCandidateCommentsByCompanyCandidateQueryHandler,
        repository=candidate_comment_repository
    )
    
    list_candidate_comments_by_stage_query_handler = providers.Factory(
        ListCandidateCommentsByStageQueryHandler,
        repository=candidate_comment_repository
    )
    
    count_pending_comments_query_handler = providers.Factory(
        CountPendingCommentsQueryHandler,
        repository=candidate_comment_repository
    )
    
    # CompanyCandidate Command Handlers
    create_company_candidate_command_handler = providers.Factory(
        CreateCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        candidate_repository=shared.candidate_repository,
        event_bus=shared.event_bus
    )
    
    update_company_candidate_command_handler = providers.Factory(
        UpdateCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        event_bus=shared.event_bus
    )
    
    confirm_company_candidate_command_handler = providers.Factory(
        ConfirmCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        event_bus=shared.event_bus
    )
    
    reject_company_candidate_command_handler = providers.Factory(
        RejectCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        event_bus=shared.event_bus
    )
    
    archive_company_candidate_command_handler = providers.Factory(
        ArchiveCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        event_bus=shared.event_bus
    )
    
    transfer_ownership_command_handler = providers.Factory(
        TransferOwnershipCommandHandler,
        repository=company_candidate_repository,
        event_bus=shared.event_bus
    )
    
    assign_workflow_command_handler = providers.Factory(
        AssignWorkflowCommandHandler,
        repository=company_candidate_repository,
        workflow_repository=shared.workflow_repository,
        event_bus=shared.event_bus
    )
    
    change_stage_command_handler = providers.Factory(
        ChangeStageCommandHandler,
        repository=company_candidate_repository,
        workflow_stage_repository=shared.workflow_stage_repository,
        interview_validation_service=shared.interview_validation_service,
        event_bus=shared.event_bus
    )
    
    create_candidate_comment_command_handler = providers.Factory(
        CreateCandidateCommentCommandHandler,
        repository=candidate_comment_repository,
        event_bus=shared.event_bus
    )
    
    update_candidate_comment_command_handler = providers.Factory(
        UpdateCandidateCommentCommandHandler,
        repository=candidate_comment_repository,
        event_bus=shared.event_bus
    )
    
    delete_candidate_comment_command_handler = providers.Factory(
        DeleteCandidateCommentCommandHandler,
        repository=candidate_comment_repository,
        event_bus=shared.event_bus
    )
    
    mark_comment_as_pending_command_handler = providers.Factory(
        MarkCommentAsPendingCommandHandler,
        repository=candidate_comment_repository,
        event_bus=shared.event_bus
    )
    
    mark_comment_as_reviewed_command_handler = providers.Factory(
        MarkCandidateCommentAsReviewedCommandHandler,
        repository=candidate_comment_repository,
        event_bus=shared.event_bus
    )
    
    # CandidateReview Query Handlers
    get_review_by_id_query_handler = providers.Factory(
        GetReviewByIdQueryHandler,
        repository=candidate_review_repository
    )
    
    list_reviews_by_company_candidate_query_handler = providers.Factory(
        ListReviewsByCompanyCandidateQueryHandler,
        repository=candidate_review_repository
    )
    
    list_reviews_by_stage_query_handler = providers.Factory(
        ListReviewsByStageQueryHandler,
        repository=candidate_review_repository
    )
    
    list_global_reviews_query_handler = providers.Factory(
        ListGlobalReviewsQueryHandler,
        repository=candidate_review_repository
    )
    
    # CandidateReview Command Handlers
    create_candidate_review_command_handler = providers.Factory(
        CreateCandidateReviewCommandHandler,
        repository=candidate_review_repository,
        event_bus=shared.event_bus
    )
    
    update_candidate_review_command_handler = providers.Factory(
        UpdateCandidateReviewCommandHandler,
        repository=candidate_review_repository,
        event_bus=shared.event_bus
    )
    
    delete_candidate_review_command_handler = providers.Factory(
        DeleteCandidateReviewCommandHandler,
        repository=candidate_review_repository,
        event_bus=shared.event_bus
    )
    
    mark_review_as_reviewed_command_handler = providers.Factory(
        MarkReviewAsReviewedCommandHandler,
        repository=candidate_review_repository,
        event_bus=shared.event_bus
    )
    
    mark_review_as_pending_command_handler = providers.Factory(
        MarkReviewAsPendingCommandHandler,
        repository=candidate_review_repository,
        event_bus=shared.event_bus
    )
    
    # Controllers
    company_controller = providers.Factory(
        CompanyManagementController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    company_user_controller = providers.Factory(
        CompanyUserController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    company_role_controller = providers.Factory(
        CompanyRoleController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    company_candidate_controller = providers.Factory(
        CompanyCandidateController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    candidate_comment_controller = providers.Factory(
        CandidateCommentController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    review_controller = providers.Factory(
        ReviewController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    task_controller = providers.Factory(
        TaskController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    email_template_controller = providers.Factory(
        EmailTemplateController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    talent_pool_controller = providers.Factory(
        TalentPoolController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    company_page_controller = providers.Factory(
        CompanyPageController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

