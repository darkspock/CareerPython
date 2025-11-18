"""Main Container - Composes all bounded context containers"""
from dependency_injector import containers, providers
from core.containers.shared_container import SharedContainer
from core.containers.auth_container import AuthContainer
from core.containers.interview_container import InterviewContainer
from core.containers.company_container import CompanyContainer
from core.containers.candidate_container import CandidateContainer
from core.containers.job_position_container import JobPositionContainer
from core.containers.workflow_container import WorkflowContainer
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

# Import the old container temporarily for backward compatibility
from core.container import Container as OldContainer


class Container(containers.DeclarativeContainer):
    """Container principal que compone todos los bounded contexts"""
    
    # Wiring configuration - will be set from main.py
    wiring_config = containers.WiringConfiguration()
    
    # Shared Container (servicios core)
    shared = providers.Container(SharedContainer)
    
    # Temporary: Use old container for backward compatibility during migration
    # This will be gradually replaced with modular containers
    _old_container = providers.Container(OldContainer)
    
    # Command Bus y Query Bus - Create first (needed by bounded contexts)
    # Note: These will be overridden in main.py after container is created
    command_bus = providers.Singleton(CommandBus)
    query_bus = providers.Singleton(QueryBus)
    
    # Create a container class for shared dependencies that will be passed to BC containers
    # This needs to be defined after shared, command_bus, and query_bus
    class SharedDependencies(containers.DeclarativeContainer):
        """Container with shared services - will be populated dynamically"""
        pass
    
    # Populate SharedDependencies with basic services BEFORE creating BC containers
    # This ensures command_bus and query_bus are available when BC containers are instantiated
    SharedDependencies.database = shared.database
    SharedDependencies.event_bus = shared.event_bus
    SharedDependencies.email_service = shared.email_service
    SharedDependencies.ai_service = shared.ai_service
    SharedDependencies.storage_service = shared.storage_service
    SharedDependencies.async_job_service = shared.async_job_service
    SharedDependencies.command_bus = command_bus
    SharedDependencies.query_bus = query_bus
    
    # Bounded Context Containers - Order matters for dependencies
    # Auth and Interview first (minimal dependencies)
    auth = providers.Container(
        AuthContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    interview = providers.Container(
        InterviewContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    # Workflow next (needed by Company, JobPosition, Candidate)
    workflow = providers.Container(
        WorkflowContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    # Company (depends on Workflow)
    company = providers.Container(
        CompanyContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    # Candidate (depends on Workflow, JobPosition)
    candidate = providers.Container(
        CandidateContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    # JobPosition (depends on Workflow)
    job_position = providers.Container(
        JobPositionContainer,
        shared=providers.Container(SharedDependencies)
    )
    
    # Now populate SharedDependencies with cross-BC dependencies
    # Basic services were already populated before creating BC containers
    # Cross-BC dependencies
    SharedDependencies.user_repository = auth.user_repository
    SharedDependencies.staff_repository = auth.staff_repository
    SharedDependencies.interview_repository = interview.interview_repository
    SharedDependencies.workflow_repository = workflow.workflow_repository
    SharedDependencies.workflow_stage_repository = workflow.workflow_stage_repository
    SharedDependencies.stage_phase_validation_service = workflow.stage_phase_validation_service
    SharedDependencies.interview_validation_service = workflow.interview_validation_service
    SharedDependencies.job_position_repository = job_position.job_position_repository
    SharedDependencies.candidate_repository = candidate.candidate_repository
    SharedDependencies.candidate_application_repository = candidate.candidate_application_repository
    SharedDependencies.position_stage_assignment_repository = job_position.position_stage_assignment_repository
    
    # Exponer servicios compartidos directamente para compatibilidad
    database = shared.database
    event_bus = shared.event_bus
    email_service = shared.email_service
    ai_service = shared.ai_service
    storage_service = shared.storage_service
    async_job_service = shared.async_job_service
    
    # Exponer providers de containers modulares para compatibilidad
    # Auth
    user_repository = auth.user_repository
    staff_repository = auth.staff_repository
    user_asset_repository = auth.user_asset_repository
    user_controller = auth.user_controller
    invitation_controller = auth.invitation_controller
    
    # Interview
    interview_repository = interview.interview_repository
    interview_answer_repository = interview.interview_answer_repository
    interview_interviewer_repository = interview.interview_interviewer_repository
    interview_template_repository = interview.interview_template_repository
    interview_template_section_repository = interview.interview_template_section_repository
    interview_template_question_repository = interview.interview_template_question_repository
    interview_controller = interview.interview_controller
    interview_template_controller = interview.interview_template_controller
    
    # Company
    company_repository = company.company_repository
    company_user_repository = company.company_user_repository
    company_role_repository = company.company_role_repository
    company_candidate_repository = company.company_candidate_repository
    company_controller = company.company_controller
    # Alias for backward compatibility
    company_management_controller = company.company_controller
    company_user_controller = company.company_user_controller
    company_role_controller = company.company_role_controller
    company_candidate_controller = company.company_candidate_controller
    candidate_comment_controller = company.candidate_comment_controller
    review_controller = company.review_controller
    task_controller = company.task_controller
    email_template_controller = company.email_template_controller
    talent_pool_controller = company.talent_pool_controller
    company_page_controller = company.company_page_controller
    
    # Candidate
    candidate_repository = candidate.candidate_repository
    candidate_controller = candidate.candidate_controller
    application_controller = candidate.application_controller
    onboarding_controller = candidate.onboarding_controller
    resume_controller = candidate.resume_controller
    admin_candidate_controller = candidate.admin_candidate_controller
    
    # JobPosition
    job_position_repository = job_position.job_position_repository
    job_position_controller = job_position.job_position_controller
    job_position_comment_controller = job_position.job_position_comment_controller
    public_position_controller = job_position.public_position_controller
    position_stage_assignment_controller = job_position.position_stage_assignment_controller
    
    # Workflow
    workflow_repository = workflow.workflow_repository
    workflow_stage_repository = workflow.workflow_stage_repository
    phase_repository = workflow.phase_repository
    workflow_controller = workflow.workflow_controller
    workflow_stage_controller = workflow.workflow_stage_controller
    phase_controller = workflow.phase_controller
    entity_customization_controller = workflow.entity_customization_controller
    workflow_analytics_controller = workflow.workflow_analytics_controller
    validation_rule_controller = workflow.validation_rule_controller
    stage_phase_validation_service = workflow.stage_phase_validation_service
    interview_validation_service = workflow.interview_validation_service
    # Alias for backward compatibility
    candidate_application_workflow_controller = workflow.workflow_controller
    
    # Exponer todos los providers del container antiguo para compatibilidad
    # Esto permite una migración gradual sin romper el código existente
    def __getattr__(self, name):
        """Delegate to old container for providers not yet migrated"""
        return getattr(self._old_container, name)
