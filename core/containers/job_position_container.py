"""Job Position Container - Job Position Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.admin_app.controllers import JobPositionController
from adapters.http.admin_app.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.company_app.job_position.controllers.public_position_controller import PublicPositionController
from adapters.http.company_app.position_stage_assignment.controllers.position_stage_assignment_controller import PositionStageAssignmentController
from adapters.http.company_app.job_position.controllers.position_question_config_controller import PositionQuestionConfigController

# Job Position Infrastructure
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import JobPositionRepository
from src.company_bc.job_position.infrastructure.repositories.job_position_comment_repository import JobPositionCommentRepository
from src.company_bc.job_position.infrastructure.repositories.job_position_activity_repository import JobPositionActivityRepository
from src.company_bc.job_position.infrastructure.repositories.job_position_stage_repository import JobPositionStageRepository
from src.company_bc.job_position.infrastructure.repositories.position_question_config_repository import PositionQuestionConfigRepository

# Job Position Application Layer - Commands
from src.company_bc.job_position.application.commands.create_job_position import CreateJobPositionCommandHandler
from src.company_bc.job_position.application.commands.update_job_position import UpdateJobPositionCommandHandler
from src.company_bc.job_position.application.commands.delete_job_position import DeleteJobPositionCommandHandler
from src.company_bc.job_position.application.commands.move_job_position_to_stage import MoveJobPositionToStageCommandHandler
from src.company_bc.job_position.application.commands.update_job_position_custom_fields import UpdateJobPositionCustomFieldsCommandHandler
from src.company_bc.job_position.application.commands.create_job_position_comment_command import CreateJobPositionCommentCommandHandler
from src.company_bc.job_position.application.commands.update_job_position_comment_command import UpdateJobPositionCommentCommandHandler
from src.company_bc.job_position.application.commands.delete_job_position_comment_command import DeleteJobPositionCommentCommandHandler
from src.company_bc.job_position.application.commands.mark_comment_as_reviewed_command import MarkJobPositionCommentAsReviewedCommandHandler
from src.company_bc.job_position.application.commands.mark_comment_as_pending_command import MarkJobPositionCommentAsPendingCommandHandler

# Position Question Config Commands
from src.company_bc.job_position.application.commands.position_question_config.configure_position_question_command import ConfigurePositionQuestionCommandHandler
from src.company_bc.job_position.application.commands.position_question_config.remove_position_question_config_command import RemovePositionQuestionConfigCommandHandler

# Job Position Application Layer - Queries
from src.company_bc.job_position.application.queries.list_job_positions import ListJobPositionsQueryHandler
from src.company_bc.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQueryHandler
from src.company_bc.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQueryHandler
from src.company_bc.job_position.application.queries.list_public_job_positions import ListPublicJobPositionsQueryHandler
from src.company_bc.job_position.application.queries.get_public_job_position import GetPublicJobPositionQueryHandler
from src.company_bc.job_position.application.queries.list_published_job_positions import ListPublishedJobPositionsQueryHandler
from src.company_bc.job_position.application.queries.get_job_position_workflow import GetJobPositionWorkflowQueryHandler
from src.company_bc.job_position.application.queries.list_job_position_workflows import ListJobPositionWorkflowsQueryHandler
from src.company_bc.job_position.application.queries.list_all_job_position_comments_query import ListAllJobPositionCommentsQueryHandler
from src.company_bc.job_position.application.queries.list_job_position_activities_query import ListJobPositionActivitiesQueryHandler

# Position Question Config Queries
from src.company_bc.job_position.application.queries.position_question_config.list_position_question_configs_query import ListPositionQuestionConfigsQueryHandler
from src.company_bc.job_position.application.queries.position_question_config.get_enabled_questions_for_position_query import GetEnabledQuestionsForPositionQueryHandler

# Position Stage Assignment
from src.company_bc.position_stage_assignment import (
    AssignUsersToStageCommandHandler,
    AddUserToStageCommandHandler,
    RemoveUserFromStageCommandHandler,
    CopyWorkflowAssignmentsCommandHandler,
    ListStageAssignmentsQueryHandler,
    GetAssignedUsersQueryHandler,
    PositionStageAssignmentRepository
)


class JobPositionContainer(containers.DeclarativeContainer):
    """Container para Job Position Bounded Context"""
    
    # Dependencias compartidas
    shared = providers.DependenciesContainer()
    
    # Repositories
    job_position_repository = providers.Factory(
        JobPositionRepository,
        database=shared.database
    )
    
    job_position_comment_repository = providers.Factory(
        JobPositionCommentRepository,
        database=shared.database
    )
    
    job_position_activity_repository = providers.Factory(
        JobPositionActivityRepository,
        database=shared.database
    )
    
    job_position_stage_repository = providers.Factory(
        JobPositionStageRepository,
        database=shared.database
    )
    
    position_stage_assignment_repository = providers.Factory(
        PositionStageAssignmentRepository,
        database=shared.database
    )

    position_question_config_repository = providers.Factory(
        PositionQuestionConfigRepository,
        database=shared.database
    )

    # Job Position Query Handlers
    list_job_positions_query_handler = providers.Factory(
        ListJobPositionsQueryHandler,
        job_position_repository=job_position_repository,
        job_position_comment_repository=job_position_comment_repository
    )
    
    get_job_position_by_id_query_handler = providers.Factory(
        GetJobPositionByIdQueryHandler,
        job_position_repository=job_position_repository
    )
    
    get_job_positions_stats_query_handler = providers.Factory(
        GetJobPositionsStatsQueryHandler,
        job_position_repository=job_position_repository
    )
    
    list_public_job_positions_query_handler = providers.Factory(
        ListPublicJobPositionsQueryHandler,
        job_position_repository=job_position_repository
    )
    
    get_public_job_position_query_handler = providers.Factory(
        GetPublicJobPositionQueryHandler,
        job_position_repository=job_position_repository
    )
    
    list_published_job_positions_query_handler = providers.Factory(
        ListPublishedJobPositionsQueryHandler,
        job_position_repository=job_position_repository
    )
    
    get_job_position_workflow_query_handler = providers.Factory(
        GetJobPositionWorkflowQueryHandler,
        workflow_repository=shared.workflow_repository
    )
    
    list_job_position_workflows_query_handler = providers.Factory(
        ListJobPositionWorkflowsQueryHandler,
        workflow_repository=shared.workflow_repository
    )
    
    list_all_job_position_comments_query_handler = providers.Factory(
        ListAllJobPositionCommentsQueryHandler,
        comment_repository=job_position_comment_repository
    )
    
    list_job_position_activities_query_handler = providers.Factory(
        ListJobPositionActivitiesQueryHandler,
        activity_repository=job_position_activity_repository
    )
    
    # Job Position Command Handlers
    create_job_position_command_handler = providers.Factory(
        CreateJobPositionCommandHandler,
        job_position_repository=job_position_repository
    )
    
    update_job_position_command_handler = providers.Factory(
        UpdateJobPositionCommandHandler,
        job_position_repository=job_position_repository
    )
    
    delete_job_position_command_handler = providers.Factory(
        DeleteJobPositionCommandHandler,
        job_position_repository=job_position_repository,
        candidate_application_repository=shared.candidate_application_repository
    )
    
    move_job_position_to_stage_command_handler = providers.Factory(
        MoveJobPositionToStageCommandHandler,
        job_position_repository=job_position_repository,
        workflow_repository=shared.workflow_repository,
        stage_repository=shared.workflow_stage_repository,
        job_position_stage_repository=job_position_stage_repository,
        activity_repository=job_position_activity_repository,
        validation_service=shared.stage_phase_validation_service
    )
    
    update_job_position_custom_fields_command_handler = providers.Factory(
        UpdateJobPositionCustomFieldsCommandHandler,
        job_position_repository=job_position_repository
    )
    
    create_job_position_comment_command_handler = providers.Factory(
        CreateJobPositionCommentCommandHandler,
        comment_repository=job_position_comment_repository,
        activity_repository=job_position_activity_repository,
        workflow_repository=shared.workflow_repository
    )
    
    update_job_position_comment_command_handler = providers.Factory(
        UpdateJobPositionCommentCommandHandler,
        comment_repository=job_position_comment_repository
    )
    
    delete_job_position_comment_command_handler = providers.Factory(
        DeleteJobPositionCommentCommandHandler,
        comment_repository=job_position_comment_repository
    )
    
    mark_job_position_comment_as_reviewed_command_handler = providers.Factory(
        MarkJobPositionCommentAsReviewedCommandHandler,
        comment_repository=job_position_comment_repository
    )
    
    mark_job_position_comment_as_pending_command_handler = providers.Factory(
        MarkJobPositionCommentAsPendingCommandHandler,
        comment_repository=job_position_comment_repository
    )
    
    # Position Stage Assignment Query Handlers
    list_stage_assignments_query_handler = providers.Factory(
        ListStageAssignmentsQueryHandler,
        repository=position_stage_assignment_repository
    )
    
    get_assigned_users_query_handler = providers.Factory(
        GetAssignedUsersQueryHandler,
        repository=position_stage_assignment_repository
    )
    
    # Position Stage Assignment Command Handlers
    assign_users_to_stage_command_handler = providers.Factory(
        AssignUsersToStageCommandHandler,
        repository=position_stage_assignment_repository
    )
    
    add_user_to_stage_command_handler = providers.Factory(
        AddUserToStageCommandHandler,
        repository=position_stage_assignment_repository
    )
    
    remove_user_from_stage_command_handler = providers.Factory(
        RemoveUserFromStageCommandHandler,
        repository=position_stage_assignment_repository
    )
    
    copy_workflow_assignments_command_handler = providers.Factory(
        CopyWorkflowAssignmentsCommandHandler,
        repository=position_stage_assignment_repository
    )

    # Position Question Config Query Handlers
    list_position_question_configs_query_handler = providers.Factory(
        ListPositionQuestionConfigsQueryHandler,
        repository=position_question_config_repository
    )

    get_enabled_questions_for_position_query_handler = providers.Factory(
        GetEnabledQuestionsForPositionQueryHandler,
        job_position_repository=job_position_repository,
        application_question_repository=shared.application_question_repository,
        position_question_config_repository=position_question_config_repository
    )

    # Position Question Config Command Handlers
    configure_position_question_command_handler = providers.Factory(
        ConfigurePositionQuestionCommandHandler,
        repository=position_question_config_repository
    )

    remove_position_question_config_command_handler = providers.Factory(
        RemovePositionQuestionConfigCommandHandler,
        repository=position_question_config_repository
    )

    # Controllers
    job_position_controller = providers.Factory(
        JobPositionController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    job_position_comment_controller = providers.Factory(
        JobPositionCommentController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    public_position_controller = providers.Factory(
        PublicPositionController,
        query_bus=shared.query_bus
    )
    
    position_stage_assignment_controller = providers.Factory(
        PositionStageAssignmentController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

    position_question_config_controller = providers.Factory(
        PositionQuestionConfigController,
        query_bus=shared.query_bus,
        command_bus=shared.command_bus
    )

