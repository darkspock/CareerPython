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
    
    # Populate SharedDependencies with Auth repositories BEFORE creating Company container
    # Company container needs user_repository and staff_repository
    SharedDependencies.user_repository = auth.user_repository
    SharedDependencies.staff_repository = auth.staff_repository
    
    # Populate SharedDependencies with Workflow repositories BEFORE creating Company container
    # Some Company handlers need workflow_repository, workflow_stage_repository, phase_repository, and entity_customization_repository
    SharedDependencies.workflow_repository = workflow.workflow_repository
    SharedDependencies.workflow_stage_repository = workflow.workflow_stage_repository
    SharedDependencies.phase_repository = workflow.phase_repository
    SharedDependencies.entity_customization_repository = workflow.entity_customization_repository
    SharedDependencies.interview_repository = interview.interview_repository
    
    # Company (depends on Workflow and Auth)
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
    
    # Now populate SharedDependencies with remaining cross-BC dependencies
    # Basic services, Auth repositories, and Workflow repositories were already populated
    # Cross-BC dependencies that depend on containers created after Company
    SharedDependencies.candidate_repository = candidate.candidate_repository
    SharedDependencies.job_position_repository = job_position.job_position_repository
    SharedDependencies.stage_phase_validation_service = workflow.stage_phase_validation_service
    SharedDependencies.interview_validation_service = workflow.interview_validation_service
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
    # Company Query Handlers (needed by QueryBus)
    get_company_by_id_query_handler = company.get_company_by_id_query_handler
    get_company_by_domain_query_handler = company.get_company_by_domain_query_handler
    get_company_by_slug_query_handler = company.get_company_by_slug_query_handler
    list_companies_query_handler = company.list_companies_query_handler
    get_company_user_by_id_query_handler = company.get_company_user_by_id_query_handler
    get_company_user_by_company_and_user_query_handler = company.get_company_user_by_company_and_user_query_handler
    list_company_users_by_company_query_handler = company.list_company_users_by_company_query_handler
    authenticate_company_user_query_handler = company.authenticate_company_user_query_handler
    get_user_invitation_query_handler = company.get_user_invitation_query_handler
    get_user_permissions_query_handler = company.get_user_permissions_query_handler
    get_invitation_by_email_and_company_query_handler = company.get_invitation_by_email_and_company_query_handler
    
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
    
    # Exponer todos los handlers (needed by QueryBus and CommandBus)
    # Auth Handlers
    authenticate_user_query_handler = auth.authenticate_user_query_handler
    check_user_exists_query_handler = auth.check_user_exists_query_handler
    create_access_token_query_handler = auth.create_access_token_query_handler
    create_user_automatically_command_handler = auth.create_user_automatically_command_handler
    create_user_command_handler = auth.create_user_command_handler
    create_user_from_landing_command_handler = auth.create_user_from_landing_command_handler
    get_current_user_from_token_query_handler = auth.get_current_user_from_token_query_handler
    get_user_by_email_query_handler = auth.get_user_by_email_query_handler
    get_user_language_query_handler = auth.get_user_language_query_handler
    request_password_reset_command_handler = auth.request_password_reset_command_handler
    reset_password_with_token_command_handler = auth.reset_password_with_token_command_handler
    update_user_language_command_handler = auth.update_user_language_command_handler
    update_user_password_command_handler = auth.update_user_password_command_handler
    
    # Interview Handlers
    accept_interviewer_invitation_command_handler = interview.accept_interviewer_invitation_command_handler
    create_interview_answer_command_handler = interview.create_interview_answer_command_handler
    create_interview_command_handler = interview.create_interview_command_handler
    create_interview_template_command_handler = interview.create_interview_template_command_handler
    create_interview_template_question_command_handler = interview.create_interview_template_question_command_handler
    create_interview_template_section_command_handler = interview.create_interview_template_section_command_handler
    delete_interview_template_command_handler = interview.delete_interview_template_command_handler
    delete_interview_template_section_command_handler = interview.delete_interview_template_section_command_handler
    disable_interview_template_command_handler = interview.disable_interview_template_command_handler
    disable_interview_template_question_command_handler = interview.disable_interview_template_question_command_handler
    disable_interview_template_section_command_handler = interview.disable_interview_template_section_command_handler
    enable_interview_template_command_handler = interview.enable_interview_template_command_handler
    enable_interview_template_question_command_handler = interview.enable_interview_template_question_command_handler
    enable_interview_template_section_command_handler = interview.enable_interview_template_section_command_handler
    finish_interview_command_handler = interview.finish_interview_command_handler
    generate_interview_link_command_handler = interview.generate_interview_link_command_handler
    get_answers_by_interview_query_handler = interview.get_answers_by_interview_query_handler
    get_interview_answer_by_id_query_handler = interview.get_interview_answer_by_id_query_handler
    get_interview_by_id_query_handler = interview.get_interview_by_id_query_handler
    get_interview_by_token_query_handler = interview.get_interview_by_token_query_handler
    get_interview_questions_by_token_query_handler = interview.get_interview_questions_by_token_query_handler
    get_interview_score_summary_query_handler = interview.get_interview_score_summary_query_handler
    get_interview_statistics_query_handler = interview.get_interview_statistics_query_handler
    get_interview_template_by_id_query_handler = interview.get_interview_template_by_id_query_handler
    get_interview_template_full_by_id_query_handler = interview.get_interview_template_full_by_id_query_handler
    get_interviewers_by_interview_query_handler = interview.get_interviewers_by_interview_query_handler
    get_interviews_by_candidate_query_handler = interview.get_interviews_by_candidate_query_handler
    get_interviews_by_date_range_query_handler = interview.get_interviews_by_date_range_query_handler
    get_overdue_interviews_query_handler = interview.get_overdue_interviews_query_handler
    get_pending_interviews_by_candidate_and_stage_query_handler = interview.get_pending_interviews_by_candidate_and_stage_query_handler
    get_questions_by_section_query_handler = interview.get_questions_by_section_query_handler
    get_scheduled_interviews_query_handler = interview.get_scheduled_interviews_query_handler
    invite_interviewer_command_handler = interview.invite_interviewer_command_handler
    list_interview_templates_query_handler = interview.list_interview_templates_query_handler
    list_interviews_query_handler = interview.list_interviews_query_handler
    move_section_down_command_handler = interview.move_section_down_command_handler
    move_section_up_command_handler = interview.move_section_up_command_handler
    score_interview_answer_command_handler = interview.score_interview_answer_command_handler
    start_interview_command_handler = interview.start_interview_command_handler
    submit_interview_answer_by_token_command_handler = interview.submit_interview_answer_by_token_command_handler
    update_interview_answer_command_handler = interview.update_interview_answer_command_handler
    update_interview_command_handler = interview.update_interview_command_handler
    update_interview_template_command_handler = interview.update_interview_template_command_handler
    update_interview_template_question_command_handler = interview.update_interview_template_question_command_handler
    update_interview_template_section_command_handler = interview.update_interview_template_section_command_handler
    
    # Company Handlers (continuación de los ya agregados arriba)
    accept_user_invitation_command_handler = company.accept_user_invitation_command_handler
    activate_company_command_handler = company.activate_company_command_handler
    activate_company_user_command_handler = company.activate_company_user_command_handler
    add_company_user_command_handler = company.add_company_user_command_handler
    archive_company_candidate_command_handler = company.archive_company_candidate_command_handler
    assign_role_to_user_command_handler = company.assign_role_to_user_command_handler
    assign_workflow_command_handler = company.assign_workflow_command_handler
    change_stage_command_handler = company.change_stage_command_handler
    confirm_company_candidate_command_handler = company.confirm_company_candidate_command_handler
    count_pending_comments_query_handler = company.count_pending_comments_query_handler
    create_candidate_comment_command_handler = company.create_candidate_comment_command_handler
    create_candidate_review_command_handler = company.create_candidate_review_command_handler
    create_company_candidate_command_handler = company.create_company_candidate_command_handler
    create_company_command_handler = company.create_company_command_handler
    create_role_command_handler = company.create_role_command_handler
    deactivate_company_user_command_handler = company.deactivate_company_user_command_handler
    delete_candidate_comment_command_handler = company.delete_candidate_comment_command_handler
    delete_candidate_review_command_handler = company.delete_candidate_review_command_handler
    delete_company_command_handler = company.delete_company_command_handler
    delete_company_with_all_data_command_handler = company.delete_company_with_all_data_command_handler
    delete_role_command_handler = company.delete_role_command_handler
    get_candidate_comment_by_id_query_handler = company.get_candidate_comment_by_id_query_handler
    get_companies_stats_query_handler = company.get_companies_stats_query_handler
    get_company_candidate_by_company_and_candidate_query_handler = company.get_company_candidate_by_company_and_candidate_query_handler
    get_company_candidate_by_id_query_handler = company.get_company_candidate_by_id_query_handler
    get_company_candidate_by_id_with_candidate_info_query_handler = company.get_company_candidate_by_id_with_candidate_info_query_handler
    get_company_role_by_id_query_handler = company.get_company_role_by_id_query_handler
    get_review_by_id_query_handler = company.get_review_by_id_query_handler
    initialize_onboarding_command_handler = company.initialize_onboarding_command_handler
    initialize_sample_data_command_handler = company.initialize_sample_data_command_handler
    invite_company_user_command_handler = company.invite_company_user_command_handler
    link_user_to_company_command_handler = company.link_user_to_company_command_handler
    list_candidate_comments_by_company_candidate_query_handler = company.list_candidate_comments_by_company_candidate_query_handler
    list_candidate_comments_by_stage_query_handler = company.list_candidate_comments_by_stage_query_handler
    list_company_candidates_by_candidate_query_handler = company.list_company_candidates_by_candidate_query_handler
    list_company_candidates_by_company_query_handler = company.list_company_candidates_by_company_query_handler
    list_company_candidates_with_candidate_info_query_handler = company.list_company_candidates_with_candidate_info_query_handler
    list_global_reviews_query_handler = company.list_global_reviews_query_handler
    list_reviews_by_company_candidate_query_handler = company.list_reviews_by_company_candidate_query_handler
    list_reviews_by_stage_query_handler = company.list_reviews_by_stage_query_handler
    list_roles_by_company_query_handler = company.list_roles_by_company_query_handler
    mark_comment_as_pending_command_handler = company.mark_comment_as_pending_command_handler
    mark_comment_as_reviewed_command_handler = company.mark_comment_as_reviewed_command_handler
    mark_review_as_pending_command_handler = company.mark_review_as_pending_command_handler
    mark_review_as_reviewed_command_handler = company.mark_review_as_reviewed_command_handler
    register_company_with_user_command_handler = company.register_company_with_user_command_handler
    reject_company_candidate_command_handler = company.reject_company_candidate_command_handler
    remove_company_user_command_handler = company.remove_company_user_command_handler
    suspend_company_command_handler = company.suspend_company_command_handler
    transfer_ownership_command_handler = company.transfer_ownership_command_handler
    update_candidate_comment_command_handler = company.update_candidate_comment_command_handler
    update_candidate_review_command_handler = company.update_candidate_review_command_handler
    update_company_candidate_command_handler = company.update_company_candidate_command_handler
    update_company_command_handler = company.update_company_command_handler
    update_company_user_command_handler = company.update_company_user_command_handler
    update_role_command_handler = company.update_role_command_handler
    upload_company_logo_command_handler = company.upload_company_logo_command_handler
    
    # Candidate Handlers
    admin_list_candidates_query_handler = candidate.admin_list_candidates_query_handler
    analyze_pdf_resume_command_handler = candidate.analyze_pdf_resume_command_handler
    claim_task_command_handler = candidate.claim_task_command_handler
    create_candidate_application_command_handler = candidate.create_candidate_application_command_handler
    create_candidate_command_handler = candidate.create_candidate_command_handler
    create_education_command_handler = candidate.create_education_command_handler
    create_experience_command_handler = candidate.create_experience_command_handler
    create_general_resume_command_handler = candidate.create_general_resume_command_handler
    create_project_command_handler = candidate.create_project_command_handler
    delete_education_command_handler = candidate.delete_education_command_handler
    delete_experience_command_handler = candidate.delete_experience_command_handler
    delete_project_command_handler = candidate.delete_project_command_handler
    delete_resume_command_handler = candidate.delete_resume_command_handler
    get_applications_by_candidate_id_query_handler = candidate.get_applications_by_candidate_id_query_handler
    get_candidate_by_email_query_handler = candidate.get_candidate_by_email_query_handler
    get_candidate_by_id_query_handler = candidate.get_candidate_by_id_query_handler
    get_candidate_by_user_id_query_handler = candidate.get_candidate_by_user_id_query_handler
    get_education_by_id_query_handler = candidate.get_education_by_id_query_handler
    get_educations_by_candidate_id_query_handler = candidate.get_educations_by_candidate_id_query_handler
    get_experience_by_id_query_handler = candidate.get_experience_by_id_query_handler
    get_experiences_by_candidate_id_query_handler = candidate.get_experiences_by_candidate_id_query_handler
    get_my_assigned_tasks_query_handler = candidate.get_my_assigned_tasks_query_handler
    get_project_by_id_query_handler = candidate.get_project_by_id_query_handler
    get_projects_by_candidate_id_query_handler = candidate.get_projects_by_candidate_id_query_handler
    get_resume_by_id_query_handler = candidate.get_resume_by_id_query_handler
    get_resume_statistics_query_handler = candidate.get_resume_statistics_query_handler
    get_resumes_by_candidate_query_handler = candidate.get_resumes_by_candidate_query_handler
    list_candidate_educations_by_candidate_id_query_handler = candidate.list_candidate_educations_by_candidate_id_query_handler
    list_candidate_experiences_by_candidate_id_query_handler = candidate.list_candidate_experiences_by_candidate_id_query_handler
    list_candidate_projects_by_candidate_id_query_handler = candidate.list_candidate_projects_by_candidate_id_query_handler
    list_candidates_query_handler = candidate.list_candidates_query_handler
    move_candidate_to_stage_command_handler = candidate.move_candidate_to_stage_command_handler
    populate_candidate_from_pdf_analysis_command_handler = candidate.populate_candidate_from_pdf_analysis_command_handler
    unclaim_task_command_handler = candidate.unclaim_task_command_handler
    update_application_status_command_handler = candidate.update_application_status_command_handler
    update_candidate_basic_command_handler = candidate.update_candidate_basic_command_handler
    update_education_command_handler = candidate.update_education_command_handler
    update_experience_command_handler = candidate.update_experience_command_handler
    update_project_command_handler = candidate.update_project_command_handler
    update_resume_content_command_handler = candidate.update_resume_content_command_handler
    
    # JobPosition Handlers
    add_user_to_stage_command_handler = job_position.add_user_to_stage_command_handler
    assign_users_to_stage_command_handler = job_position.assign_users_to_stage_command_handler
    copy_workflow_assignments_command_handler = job_position.copy_workflow_assignments_command_handler
    create_job_position_command_handler = job_position.create_job_position_command_handler
    create_job_position_comment_command_handler = job_position.create_job_position_comment_command_handler
    delete_job_position_command_handler = job_position.delete_job_position_command_handler
    delete_job_position_comment_command_handler = job_position.delete_job_position_comment_command_handler
    get_assigned_users_query_handler = job_position.get_assigned_users_query_handler
    get_job_position_by_id_query_handler = job_position.get_job_position_by_id_query_handler
    get_job_position_workflow_query_handler = job_position.get_job_position_workflow_query_handler
    get_job_positions_stats_query_handler = job_position.get_job_positions_stats_query_handler
    get_public_job_position_query_handler = job_position.get_public_job_position_query_handler
    list_all_job_position_comments_query_handler = job_position.list_all_job_position_comments_query_handler
    list_job_position_activities_query_handler = job_position.list_job_position_activities_query_handler
    list_job_position_workflows_query_handler = job_position.list_job_position_workflows_query_handler
    list_job_positions_query_handler = job_position.list_job_positions_query_handler
    list_public_job_positions_query_handler = job_position.list_public_job_positions_query_handler
    list_published_job_positions_query_handler = job_position.list_published_job_positions_query_handler
    list_stage_assignments_query_handler = job_position.list_stage_assignments_query_handler
    mark_job_position_comment_as_pending_command_handler = job_position.mark_job_position_comment_as_pending_command_handler
    mark_job_position_comment_as_reviewed_command_handler = job_position.mark_job_position_comment_as_reviewed_command_handler
    move_job_position_to_stage_command_handler = job_position.move_job_position_to_stage_command_handler
    remove_user_from_stage_command_handler = job_position.remove_user_from_stage_command_handler
    update_job_position_command_handler = job_position.update_job_position_command_handler
    update_job_position_comment_command_handler = job_position.update_job_position_comment_command_handler
    update_job_position_custom_fields_command_handler = job_position.update_job_position_custom_fields_command_handler
    
    # Workflow Handlers
    activate_phase_command_handler = workflow.activate_phase_command_handler
    activate_stage_command_handler = workflow.activate_stage_command_handler
    activate_validation_rule_command_handler = workflow.activate_validation_rule_command_handler
    activate_workflow_command_handler = workflow.activate_workflow_command_handler
    add_custom_field_to_entity_command_handler = workflow.add_custom_field_to_entity_command_handler
    archive_phase_command_handler = workflow.archive_phase_command_handler
    archive_workflow_command_handler = workflow.archive_workflow_command_handler
    create_entity_customization_command_handler = workflow.create_entity_customization_command_handler
    create_phase_command_handler = workflow.create_phase_command_handler
    create_stage_command_handler = workflow.create_stage_command_handler
    create_validation_rule_command_handler = workflow.create_validation_rule_command_handler
    create_workflow_command_handler = workflow.create_workflow_command_handler
    deactivate_stage_command_handler = workflow.deactivate_stage_command_handler
    deactivate_validation_rule_command_handler = workflow.deactivate_validation_rule_command_handler
    deactivate_workflow_command_handler = workflow.deactivate_workflow_command_handler
    delete_entity_customization_command_handler = workflow.delete_entity_customization_command_handler
    delete_phase_command_handler = workflow.delete_phase_command_handler
    delete_stage_command_handler = workflow.delete_stage_command_handler
    delete_validation_rule_command_handler = workflow.delete_validation_rule_command_handler
    delete_workflow_command_handler = workflow.delete_workflow_command_handler
    get_custom_field_values_by_entity_query_handler = workflow.get_custom_field_values_by_entity_query_handler
    get_entity_customization_by_id_query_handler = workflow.get_entity_customization_by_id_query_handler
    get_entity_customization_query_handler = workflow.get_entity_customization_query_handler
    get_final_stages_query_handler = workflow.get_final_stages_query_handler
    get_initial_stage_query_handler = workflow.get_initial_stage_query_handler
    get_phase_by_id_query_handler = workflow.get_phase_by_id_query_handler
    get_stage_bottlenecks_query_handler = workflow.get_stage_bottlenecks_query_handler
    get_stage_by_id_query_handler = workflow.get_stage_by_id_query_handler
    get_validation_rule_by_id_query_handler = workflow.get_validation_rule_by_id_query_handler
    get_workflow_analytics_query_handler = workflow.get_workflow_analytics_query_handler
    get_workflow_by_id_query_handler = workflow.get_workflow_by_id_query_handler
    initialize_company_phases_command_handler = workflow.initialize_company_phases_command_handler
    list_custom_fields_by_entity_query_handler = workflow.list_custom_fields_by_entity_query_handler
    list_phases_by_company_query_handler = workflow.list_phases_by_company_query_handler
    list_stages_by_phase_query_handler = workflow.list_stages_by_phase_query_handler
    list_stages_by_workflow_query_handler = workflow.list_stages_by_workflow_query_handler
    list_validation_rules_by_field_query_handler = workflow.list_validation_rules_by_field_query_handler
    list_validation_rules_by_stage_query_handler = workflow.list_validation_rules_by_stage_query_handler
    list_workflows_by_company_query_handler = workflow.list_workflows_by_company_query_handler
    list_workflows_by_phase_query_handler = workflow.list_workflows_by_phase_query_handler
    reorder_stages_command_handler = workflow.reorder_stages_command_handler
    set_as_default_workflow_command_handler = workflow.set_as_default_workflow_command_handler
    unset_as_default_workflow_command_handler = workflow.unset_as_default_workflow_command_handler
    update_entity_customization_command_handler = workflow.update_entity_customization_command_handler
    update_phase_command_handler = workflow.update_phase_command_handler
    update_stage_command_handler = workflow.update_stage_command_handler
    update_validation_rule_command_handler = workflow.update_validation_rule_command_handler
    update_workflow_command_handler = workflow.update_workflow_command_handler
    
    # Exponer todos los providers del container antiguo para compatibilidad
    # Esto permite una migración gradual sin romper el código existente
    def __getattr__(self, name):
        """Delegate to old container for providers not yet migrated"""
        return getattr(self._old_container, name)
