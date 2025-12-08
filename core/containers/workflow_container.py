"""Workflow Container - Workflow Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.shared.workflow.controllers import WorkflowController
from adapters.http.shared.workflow.controllers import WorkflowStageController
from adapters.http.shared.phase.controllers.phase_controller import PhaseController
from adapters.http.shared.customization.controllers.entity_customization_controller import EntityCustomizationController
from adapters.http.shared.workflow_analytics.controllers.workflow_analytics_controller import WorkflowAnalyticsController
from adapters.http.shared.field_validation.controllers.validation_rule_controller import ValidationRuleController

# Workflow Infrastructure
from src.shared_bc.customization.workflow.infrastructure.repositories import WorkflowRepository
from src.shared_bc.customization.workflow.infrastructure.repositories.workflow_stage_repository import WorkflowStageRepository
from src.shared_bc.customization.phase.infrastructure.repositories.phase_repository import PhaseRepository
from src.shared_bc.customization.entity_customization.infrastructure.repositories.entity_customization_repository import EntityCustomizationRepository
from src.shared_bc.customization.entity_customization.infrastructure.repositories.custom_field_repository import CustomFieldRepository as NewCustomFieldRepository
from src.shared_bc.customization.field_validation.infrastructure.repositories.validation_rule_repository import ValidationRuleRepository

# Company User Repository (needed for StagePermissionService)
from src.company_bc.company.infrastructure.repositories.company_user_repository import CompanyUserRepository

# Workflow Domain Services
from src.shared_bc.customization.workflow.domain.services.stage_phase_validation_service import StagePhaseValidationService
from src.shared_bc.customization.field_validation.application.services.field_validation_service import FieldValidationService
from src.shared_bc.customization.field_validation.application.services.interview_validation_service import InterviewValidationService
from src.company_bc.candidate_application.application.services.stage_permission_service import StagePermissionService
from src.shared_bc.customization.workflow.application.services.workflow_response_service import WorkflowResponseService

# Candidate Application Query for permission checking
from src.company_bc.candidate_application.application.queries.can_user_process_application_query import \
    CanUserProcessApplicationQueryHandler

# Workflow Application Layer - Commands
from src.shared_bc.customization.workflow.application import CreateWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.update_workflow_command import UpdateWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.activate_workflow_command import ActivateWorkflowCommandHandler
from src.shared_bc.customization.workflow.application import DeactivateWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.archive_workflow_command import ArchiveWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.delete_workflow_command import DeleteWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.set_as_default_workflow_command import SetAsDefaultWorkflowCommandHandler
from src.shared_bc.customization.workflow.application.commands.workflow.unset_as_default_workflow_command import UnsetAsDefaultWorkflowCommandHandler

# WorkflowStage Application Layer - Commands
from src.shared_bc.customization.workflow.application import CreateStageCommandHandler
from src.shared_bc.customization.workflow.application.commands.stage.update_stage_command import UpdateStageCommandHandler
from src.shared_bc.customization.workflow.application.commands.stage.delete_stage_command import DeleteStageCommandHandler
from src.shared_bc.customization.workflow.application import ReorderStagesCommandHandler
from src.shared_bc.customization.workflow.application.commands.stage.activate_stage_command import ActivateStageCommandHandler
from src.shared_bc.customization.workflow.application import DeactivateStageCommandHandler

# Workflow Application Layer - Queries
from src.shared_bc.customization.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQueryHandler
from src.shared_bc.customization.workflow.application.queries.workflow.list_workflows_by_company import ListWorkflowsByCompanyQueryHandler
from src.shared_bc.customization.workflow.application.queries.workflow.list_workflows_by_phase import ListWorkflowsByPhaseQueryHandler

# WorkflowStage Application Layer - Queries
from src.shared_bc.customization.workflow.application.queries.stage.get_stage_by_id import GetStageByIdQueryHandler
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQueryHandler
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_phase import ListStagesByPhaseQueryHandler
from src.shared_bc.customization.workflow.application import GetInitialStageQueryHandler
from src.shared_bc.customization.workflow.application.queries.stage.get_final_stages import GetFinalStagesQueryHandler

# Phase Application Layer
from src.shared_bc.customization.phase.application import (
    GetPhaseByIdQueryHandler,
    ListPhasesByCompanyQueryHandler,
    ArchivePhaseCommandHandler,
    ActivatePhaseCommandHandler,
    CreatePhaseCommandHandler,
    UpdatePhaseCommandHandler,
    InitializeCompanyPhasesCommandHandler,
    DeletePhaseCommandHandler
)
from src.shared_bc.customization.phase.application.handlers.candidate_stage_transition_handler import CandidateStageTransitionHandler

# EntityCustomization Application Layer - Commands
from src.shared_bc.customization.entity_customization.application.commands.create_entity_customization_command import CreateEntityCustomizationCommandHandler
from src.shared_bc.customization.entity_customization.application.commands.update_entity_customization_command import UpdateEntityCustomizationCommandHandler
from src.shared_bc.customization.entity_customization.application.commands.delete_entity_customization_command import DeleteEntityCustomizationCommandHandler
from src.shared_bc.customization.entity_customization.application.commands.add_custom_field_to_entity_command import AddCustomFieldToEntityCommandHandler

# EntityCustomization Application Layer - Queries
from src.shared_bc.customization.entity_customization.application.queries.get_entity_customization_query import GetEntityCustomizationQueryHandler
from src.shared_bc.customization.entity_customization.application.queries.get_entity_customization_by_id_query import GetEntityCustomizationByIdQueryHandler
from src.shared_bc.customization.entity_customization.application.queries.list_custom_fields_by_entity_query import ListCustomFieldsByEntityQueryHandler
from src.shared_bc.customization.entity_customization.application.queries.get_custom_field_values_by_entity_query import GetCustomFieldValuesByEntityQueryHandler

# FieldValidation Application Layer - Commands
from src.shared_bc.customization.field_validation.application.commands.create_validation_rule_command import CreateValidationRuleCommandHandler
from src.shared_bc.customization.field_validation.application.commands.update_validation_rule_command import UpdateValidationRuleCommandHandler
from src.shared_bc.customization.field_validation.application.commands.delete_validation_rule_command import DeleteValidationRuleCommandHandler
from src.shared_bc.customization.field_validation.application.commands.activate_validation_rule_command import ActivateValidationRuleCommandHandler
from src.shared_bc.customization.field_validation.application.commands.deactivate_validation_rule_command import DeactivateValidationRuleCommandHandler

# FieldValidation Application Layer - Queries
from src.shared_bc.customization.field_validation.application.queries.get_validation_rule_by_id_query import GetValidationRuleByIdQueryHandler
from src.shared_bc.customization.field_validation.application.queries.list_validation_rules_by_stage_query import ListValidationRulesByStageQueryHandler
from src.shared_bc.customization.field_validation.application.queries.list_validation_rules_by_field_query import ListValidationRulesByFieldQueryHandler

# ApplicationQuestion Infrastructure
from src.shared_bc.customization.workflow.infrastructure.repositories.application_question_repository import ApplicationQuestionRepository

# ApplicationQuestion Application Layer - Queries
from src.shared_bc.customization.workflow.application.queries.application_question.list_application_questions_query import ListApplicationQuestionsQueryHandler

# ApplicationQuestion Application Layer - Commands
from src.shared_bc.customization.workflow.application.commands.application_question.create_application_question_command import CreateApplicationQuestionCommandHandler
from src.shared_bc.customization.workflow.application.commands.application_question.update_application_question_command import UpdateApplicationQuestionCommandHandler
from src.shared_bc.customization.workflow.application.commands.application_question.delete_application_question_command import DeleteApplicationQuestionCommandHandler

# ApplicationQuestion Controller
from adapters.http.company_app.application_question.controllers.application_question_controller import ApplicationQuestionController

# WorkflowAnalytics Application Layer - Queries
from src.shared_bc.customization.workflow_analytics.application.queries.get_workflow_analytics_query import GetWorkflowAnalyticsQueryHandler
from src.shared_bc.customization.workflow_analytics.application.queries.get_stage_bottlenecks_query import GetStageBottlenecksQueryHandler


class WorkflowContainer(containers.DeclarativeContainer):
    """Container para Workflow Bounded Context"""
    
    # Dependencias compartidas
    shared = providers.DependenciesContainer()
    
    # Repositories
    workflow_repository = providers.Factory(
        WorkflowRepository,
        database=shared.database
    )
    
    workflow_stage_repository = providers.Factory(
        WorkflowStageRepository,
        database=shared.database
    )
    
    phase_repository = providers.Factory(
        PhaseRepository,
        database=shared.database
    )
    
    entity_customization_repository = providers.Factory(
        EntityCustomizationRepository,
        database=shared.database
    )
    
    new_custom_field_repository = providers.Factory(
        NewCustomFieldRepository,
        database=shared.database
    )
    
    validation_rule_repository = providers.Factory(
        ValidationRuleRepository
    )

    # Company User Repository (for permission checks)
    company_user_repository = providers.Factory(
        CompanyUserRepository,
        database=shared.database
    )

    # Domain Services
    stage_phase_validation_service = providers.Factory(
        StagePhaseValidationService,
        workflow_repository=workflow_repository,
        stage_repository=workflow_stage_repository
    )
    
    interview_validation_service = providers.Factory(
        InterviewValidationService,
        interview_repository=shared.interview_repository
    )
    
    field_validation_service = providers.Factory(
        FieldValidationService,
        validation_rule_repository=validation_rule_repository,
        custom_field_repository=new_custom_field_repository
    )
    
    stage_permission_service = providers.Factory(
        StagePermissionService,
        position_stage_assignment_repository=shared.position_stage_assignment_repository,
        company_user_repository=company_user_repository
    )

    # Permission Query Handler
    can_user_process_application_query_handler = providers.Factory(
        CanUserProcessApplicationQueryHandler,
        application_repository=shared.candidate_application_repository,
        stage_permission_service=stage_permission_service
    )

    candidate_stage_transition_handler = providers.Factory(
        CandidateStageTransitionHandler,
        application_repository=shared.candidate_application_repository,
        stage_repository=workflow_stage_repository,
        workflow_repository=workflow_repository
    )
    
    workflow_response_service = providers.Factory(
        WorkflowResponseService,
        query_bus=shared.query_bus
    )
    
    # Workflow Query Handlers
    get_workflow_by_id_query_handler = providers.Factory(
        GetWorkflowByIdQueryHandler,
        repository=workflow_repository
    )
    
    list_workflows_by_company_query_handler = providers.Factory(
        ListWorkflowsByCompanyQueryHandler,
        repository=workflow_repository
    )
    
    list_workflows_by_phase_query_handler = providers.Factory(
        ListWorkflowsByPhaseQueryHandler,
        repository=workflow_repository
    )
    
    # WorkflowStage Query Handlers
    get_stage_by_id_query_handler = providers.Factory(
        GetStageByIdQueryHandler,
        repository=workflow_stage_repository
    )
    
    list_stages_by_workflow_query_handler = providers.Factory(
        ListStagesByWorkflowQueryHandler,
        repository=workflow_stage_repository
    )
    
    list_stages_by_phase_query_handler = providers.Factory(
        ListStagesByPhaseQueryHandler,
        repository=workflow_stage_repository
    )
    
    get_initial_stage_query_handler = providers.Factory(
        GetInitialStageQueryHandler,
        repository=workflow_stage_repository
    )
    
    get_final_stages_query_handler = providers.Factory(
        GetFinalStagesQueryHandler,
        repository=workflow_stage_repository
    )
    
    # Workflow Command Handlers
    create_workflow_command_handler = providers.Factory(
        CreateWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    update_workflow_command_handler = providers.Factory(
        UpdateWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    activate_workflow_command_handler = providers.Factory(
        ActivateWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    deactivate_workflow_command_handler = providers.Factory(
        DeactivateWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    archive_workflow_command_handler = providers.Factory(
        ArchiveWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    delete_workflow_command_handler = providers.Factory(
        DeleteWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    set_as_default_workflow_command_handler = providers.Factory(
        SetAsDefaultWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    unset_as_default_workflow_command_handler = providers.Factory(
        UnsetAsDefaultWorkflowCommandHandler,
        repository=workflow_repository
    )
    
    # WorkflowStage Command Handlers
    create_stage_command_handler = providers.Factory(
        CreateStageCommandHandler,
        repository=workflow_stage_repository
    )
    
    update_stage_command_handler = providers.Factory(
        UpdateStageCommandHandler,
        repository=workflow_stage_repository
    )
    
    delete_stage_command_handler = providers.Factory(
        DeleteStageCommandHandler,
        repository=workflow_stage_repository
    )
    
    reorder_stages_command_handler = providers.Factory(
        ReorderStagesCommandHandler,
        repository=workflow_stage_repository
    )
    
    activate_stage_command_handler = providers.Factory(
        ActivateStageCommandHandler,
        repository=workflow_stage_repository
    )
    
    deactivate_stage_command_handler = providers.Factory(
        DeactivateStageCommandHandler,
        repository=workflow_stage_repository
    )
    
    # Phase Query Handlers
    get_phase_by_id_query_handler = providers.Factory(
        GetPhaseByIdQueryHandler,
        phase_repository=phase_repository
    )
    
    list_phases_by_company_query_handler = providers.Factory(
        ListPhasesByCompanyQueryHandler,
        phase_repository=phase_repository
    )
    
    # Phase Command Handlers
    create_phase_command_handler = providers.Factory(
        CreatePhaseCommandHandler,
        phase_repository=phase_repository
    )
    
    update_phase_command_handler = providers.Factory(
        UpdatePhaseCommandHandler,
        phase_repository=phase_repository
    )
    
    delete_phase_command_handler = providers.Factory(
        DeletePhaseCommandHandler,
        phase_repository=phase_repository
    )
    
    archive_phase_command_handler = providers.Factory(
        ArchivePhaseCommandHandler,
        phase_repository=phase_repository
    )
    
    activate_phase_command_handler = providers.Factory(
        ActivatePhaseCommandHandler,
        phase_repository=phase_repository
    )
    
    initialize_company_phases_command_handler = providers.Factory(
        InitializeCompanyPhasesCommandHandler,
        phase_repository=phase_repository,
        workflow_repository=workflow_repository,
        stage_repository=workflow_stage_repository
    )
    
    # EntityCustomization Query Handlers
    get_entity_customization_query_handler = providers.Factory(
        GetEntityCustomizationQueryHandler,
        repository=entity_customization_repository
    )
    
    get_entity_customization_by_id_query_handler = providers.Factory(
        GetEntityCustomizationByIdQueryHandler,
        repository=entity_customization_repository
    )
    
    list_custom_fields_by_entity_query_handler = providers.Factory(
        ListCustomFieldsByEntityQueryHandler,
        repository=new_custom_field_repository
    )
    
    get_custom_field_values_by_entity_query_handler = providers.Factory(
        GetCustomFieldValuesByEntityQueryHandler,
        database=shared.database
    )
    
    # EntityCustomization Command Handlers
    create_entity_customization_command_handler = providers.Factory(
        CreateEntityCustomizationCommandHandler,
        repository=entity_customization_repository
    )
    
    update_entity_customization_command_handler = providers.Factory(
        UpdateEntityCustomizationCommandHandler,
        repository=entity_customization_repository
    )
    
    delete_entity_customization_command_handler = providers.Factory(
        DeleteEntityCustomizationCommandHandler,
        repository=entity_customization_repository
    )
    
    add_custom_field_to_entity_command_handler = providers.Factory(
        AddCustomFieldToEntityCommandHandler,
        repository=entity_customization_repository
    )
    
    # FieldValidation Query Handlers
    get_validation_rule_by_id_query_handler = providers.Factory(
        GetValidationRuleByIdQueryHandler,
        repository=validation_rule_repository
    )
    
    list_validation_rules_by_stage_query_handler = providers.Factory(
        ListValidationRulesByStageQueryHandler,
        repository=validation_rule_repository
    )
    
    list_validation_rules_by_field_query_handler = providers.Factory(
        ListValidationRulesByFieldQueryHandler,
        repository=validation_rule_repository
    )
    
    # FieldValidation Command Handlers
    create_validation_rule_command_handler = providers.Factory(
        CreateValidationRuleCommandHandler,
        repository=validation_rule_repository
    )
    
    update_validation_rule_command_handler = providers.Factory(
        UpdateValidationRuleCommandHandler,
        repository=validation_rule_repository
    )
    
    delete_validation_rule_command_handler = providers.Factory(
        DeleteValidationRuleCommandHandler,
        repository=validation_rule_repository
    )
    
    activate_validation_rule_command_handler = providers.Factory(
        ActivateValidationRuleCommandHandler,
        repository=validation_rule_repository
    )
    
    deactivate_validation_rule_command_handler = providers.Factory(
        DeactivateValidationRuleCommandHandler,
        repository=validation_rule_repository
    )
    
    # WorkflowAnalytics Query Handlers
    get_workflow_analytics_query_handler = providers.Factory(
        GetWorkflowAnalyticsQueryHandler,
        workflow_repository=workflow_repository,
        workflow_stage_repository=workflow_stage_repository
    )
    
    get_stage_bottlenecks_query_handler = providers.Factory(
        GetStageBottlenecksQueryHandler,
        workflow_repository=workflow_repository,
        workflow_stage_repository=workflow_stage_repository
    )
    
    # Controllers
    workflow_controller = providers.Factory(
        WorkflowController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus,
        database=shared.database,
        workflow_response_service=workflow_response_service
    )
    
    workflow_stage_controller = providers.Factory(
        WorkflowStageController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    phase_controller = providers.Factory(
        PhaseController,
        create_handler=create_phase_command_handler,
        update_handler=update_phase_command_handler,
        delete_handler=delete_phase_command_handler,
        archive_handler=archive_phase_command_handler,
        activate_handler=activate_phase_command_handler,
        get_by_id_handler=get_phase_by_id_query_handler,
        list_by_company_handler=list_phases_by_company_query_handler,
        initialize_handler=initialize_company_phases_command_handler
    )
    
    entity_customization_controller = providers.Factory(
        EntityCustomizationController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    workflow_analytics_controller = providers.Factory(
        WorkflowAnalyticsController,
        query_bus=shared.query_bus
    )
    
    validation_rule_controller = providers.Factory(
        ValidationRuleController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

    # ApplicationQuestion Repository
    application_question_repository = providers.Factory(
        ApplicationQuestionRepository,
        database=shared.database
    )

    # ApplicationQuestion Query Handlers
    list_application_questions_query_handler = providers.Factory(
        ListApplicationQuestionsQueryHandler,
        repository=application_question_repository
    )

    # ApplicationQuestion Command Handlers
    create_application_question_command_handler = providers.Factory(
        CreateApplicationQuestionCommandHandler,
        repository=application_question_repository
    )

    update_application_question_command_handler = providers.Factory(
        UpdateApplicationQuestionCommandHandler,
        repository=application_question_repository
    )

    delete_application_question_command_handler = providers.Factory(
        DeleteApplicationQuestionCommandHandler,
        repository=application_question_repository
    )

    # ApplicationQuestion Controller
    application_question_controller = providers.Factory(
        ApplicationQuestionController,
        query_bus=shared.query_bus,
        command_bus=shared.command_bus
    )
