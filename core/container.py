from dependency_injector import containers, providers

from core.database import SQLAlchemyDatabase
from core.event_bus import EventBus

# Solo imports esenciales para admin e interview templates
from adapters.http.admin.controllers.inverview_template_controller import InterviewTemplateController
from adapters.http.admin.controllers.company_controller import CompanyController
from adapters.http.admin.controllers import JobPositionController
from adapters.http.admin.controllers.job_position_workflow_controller import JobPositionWorkflowController
from adapters.http.admin.controllers.job_position_comment_controller import JobPositionCommentController
from adapters.http.admin.controllers.interview_controller import InterviewController
from adapters.http.shared.controllers.user import UserController

# Onboarding Controller
from adapters.http.candidate import OnboardingController
from adapters.http.candidate.controllers.candidate import CandidateController
from adapters.http.candidate.controllers.application_controller import ApplicationController
from adapters.http.company.controllers.task_controller import TaskController

# Admin Controllers
from adapters.http.admin.controllers.admin_candidate_controller import AdminCandidateController
from src.company.application.queries.get_companies_stats import GetCompaniesStatsQueryHandler

# Auth Application Layer
from src.user.application.commands.create_user_command import CreateUserCommandHandler
from src.user.application.commands.create_user_automatically_command import CreateUserAutomaticallyCommandHandler
from src.user.application.commands.create_user_from_landing import CreateUserFromLandingCommandHandler
from src.user.application.commands.request_password_reset_command import RequestPasswordResetCommandHandler
from src.user.application.commands.reset_password_with_token_command import ResetPasswordWithTokenCommandHandler
from src.user.application.commands.update_user_password_command import UpdateUserPasswordCommandHandler
from src.user.application.commands.update_user_language_command import UpdateUserLanguageCommandHandler
from src.user.application.queries.authenticate_user_query import AuthenticateUserQueryHandler
from src.user.application.queries.check_user_exists_query import CheckUserExistsQueryHandler
from src.user.application.queries.create_access_token_query import CreateAccessTokenQueryHandler
from src.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQueryHandler
from src.user.application.queries.get_user_language_query import GetUserLanguageQueryHandler

# Auth Infrastructure
from src.user.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

# Interview Template Application Layer
from src.interview.interview_template.application.queries.list_interview_templates import ListInterviewTemplatesQueryHandler
from src.interview.interview_template.application.queries.get_interview_template_by_id import GetInterviewTemplateByIdQueryHandler
from src.interview.interview_template.application.queries.get_interview_template_full_by_id import GetInterviewTemplateFullByIdQueryHandler
from src.interview.interview_template.application.queries.get_questions_by_section import GetQuestionsBySectionQueryHandler
from src.interview.interview_template.application.commands.create_interview_template import CreateInterviewTemplateCommandHandler
from src.interview.interview_template.application import UpdateInterviewTemplateCommandHandler
from src.interview.interview_template.application.commands.enable_interview_template import EnableInterviewTemplateCommandHandler
from src.interview.interview_template.application.commands.disable_interview_template import DisableInterviewTemplateCommandHandler
from src.interview.interview_template.application.commands.create_interview_template_section import CreateInterviewTemplateSectionCommandHandler
from src.interview.interview_template.application.commands.update_interview_template_section import UpdateInterviewTemplateSectionCommandHandler
from src.interview.interview_template.application.commands.enable_interview_template_section import EnableInterviewTemplateSectionCommandHandler
from src.interview.interview_template.application.commands.disable_interview_template_section import DisableInterviewTemplateSectionCommandHandler
from src.interview.interview_template.application.commands.delete_interview_template_section import DeleteInterviewTemplateSectionCommandHandler
from src.interview.interview_template.application.commands.move_section_up import MoveSectionUpCommandHandler
from src.interview.interview_template.application.commands.move_section_down import MoveSectionDownCommandHandler
from src.interview.interview_template.application.commands.create_interview_template_question import CreateInterviewTemplateQuestionCommandHandler
from src.interview.interview_template.application.commands.update_interview_template_question import UpdateInterviewTemplateQuestionCommandHandler
from src.interview.interview_template.application.commands.enable_interview_template_question import EnableInterviewTemplateQuestionCommandHandler
from src.interview.interview_template.application.commands.disable_interview_template_question import DisableInterviewTemplateQuestionCommandHandler
from src.interview.interview_template.application.commands.delete_interview_template import DeleteInterviewTemplateCommandHandler

# Interview Template Infrastructure
from src.interview.interview_template.infrastructure import InterviewTemplateRepository
from src.interview.interview_template.infrastructure.repositories.interview_template_section_repository import InterviewTemplateSectionRepository
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import InterviewTemplateQuestionRepository

# Interview Management Application Layer
from src.interview.interview.application.commands.create_interview import CreateInterviewCommandHandler
from src.interview.interview.application.commands.start_interview import StartInterviewCommandHandler
from src.interview.interview.application.commands.finish_interview import FinishInterviewCommandHandler
from src.interview.interview.application.commands.create_interview_answer import CreateInterviewAnswerCommandHandler
from src.interview.interview.application.commands.update_interview_answer import UpdateInterviewAnswerCommandHandler
from src.interview.interview.application.commands.score_interview_answer import ScoreInterviewAnswerCommandHandler
from src.interview.interview.application.queries.list_interviews import ListInterviewsQueryHandler
from src.interview.interview.application.queries.get_interview_by_id import GetInterviewByIdQueryHandler
from src.interview.interview.application.queries.get_interviews_by_candidate import GetInterviewsByCandidateQueryHandler
from src.interview.interview.application.queries.get_scheduled_interviews import GetScheduledInterviewsQueryHandler
from src.interview.interview.application.queries.get_interview_score_summary import GetInterviewScoreSummaryQueryHandler
from src.interview.interview.application.queries.get_answers_by_interview import GetAnswersByInterviewQueryHandler
from src.interview.interview.application.queries.get_interview_answer_by_id import GetInterviewAnswerByIdQueryHandler

# Interview Management Infrastructure
from src.interview.interview.Infrastructure.repositories.interview_repository import SQLAlchemyInterviewRepository as InterviewRepository
from src.interview.interview.Infrastructure.repositories.interview_answer_repository import SQLAlchemyInterviewAnswerRepository as InterviewAnswerRepository

# Company Application Layer - Commands
from src.company.application.commands.create_company_command import CreateCompanyCommandHandler
from src.company.application.commands.register_company_with_user_command import RegisterCompanyWithUserCommandHandler
from src.company.application.commands.link_user_to_company_command import LinkUserToCompanyCommandHandler
from src.company.application.commands.update_company_command import UpdateCompanyCommandHandler
from src.company.application.commands.upload_company_logo_command import UploadCompanyLogoCommandHandler
from src.company.application.commands.suspend_company_command import SuspendCompanyCommandHandler
from src.company.application.commands.activate_company_command import ActivateCompanyCommandHandler
from src.company.application.commands.delete_company_command import DeleteCompanyCommandHandler
from src.company.application.commands.add_company_user_command import AddCompanyUserCommandHandler
from src.company.application.commands.update_company_user_command import UpdateCompanyUserCommandHandler
from src.company.application.commands.activate_company_user_command import ActivateCompanyUserCommandHandler
from src.company.application.commands.deactivate_company_user_command import DeactivateCompanyUserCommandHandler
from src.company.application.commands.remove_company_user_command import RemoveCompanyUserCommandHandler
from src.company.application.commands.invite_company_user_command import InviteCompanyUserCommandHandler
from src.company.application.commands.accept_user_invitation_command import AcceptUserInvitationCommandHandler
from src.company.application.commands.assign_role_to_user_command import AssignRoleToUserCommandHandler

# Company Application Layer - Queries
from src.company.application.queries.get_company_by_id import GetCompanyByIdQueryHandler
from src.company.application.queries.get_company_by_domain import GetCompanyByDomainQueryHandler
from src.company.application.queries.get_company_by_slug import GetCompanyBySlugQueryHandler
from src.company.application.queries.list_companies import ListCompaniesQueryHandler
from src.company.application.queries.get_company_user_by_id import GetCompanyUserByIdQueryHandler
from src.company.application.queries.get_company_user_by_company_and_user import GetCompanyUserByCompanyAndUserQueryHandler
from src.company.application.queries.list_company_users_by_company import ListCompanyUsersByCompanyQueryHandler
from src.company.application.queries.authenticate_company_user_query import AuthenticateCompanyUserQueryHandler
from src.company.application.queries.get_user_invitation_query import GetUserInvitationQueryHandler
from src.company.application.queries.get_user_permissions_query import GetUserPermissionsQueryHandler
from src.company.application.queries.get_invitation_by_email_and_company_query import GetInvitationByEmailAndCompanyQueryHandler

# Company Infrastructure
from src.company.infrastructure.repositories.company_repository import CompanyRepository
from src.company.infrastructure.repositories.company_user_repository import CompanyUserRepository
from src.company.infrastructure.repositories.company_user_invitation_repository import CompanyUserInvitationRepository

# Company Presentation Controllers
from adapters.http.company.controllers.company_controller import CompanyController as CompanyManagementController
from adapters.http.company.controllers.company_user_controller import CompanyUserController

# CompanyRole Application Layer - Commands
from src.company_role.application.commands.create_role_command import CreateRoleCommandHandler
from src.company_role.application.commands.update_role_command import UpdateRoleCommandHandler
from src.company_role.application.commands.delete_role_command import DeleteRoleCommandHandler

# CompanyRole Application Layer - Queries
from src.company_role.application.queries.get_role_by_id import GetCompanyRoleByIdQueryHandler
from src.company_role.application.queries.list_roles_by_company import ListRolesByCompanyQueryHandler

# CompanyRole Infrastructure
from src.company_role.infrastructure.repositories.company_role_repository import CompanyRoleRepository

# CompanyRole Presentation Controllers
from adapters.http.company.controllers.company_role_controller import CompanyRoleController

# CompanyCandidate Application Layer - Commands
from src.company_candidate.application.commands.create_company_candidate_command import CreateCompanyCandidateCommandHandler
from src.company_candidate.application.commands.update_company_candidate_command import UpdateCompanyCandidateCommandHandler
from src.company_candidate.application.commands.confirm_company_candidate_command import ConfirmCompanyCandidateCommandHandler
from src.company_candidate.application.commands.reject_company_candidate_command import RejectCompanyCandidateCommandHandler
from src.company_candidate.application.commands.archive_company_candidate_command import ArchiveCompanyCandidateCommandHandler
from src.company_candidate.application.commands.transfer_ownership_command import TransferOwnershipCommandHandler
from src.company_candidate.application.commands.assign_workflow_command import AssignWorkflowCommandHandler
from src.company_candidate.application.commands.change_stage_command import ChangeStageCommandHandler
from src.company_candidate.application.commands.create_candidate_comment_command import CreateCandidateCommentCommandHandler
from src.company_candidate.application.commands.update_candidate_comment_command import UpdateCandidateCommentCommandHandler
from src.company_candidate.application.commands.delete_candidate_comment_command import DeleteCandidateCommentCommandHandler
from src.company_candidate.application.commands.mark_comment_as_pending_command import MarkCommentAsPendingCommandHandler
from src.company_candidate.application.commands.mark_comment_as_reviewed_command import MarkCandidateCommentAsReviewedCommandHandler

# CompanyCandidate Application Layer - Queries
from src.company_candidate.application.queries.get_company_candidate_by_id import GetCompanyCandidateByIdQueryHandler
from src.company_candidate.application.queries.get_company_candidate_by_id_with_candidate_info import GetCompanyCandidateByIdWithCandidateInfoQueryHandler
from src.company_candidate.application.queries.get_company_candidate_by_company_and_candidate import GetCompanyCandidateByCompanyAndCandidateQueryHandler
from src.company_candidate.application.queries.list_company_candidates_by_company import ListCompanyCandidatesByCompanyQueryHandler
from src.company_candidate.application.queries.list_company_candidates_by_candidate import ListCompanyCandidatesByCandidateQueryHandler
from src.company_candidate.application.queries.list_company_candidates_with_candidate_info import ListCompanyCandidatesWithCandidateInfoQueryHandler
from src.company_candidate.application.queries.get_candidate_comment_by_id import GetCandidateCommentByIdQueryHandler
from src.company_candidate.application.queries.list_candidate_comments_by_company_candidate import ListCandidateCommentsByCompanyCandidateQueryHandler
from src.company_candidate.application.queries.list_candidate_comments_by_stage import ListCandidateCommentsByStageQueryHandler
from src.company_candidate.application.queries.count_pending_comments_query import CountPendingCommentsQueryHandler

# CompanyCandidate Infrastructure
from src.company_candidate.infrastructure.repositories.company_candidate_repository import CompanyCandidateRepository
from src.company_candidate.infrastructure.repositories.candidate_comment_repository import CandidateCommentRepository

# CompanyCandidate Presentation Controllers
from src.company_candidate.presentation.controllers.company_candidate_controller import CompanyCandidateController
from src.company_candidate.presentation.controllers.candidate_comment_controller import CandidateCommentController

# CandidateApplicationWorkflow Application Layer - Commands
from src.workflow.application.commands.workflow.create_workflow_command import CreateWorkflowCommandHandler
from src.workflow.application.commands.workflow.update_workflow_command import UpdateWorkflowCommandHandler
from src.workflow.application.commands.workflow.activate_workflow_command import ActivateWorkflowCommandHandler
from src.workflow.application.commands.workflow.deactivate_workflow_command import DeactivateWorkflowCommandHandler
from src.workflow.application.commands.workflow.archive_workflow_command import ArchiveWorkflowCommandHandler
from src.workflow.application.commands.workflow.delete_workflow_command import DeleteWorkflowCommandHandler
from src.workflow.application.commands.workflow.set_as_default_workflow_command import SetAsDefaultWorkflowCommandHandler
from src.workflow.application.commands.workflow.unset_as_default_workflow_command import UnsetAsDefaultWorkflowCommandHandler
from src.workflow.application.commands.stage.create_stage_command import CreateStageCommandHandler
from src.workflow.application.commands.stage.update_stage_command import UpdateStageCommandHandler
from src.workflow.application.commands.stage.delete_stage_command import DeleteStageCommandHandler
from src.workflow.application.commands.stage.reorder_stages_command import ReorderStagesCommandHandler
from src.workflow.application.commands.stage.activate_stage_command import ActivateStageCommandHandler
from src.workflow.application.commands.stage.deactivate_stage_command import DeactivateStageCommandHandler
from src.customization.application.create_custom_field_command import CreateCustomFieldCommandHandler
from src.customization.application.update_custom_field_command import UpdateCustomFieldCommandHandler
from src.customization.application.delete_custom_field_command import DeleteCustomFieldCommandHandler
from src.customization.application.reorder_custom_field_command import ReorderCustomFieldCommandHandler
from src.customization.application.configure_stage_field_command import ConfigureStageFieldCommandHandler
from src.customization.application.update_field_visibility_command import UpdateFieldVisibilityCommandHandler

# CandidateApplicationWorkflow Application Layer - Queries
from src.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQueryHandler
from src.workflow.application.queries.workflow.list_workflows_by_company import ListWorkflowsByCompanyQueryHandler
from src.workflow.application.queries.workflow.list_workflows_by_phase import ListWorkflowsByPhaseQueryHandler
from src.workflow.application.queries.stage.get_stage_by_id import GetStageByIdQueryHandler
from src.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQueryHandler
from src.workflow.application.queries.stage.list_stages_by_phase import ListStagesByPhaseQueryHandler
from src.workflow.application.queries.stage.get_initial_stage import GetInitialStageQueryHandler
from src.workflow.application.queries.stage.get_final_stages import GetFinalStagesQueryHandler
from src.customization.application.get_custom_field_by_id import GetCustomFieldByIdQueryHandler
from src.customization.application.list_custom_fields_by_workflow import ListCustomFieldsByWorkflowQueryHandler
from src.customization.application.list_field_configurations_by_stage import ListFieldConfigurationsByStageQueryHandler
from src.customization.application.get_field_configuration_by_id import GetFieldConfigurationByIdQueryHandler
from src.customization.application.get_custom_field_values_by_company_candidate import GetCustomFieldValuesByCompanyCandidateQueryHandler
from src.customization.application.get_all_custom_field_values_by_company_candidate import GetAllCustomFieldValuesByCompanyCandidateQueryHandler
from src.customization.application.create_custom_field_value_command import CreateCustomFieldValueCommandHandler
from src.customization.application.update_custom_field_value_command import UpdateCustomFieldValueCommandHandler
from src.customization.application.delete_custom_field_value_command import DeleteCustomFieldValueCommandHandler
from src.customization.application.get_custom_field_value_by_id import GetCustomFieldValueByIdQueryHandler

# CandidateApplicationWorkflow Infrastructure
from src.workflow.infrastructure.repositories.workflow_stage_repository import WorkflowStageRepository
from src.customization.infrastructure.repositories.custom_field_repository import CustomFieldRepository
from src.customization.infrastructure.repositories.custom_field_value_repository import CustomFieldValueRepository
from src.customization.infrastructure.repositories.field_configuration_repository import FieldConfigurationRepository

# CandidateApplicationWorkflow Presentation Controllers
from adapters.http.workflow.controllers import WorkflowController
from adapters.http.workflow.controllers import WorkflowStageController
from src.customization.custom_field_value_controller import CustomFieldValueController
from src.customization.custom_field_controller import CustomFieldController

# FieldValidation Application Layer - Commands
from src.field_validation.application.commands.create_validation_rule_command import CreateValidationRuleCommandHandler
from src.field_validation.application.commands.update_validation_rule_command import UpdateValidationRuleCommandHandler
from src.field_validation.application.commands.delete_validation_rule_command import DeleteValidationRuleCommandHandler
from src.field_validation.application.commands.activate_validation_rule_command import ActivateValidationRuleCommandHandler
from src.field_validation.application.commands.deactivate_validation_rule_command import DeactivateValidationRuleCommandHandler

# FieldValidation Application Layer - Queries
from src.field_validation.application.queries.get_validation_rule_by_id_query import GetValidationRuleByIdQueryHandler
from src.field_validation.application.queries.list_validation_rules_by_stage_query import ListValidationRulesByStageQueryHandler
from src.field_validation.application.queries.list_validation_rules_by_field_query import ListValidationRulesByFieldQueryHandler

# FieldValidation Application Layer - Services
from src.field_validation.application.services.field_validation_service import FieldValidationService

# CandidateApplication Application Layer - Services
from src.candidate_application.application.services.stage_permission_service import StagePermissionService

# FieldValidation Infrastructure
from src.field_validation.infrastructure.repositories.validation_rule_repository import ValidationRuleRepository

# FieldValidation Presentation Controllers
from src.field_validation.presentation.controllers.validation_rule_controller import ValidationRuleController

# Job Position Application Layer
from src.job_position.application.commands.create_job_position import CreateJobPositionCommandHandler
from src.job_position.application.commands.update_job_position import UpdateJobPositionCommandHandler
from src.job_position.application.commands.delete_job_position import DeleteJobPositionCommandHandler
# Status management command handlers have been removed - use MoveJobPositionToStageCommandHandler instead
from src.job_position.application.commands.create_job_position_workflow import CreateJobPositionWorkflowCommandHandler
from src.job_position.application.commands.update_job_position_workflow import UpdateJobPositionWorkflowCommandHandler
from src.job_position.application.commands.delete_job_position_workflow_command import DeleteJobPositionWorkflowCommandHandler
from src.job_position.application.commands.move_job_position_to_stage import MoveJobPositionToStageCommandHandler
from src.job_position.application.commands.update_job_position_custom_fields import UpdateJobPositionCustomFieldsCommandHandler
from src.job_position.application.commands.create_job_position_comment_command import CreateJobPositionCommentCommandHandler
from src.job_position.application.commands.update_job_position_comment_command import UpdateJobPositionCommentCommandHandler
from src.job_position.application.commands.delete_job_position_comment_command import DeleteJobPositionCommentCommandHandler
from src.job_position.application.commands.mark_comment_as_reviewed_command import MarkJobPositionCommentAsReviewedCommandHandler
from src.job_position.application.commands.mark_comment_as_pending_command import MarkJobPositionCommentAsPendingCommandHandler
from src.job_position.application.queries.list_job_positions import ListJobPositionsQueryHandler
from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQueryHandler
from src.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQueryHandler
# Phase 10: Public position queries
from src.job_position.application.queries.list_public_job_positions import ListPublicJobPositionsQueryHandler
from src.job_position.application.queries.get_public_job_position import GetPublicJobPositionQueryHandler
from src.job_position.application.queries.get_job_position_workflow import GetJobPositionWorkflowQueryHandler
from src.job_position.application.queries.list_job_position_workflows import ListJobPositionWorkflowsQueryHandler
from src.job_position.application.queries.list_job_position_comments_query import ListJobPositionCommentsQueryHandler
from src.job_position.application.queries.list_all_job_position_comments_query import ListAllJobPositionCommentsQueryHandler
from src.job_position.application.queries.list_job_position_activities_query import ListJobPositionActivitiesQueryHandler

# Job Position Infrastructure
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepository
from src.job_position.infrastructure.repositories.job_position_workflow_repository import JobPositionWorkflowRepository
from src.job_position.infrastructure.repositories.job_position_comment_repository import JobPositionCommentRepository
from src.job_position.infrastructure.repositories.job_position_activity_repository import JobPositionActivityRepository

# Phase 10: Public Position Controller
from src.job_position.presentation.controllers.public_position_controller import PublicPositionController

# Phase 12: Phase Application Layer - Commands
from src.phase.application.commands.create_phase_command import CreatePhaseCommandHandler
from src.phase.application.commands.update_phase_command import UpdatePhaseCommandHandler
from src.phase.application.commands.delete_phase_command import DeletePhaseCommandHandler
from src.phase.application.commands.archive_phase_command import ArchivePhaseCommandHandler
from src.phase.application.commands.activate_phase_command import ActivatePhaseCommandHandler
from src.phase.application.commands.initialize_company_phases_command import InitializeCompanyPhasesCommandHandler

# Phase 12: Phase Application Layer - Queries
from src.phase.application.queries.get_phase_by_id_query import GetPhaseByIdQueryHandler
from src.phase.application.queries.list_phases_by_company_query import ListPhasesByCompanyQueryHandler

# Phase 12: Phase Infrastructure
from src.phase.infrastructure.repositories.phase_repository import PhaseRepository

# Phase 12: Phase Presentation Controllers
from src.phase.presentation.controllers.phase_controller import PhaseController

# Phase 12: Phase Handlers
from src.phase.application.handlers.candidate_stage_transition_handler import CandidateStageTransitionHandler

# Position Stage Assignment Application Layer - Commands
from src.position_stage_assignment.application import (
    AssignUsersToStageCommandHandler,
    AddUserToStageCommandHandler,
    RemoveUserFromStageCommandHandler,
    CopyWorkflowAssignmentsCommandHandler
)

# Position Stage Assignment Application Layer - Queries
from src.position_stage_assignment.application import (
    ListStageAssignmentsQueryHandler,
    GetAssignedUsersQueryHandler
)

# Position Stage Assignment Infrastructure
from src.position_stage_assignment.infrastructure import PositionStageAssignmentRepository

# Position Stage Assignment Presentation
from src.position_stage_assignment.presentation.controllers import PositionStageAssignmentController

# Onboarding dependencies - SIMPLIFIED for landing endpoint only
from src.user.infrastructure.repositories.user_asset_repository import SQLAlchemyUserAssetRepository
from src.user.infrastructure.services.pdf_processing_service import PDFProcessingService
from src.candidate.application.commands.create_candidate import CreateCandidateCommandHandler
from src.candidate.application.commands.update_candidate_basic import UpdateCandidateCommandHandler
from src.candidate.application.queries.get_candidate_by_user_id import GetCandidateByUserIdQueryHandler
from src.candidate.application.queries.get_candidate_by_id import GetCandidateByIdQueryHandler
from src.candidate.application.queries.list_candidates import ListCandidatesQueryHandler
from src.candidate.application.queries.get_experiences_by_candidate_id import GetExperiencesByCandidateIdQueryHandler
from src.candidate.application.queries.list_candidate_experiences_by_candidate_id import ListCandidateExperiencesByCandidateIdQueryHandler
from src.candidate.application.queries.get_educations_by_candidate_id import GetEducationsByCandidateIdQueryHandler
from src.candidate.application.queries.list_candidate_educations_by_candidate_id import ListCandidateEducationsByCandidateIdQueryHandler
from src.candidate.application.queries.get_projects_by_candidate_id import GetProjectsByCandidateIdQueryHandler
from src.candidate.application.queries.list_candidate_projects_by_candidate_id import ListCandidateProjectsByCandidateIdQueryHandler
from src.candidate.application.queries.get_experience_by_id import GetExperienceByIdQueryHandler
from src.candidate.application.queries.get_education_by_id import GetEducationByIdQueryHandler
from src.candidate.application.queries.get_project_by_id import GetProjectByIdQueryHandler
from src.candidate.application.queries.admin_list_candidates import AdminListCandidatesQueryHandler
from src.candidate.application.commands.create_experience import CreateExperienceCommandHandler
from src.candidate.application.commands.update_experience import UpdateExperienceCommandHandler
from src.candidate.application.commands.delete_experience import DeleteExperienceCommandHandler
from src.candidate.application.commands.create_education import CreateEducationCommandHandler
from src.candidate.application.commands.update_education import UpdateEducationCommandHandler
from src.candidate.application.commands.delete_education import DeleteEducationCommandHandler
from src.candidate.application.commands.create_project import CreateProjectCommandHandler
from src.candidate.application.commands.update_project import UpdateProjectCommandHandler
from src.candidate.application.commands.delete_project import DeleteProjectCommandHandler
from src.candidate.application.commands.populate_candidate_from_pdf_analysis import PopulateCandidateFromPdfAnalysisCommandHandler
from src.candidate.infrastructure.repositories.candidate_repository import SQLAlchemyCandidateRepository
from src.candidate.infrastructure.repositories.candidate_experience_repository import SQLAlchemyCandidateExperienceRepository
from src.candidate.infrastructure.repositories.candidate_education_repository import SQLAlchemyCandidateEducationRepository
from src.candidate.infrastructure.repositories.candidate_project_repository import SQLAlchemyCandidateProjectRepository
from src.candidate_application.application.commands.create_candidate_application import CreateCandidateApplicationCommandHandler
from src.candidate_application.application.commands.update_application_status import UpdateApplicationStatusCommandHandler
from src.candidate_application.application.queries.get_applications_by_candidate_id import GetApplicationsByCandidateIdQueryHandler
# Phase 6: Task Management
from src.candidate_application.application.queries.get_my_assigned_tasks_query import GetMyAssignedTasksQueryHandler
from src.candidate_application.application.commands.claim_task_command import ClaimTaskCommandHandler
from src.candidate_application.application.commands.unclaim_task_command import UnclaimTaskCommandHandler
from src.candidate_application.infrastructure.repositories.candidate_application_repository import SQLAlchemyCandidateApplicationRepository

# Phase 12: Candidate Stage Tracking and Phase Transitions
from src.candidate_application.application.commands.move_candidate_to_stage_command import MoveCandidateToStageCommandHandler
from src.candidate_application_stage.infrastructure.repositories.candidate_application_stage_repository import CandidateApplicationStageRepository

# Phase 7: Email Template Management
from src.email_template.application.commands.create_email_template_command import CreateEmailTemplateCommandHandler
from src.email_template.application.commands.update_email_template_command import UpdateEmailTemplateCommandHandler
from src.email_template.application.commands.delete_email_template_command import DeleteEmailTemplateCommandHandler
from src.email_template.application.commands.activate_email_template_command import ActivateEmailTemplateCommandHandler
from src.email_template.application.commands.deactivate_email_template_command import DeactivateEmailTemplateCommandHandler
from src.email_template.application.queries.get_email_template_by_id_query import GetEmailTemplateByIdQueryHandler
from src.email_template.application.queries.list_email_templates_by_workflow_query import ListEmailTemplatesByWorkflowQueryHandler
from src.email_template.application.queries.list_email_templates_by_stage_query import ListEmailTemplatesByStageQueryHandler
from src.email_template.application.queries.get_email_templates_by_trigger_query import GetEmailTemplatesByTriggerQueryHandler
from src.email_template.infrastructure.repositories.email_template_repository import EmailTemplateRepository
from src.email_template.application.handlers.send_stage_transition_email_handler import SendStageTransitionEmailHandler
from adapters.http.company.controllers.email_template_controller import EmailTemplateController

# Phase 8: Talent Pool Management
from src.talent_pool.application.commands.add_to_talent_pool_command import AddToTalentPoolCommandHandler
from src.talent_pool.application.commands.update_talent_pool_entry_command import UpdateTalentPoolEntryCommandHandler
from src.talent_pool.application.commands.remove_from_talent_pool_command import RemoveFromTalentPoolCommandHandler
from src.talent_pool.application.commands.change_talent_pool_entry_status_command import ChangeTalentPoolEntryStatusCommandHandler
from src.talent_pool.application.queries.list_talent_pool_entries_query import ListTalentPoolEntriesQueryHandler
from src.talent_pool.application.queries.get_talent_pool_entry_by_id_query import GetTalentPoolEntryByIdQueryHandler
from src.talent_pool.application.queries.search_talent_pool_query import SearchTalentPoolQueryHandler
from src.talent_pool.infrastructure.repositories.talent_pool_entry_repository import TalentPoolEntryRepository
from src.talent_pool.presentation.controllers.talent_pool_controller import TalentPoolController

# Phase 9: Workflow Analytics
from src.workflow_analytics.application.queries.get_workflow_analytics_query import GetWorkflowAnalyticsQueryHandler
from src.workflow_analytics.application.queries.get_stage_bottlenecks_query import GetStageBottlenecksQueryHandler
from src.workflow_analytics.presentation.controllers.workflow_analytics_controller import WorkflowAnalyticsController

# Email Services
from src.notification.infrastructure.services.smtp_email_service import SMTPEmailService
from src.notification.infrastructure.services.mailgun_service import MailgunService
from src.notification.application.handlers.send_email_command_handler import SendEmailCommandHandler

# Storage Services
from src.shared.infrastructure.storage.storage_factory import StorageFactory

from core.config import settings

# Command and Query Buses
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus

# Async Job Infrastructure
from src.shared.infrastructure.jobs.async_job_service import AsyncJobService
from src.shared.infrastructure.repositories.async_job_repository import AsyncJobRepository
from src.resume.application.commands.analyze_pdf_resume_command import AnalyzePDFResumeCommandHandler


class Container(containers.DeclarativeContainer):
    """Container for admin + interview templates + auth"""

    # Core services
    database = providers.Singleton(SQLAlchemyDatabase)

    event_bus = providers.Singleton(EventBus)

    # Auth Services
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        database=database
    )

    # Email service - automatically selects SMTP or Mailgun based on settings
    @staticmethod
    def _get_email_service():
        """Factory method to create the appropriate email service based on configuration"""
        if settings.EMAIL_SERVICE == "mailgun":
            return MailgunService()
        else:
            return SMTPEmailService()

    email_service = providers.Singleton(_get_email_service)

    # AI service - automatically selects xAI or Groq based on settings
    @staticmethod
    def _get_ai_service():
        """Factory method to create the appropriate AI service based on configuration"""
        # Lazy import to avoid circular dependencies
        if settings.AI_AGENT.lower() == "groq":
            from src.shared.infrastructure.services.ai.groq_service import GroqResumeAnalysisService
            return GroqResumeAnalysisService()
        else:
            from src.shared.infrastructure.services.ai.xai_service import XAIResumeAnalysisService
            return XAIResumeAnalysisService()

    ai_service = providers.Singleton(_get_ai_service)

    # Storage service - automatically selects Local or S3 based on settings
    @staticmethod
    def _get_storage_service():
        """Factory method to create the appropriate storage service based on configuration"""
        from src.shared.domain.infrastructure.storage_service_interface import StorageConfig

        # Create storage config from settings
        allowed_extensions = [ext.strip() for ext in settings.ALLOWED_FILE_EXTENSIONS.split(',')]
        config = StorageConfig(
            max_file_size_mb=settings.MAX_FILE_SIZE_MB,
            allowed_extensions=allowed_extensions
        )

        return StorageFactory.create_storage_service(
            storage_type=settings.STORAGE_TYPE,
            config=config
        )

    storage_service = providers.Singleton(_get_storage_service)

    # Repositories - Using concrete implementation but typed as interface
    interview_template_repository = providers.Factory(
        InterviewTemplateRepository,  # Concrete implementation
        database=database
    )

    interview_template_section_repository = providers.Factory(
        InterviewTemplateSectionRepository,  # Concrete implementation
        database=database
    )

    interview_template_question_repository = providers.Factory(
        InterviewTemplateQuestionRepository,  # Concrete implementation
        database=database
    )

    # Interview Management Repositories
    interview_repository = providers.Factory(
        InterviewRepository,
        database=database
    )

    interview_answer_repository = providers.Factory(
        InterviewAnswerRepository,
        database=database
    )

    # Company Repositories
    company_repository = providers.Factory(
        CompanyRepository,
        database=database
    )

    company_user_repository = providers.Factory(
        CompanyUserRepository,
        database=database
    )

    company_user_invitation_repository = providers.Factory(
        CompanyUserInvitationRepository,
        database=database
    )

    # CompanyRole Repository
    company_role_repository = providers.Factory(
        CompanyRoleRepository,
        database=database
    )

    # CompanyCandidate Repository
    company_candidate_repository = providers.Factory(
        CompanyCandidateRepository,
        database=database
    )

    # CandidateApplicationWorkflow Repositories
    candidate_application_workflow_repository = providers.Factory(
        CandidateApplicationWorkflowRepository,
        database=database
    )

    workflow_stage_repository = providers.Factory(
        WorkflowStageRepository,
        database=database
    )

    custom_field_repository = providers.Factory(
        CustomFieldRepository,
        database=database
    )

    custom_field_value_repository = providers.Factory(
        CustomFieldValueRepository,
        database=database
    )

    field_configuration_repository = providers.Factory(
        FieldConfigurationRepository,
        database=database
    )

    # FieldValidation Repository
    validation_rule_repository = providers.Factory(
        ValidationRuleRepository
    )

    # Job Position Repository
    job_position_repository = providers.Factory(
        JobPositionRepository,
        database=database
    )

    # Job Position Workflow Repository
    job_position_workflow_repository = providers.Factory(
        JobPositionWorkflowRepository,
        database=database
    )

    job_position_comment_repository = providers.Factory(
        JobPositionCommentRepository,
        database=database
    )

    job_position_activity_repository = providers.Factory(
        JobPositionActivityRepository,
        database=database
    )

    # Position Stage Assignment Repository
    position_stage_assignment_repository = providers.Factory(
        PositionStageAssignmentRepository,
        database=database
    )

    # Phase 12: Phase Repository
    phase_repository = providers.Factory(
        PhaseRepository,
        database=database
    )

    # Phase 7: Email Template Repository
    email_template_repository = providers.Factory(
        EmailTemplateRepository,
        database=database
    )

    # Phase 8: Talent Pool Repository
    talent_pool_repository = providers.Factory(
        TalentPoolEntryRepository,
        database=database
    )

    # Onboarding Repositories - SIMPLIFIED
    user_asset_repository = providers.Factory(
        SQLAlchemyUserAssetRepository,
        database=database
    )

    candidate_repository = providers.Factory(
        SQLAlchemyCandidateRepository,
        database=database
    )

    # Candidate Experience, Education, Project Repositories
    candidate_experience_repository = providers.Factory(
        SQLAlchemyCandidateExperienceRepository,
        database=database
    )

    candidate_education_repository = providers.Factory(
        SQLAlchemyCandidateEducationRepository,
        database=database
    )

    candidate_project_repository = providers.Factory(
        SQLAlchemyCandidateProjectRepository,
        database=database
    )

    # Resume Repository and Services
    resume_repository = providers.Factory(
        'src.resume.infrastructure.repositories.resume_repository.SQLAlchemyResumeRepository',
        database=database
    )

    resume_generation_service = providers.Factory(
        'src.resume.application.services.resume_generation_service.ResumeGenerationService'
    )

    candidate_application_repository = providers.Factory(
        SQLAlchemyCandidateApplicationRepository,
        database=database
    )

    # Phase 12: Candidate Stage Repository
    candidate_stage_repository = providers.Factory(
        CandidateApplicationStageRepository,
        session=database.provided.session
    )

    # Onboarding Services - SIMPLIFIED
    pdf_processing_service = providers.Factory(PDFProcessingService)

    # Async Job Services
    async_job_repository = providers.Factory(
        AsyncJobRepository,
        database=database
    )

    async_job_service = providers.Factory(
        AsyncJobService,
        repository=async_job_repository
    )

    # mailgun_service = providers.Factory(MailgunService)

    # Auth Query Handlers
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
        CreateAccessTokenQueryHandler,
    )

    get_user_language_query_handler = providers.Factory(
        GetUserLanguageQueryHandler,
        user_repository=user_repository
    )


    # Interview Template Query Handlers
    list_interview_templates_query_handler = providers.Factory(
        ListInterviewTemplatesQueryHandler,
        interview_template_repository=interview_template_repository
    )

    get_interview_template_by_id_query_handler = providers.Factory(
        GetInterviewTemplateByIdQueryHandler,
        interview_template_repository=interview_template_repository
    )

    get_interview_template_full_by_id_query_handler = providers.Factory(
        GetInterviewTemplateFullByIdQueryHandler,
        interview_template_repository=interview_template_repository,
        interview_template_section_repository=interview_template_section_repository,
        interview_template_question_repository=interview_template_question_repository
    )

    get_questions_by_section_query_handler = providers.Factory(
        GetQuestionsBySectionQueryHandler,
        interview_template_question_repository=interview_template_question_repository
    )

    # Interview Management Query Handlers
    list_interviews_query_handler = providers.Factory(
        ListInterviewsQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_by_id_query_handler = providers.Factory(
        GetInterviewByIdQueryHandler,
        interview_repository=interview_repository
    )

    get_interviews_by_candidate_query_handler = providers.Factory(
        GetInterviewsByCandidateQueryHandler,
        interview_repository=interview_repository
    )

    get_scheduled_interviews_query_handler = providers.Factory(
        GetScheduledInterviewsQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_score_summary_query_handler = providers.Factory(
        GetInterviewScoreSummaryQueryHandler,
        interview_repository=interview_repository,
        interview_answer_repository=interview_answer_repository
    )

    get_answers_by_interview_query_handler = providers.Factory(
        GetAnswersByInterviewQueryHandler,
        interview_answer_repository=interview_answer_repository
    )

    get_interview_answer_by_id_query_handler = providers.Factory(
        GetInterviewAnswerByIdQueryHandler,
        interview_answer_repository=interview_answer_repository
    )

    # Company Query Handlers
    get_company_by_id_query_handler = providers.Factory(
        GetCompanyByIdQueryHandler,
        company_repository=company_repository
    )

    get_company_by_domain_query_handler = providers.Factory(
        GetCompanyByDomainQueryHandler,
        company_repository=company_repository
    )

    get_company_by_slug_query_handler = providers.Factory(
        GetCompanyBySlugQueryHandler,
        company_repository=company_repository
    )

    list_companies_query_handler = providers.Factory(
        ListCompaniesQueryHandler,
        company_repository=company_repository
    )

    authenticate_company_user_query_handler = providers.Factory(
        AuthenticateCompanyUserQueryHandler,
        user_repository=user_repository,
        company_user_repository=company_user_repository
    )

    # Company User Query Handlers
    get_company_user_by_id_query_handler = providers.Factory(
        GetCompanyUserByIdQueryHandler,
        company_user_repository=company_user_repository,
        user_repository=user_repository
    )

    get_company_user_by_company_and_user_query_handler = providers.Factory(
        GetCompanyUserByCompanyAndUserQueryHandler,
        company_user_repository=company_user_repository,
        user_repository=user_repository
    )

    list_company_users_by_company_query_handler = providers.Factory(
        ListCompanyUsersByCompanyQueryHandler,
        company_user_repository=company_user_repository,
        user_repository=user_repository
    )

    get_user_invitation_query_handler = providers.Factory(
        GetUserInvitationQueryHandler,
        invitation_repository=company_user_invitation_repository
    )

    get_user_permissions_query_handler = providers.Factory(
        GetUserPermissionsQueryHandler,
        company_user_repository=company_user_repository
    )

    get_invitation_by_email_and_company_query_handler = providers.Factory(
        GetInvitationByEmailAndCompanyQueryHandler,
        invitation_repository=company_user_invitation_repository
    )

    get_companies_stats_query_handler = providers.Factory(
        GetCompaniesStatsQueryHandler,
        company_repository=company_repository
    )

    # CompanyRole Query Handlers
    get_role_by_id_query_handler = providers.Factory(
        GetCompanyRoleByIdQueryHandler,
        repository=company_role_repository
    )

    list_roles_by_company_query_handler = providers.Factory(
        ListRolesByCompanyQueryHandler,
        repository=company_role_repository
    )

    # CompanyCandidate Query Handlers
    get_company_candidate_by_id_query_handler = providers.Factory(
        GetCompanyCandidateByIdQueryHandler,
        repository=company_candidate_repository
    )

    get_company_candidate_by_id_with_candidate_info_query_handler = providers.Factory(
        GetCompanyCandidateByIdWithCandidateInfoQueryHandler,
        repository=company_candidate_repository
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
        repository=company_candidate_repository
    )

    # CandidateApplicationWorkflow Query Handlers
    get_workflow_by_id_query_handler = providers.Factory(
        GetWorkflowByIdQueryHandler,
        repository=candidate_application_workflow_repository
    )

    list_workflows_by_company_query_handler = providers.Factory(
        ListWorkflowsByCompanyQueryHandler,
        repository=candidate_application_workflow_repository
    )

    list_workflows_by_phase_query_handler = providers.Factory(
        ListWorkflowsByPhaseQueryHandler,
        repository=candidate_application_workflow_repository
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

    # CustomField Query Handlers
    get_custom_field_by_id_query_handler = providers.Factory(
        GetCustomFieldByIdQueryHandler,
        repository=custom_field_repository
    )

    list_custom_fields_by_workflow_query_handler = providers.Factory(
        ListCustomFieldsByWorkflowQueryHandler,
        repository=custom_field_repository
    )

    # FieldConfiguration Query Handlers
    list_field_configurations_by_stage_query_handler = providers.Factory(
        ListFieldConfigurationsByStageQueryHandler,
        repository=field_configuration_repository
    )

    get_field_configuration_by_id_query_handler = providers.Factory(
        GetFieldConfigurationByIdQueryHandler,
        repository=field_configuration_repository
    )

    get_custom_field_values_by_company_candidate_query_handler = providers.Factory(
        GetCustomFieldValuesByCompanyCandidateQueryHandler,
        custom_field_value_repository=custom_field_value_repository,
        custom_field_repository=custom_field_repository,
        company_candidate_repository=company_candidate_repository
    )

    get_all_custom_field_values_by_company_candidate_query_handler = providers.Factory(
        GetAllCustomFieldValuesByCompanyCandidateQueryHandler,
        custom_field_value_repository=custom_field_value_repository,
        custom_field_repository=custom_field_repository
    )

    # Custom Field Value Command Handlers
    create_custom_field_value_command_handler = providers.Factory(
        CreateCustomFieldValueCommandHandler,
        repository=custom_field_value_repository
    )

    update_custom_field_value_command_handler = providers.Factory(
        UpdateCustomFieldValueCommandHandler,
        repository=custom_field_value_repository
    )

    delete_custom_field_value_command_handler = providers.Factory(
        DeleteCustomFieldValueCommandHandler,
        repository=custom_field_value_repository
    )

    # Custom Field Value Query Handlers
    get_custom_field_value_by_id_query_handler = providers.Factory(
        GetCustomFieldValueByIdQueryHandler,
        repository=custom_field_value_repository
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

    # Phase 10: Public Position Query Handlers
    list_public_job_positions_query_handler = providers.Factory(
        ListPublicJobPositionsQueryHandler,
        job_position_repository=job_position_repository
    )

    get_public_job_position_query_handler = providers.Factory(
        GetPublicJobPositionQueryHandler,
        job_position_repository=job_position_repository
    )

    # Job Position Workflow Query Handlers
    get_job_position_workflow_query_handler = providers.Factory(
        GetJobPositionWorkflowQueryHandler,
        workflow_repository=job_position_workflow_repository
    )

    list_job_position_workflows_query_handler = providers.Factory(
        ListJobPositionWorkflowsQueryHandler,
        workflow_repository=job_position_workflow_repository
    )

    list_job_position_comments_query_handler = providers.Factory(
        ListJobPositionCommentsQueryHandler,
        comment_repository=job_position_comment_repository
    )

    list_all_job_position_comments_query_handler = providers.Factory(
        ListAllJobPositionCommentsQueryHandler,
        comment_repository=job_position_comment_repository
    )

    list_job_position_activities_query_handler = providers.Factory(
        ListJobPositionActivitiesQueryHandler,
        activity_repository=job_position_activity_repository
    )

    # Phase 12: Phase Query Handlers
    get_phase_by_id_query_handler = providers.Factory(
        GetPhaseByIdQueryHandler,
        phase_repository=phase_repository
    )

    list_phases_by_company_query_handler = providers.Factory(
        ListPhasesByCompanyQueryHandler,
        phase_repository=phase_repository
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

    # Auth Command Handlers
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
        email_service=email_service
    )

    reset_password_with_token_command_handler = providers.Factory(
        ResetPasswordWithTokenCommandHandler,
        user_repository=user_repository
    )

    # Admin User Management Command Handlers
    update_user_password_command_handler = providers.Factory(
        UpdateUserPasswordCommandHandler,
        user_repository=user_repository
    )

    update_user_language_command_handler = providers.Factory(
        UpdateUserLanguageCommandHandler,
        user_repository=user_repository
    )


    # Interview Template Command Handlers
    create_interview_template_command_handler = providers.Factory(
        CreateInterviewTemplateCommandHandler,
        interview_template_repository=interview_template_repository
    )

    update_interview_template_command_handler = providers.Factory(
        UpdateInterviewTemplateCommandHandler,
        template_repository=interview_template_repository
    )

    enable_interview_template_command_handler = providers.Factory(
        EnableInterviewTemplateCommandHandler,
        template_repository=interview_template_repository
    )

    disable_interview_template_command_handler = providers.Factory(
        DisableInterviewTemplateCommandHandler,
        template_repository=interview_template_repository
    )

    # Interview Template Section Command Handlers
    create_interview_template_section_command_handler = providers.Factory(
        CreateInterviewTemplateSectionCommandHandler,
        interview_template_section_repository=interview_template_section_repository
    )

    update_interview_template_section_command_handler = providers.Factory(
        UpdateInterviewTemplateSectionCommandHandler,
        section_repository=interview_template_section_repository
    )

    enable_interview_template_section_command_handler = providers.Factory(
        EnableInterviewTemplateSectionCommandHandler,
        section_repository=interview_template_section_repository,
        question_repository=interview_template_question_repository
    )

    disable_interview_template_section_command_handler = providers.Factory(
        DisableInterviewTemplateSectionCommandHandler,
        section_repository=interview_template_section_repository
    )

    delete_interview_template_section_command_handler = providers.Factory(
        DeleteInterviewTemplateSectionCommandHandler,
        section_repository=interview_template_section_repository
    )

    move_section_up_command_handler = providers.Factory(
        MoveSectionUpCommandHandler,
        section_repository=interview_template_section_repository
    )

    move_section_down_command_handler = providers.Factory(
        MoveSectionDownCommandHandler,
        section_repository=interview_template_section_repository
    )

    # Question Command Handlers
    create_interview_template_question_command_handler = providers.Factory(
        CreateInterviewTemplateQuestionCommandHandler,
        interview_template_question_repository=interview_template_question_repository
    )

    update_interview_template_question_command_handler = providers.Factory(
        UpdateInterviewTemplateQuestionCommandHandler,
        interview_template_question_repository=interview_template_question_repository
    )

    enable_interview_template_question_command_handler = providers.Factory(
        EnableInterviewTemplateQuestionCommandHandler,
        interview_template_question_repository=interview_template_question_repository
    )

    disable_interview_template_question_command_handler = providers.Factory(
        DisableInterviewTemplateQuestionCommandHandler,
        interview_template_question_repository=interview_template_question_repository
    )

    delete_interview_template_command_handler = providers.Factory(
        DeleteInterviewTemplateCommandHandler,
        template_repository=interview_template_repository,
        section_repository=interview_template_section_repository
    )

    # Interview Management Command Handlers
    create_interview_command_handler = providers.Factory(
        CreateInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=event_bus
    )

    start_interview_command_handler = providers.Factory(
        StartInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=event_bus
    )

    finish_interview_command_handler = providers.Factory(
        FinishInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=event_bus
    )

    create_interview_answer_command_handler = providers.Factory(
        CreateInterviewAnswerCommandHandler,
        interview_answer_repository=interview_answer_repository,
        interview_repository=interview_repository
    )

    update_interview_answer_command_handler = providers.Factory(
        UpdateInterviewAnswerCommandHandler,
        interview_answer_repository=interview_answer_repository
    )

    score_interview_answer_command_handler = providers.Factory(
        ScoreInterviewAnswerCommandHandler,
        interview_answer_repository=interview_answer_repository
    )

    # Company Command Handlers


    update_company_command_handler = providers.Factory(
        UpdateCompanyCommandHandler,
        repository=company_repository
    )

    upload_company_logo_command_handler = providers.Factory(
        UploadCompanyLogoCommandHandler,
        repository=company_repository,
        storage_service=storage_service
    )

    suspend_company_command_handler = providers.Factory(
        SuspendCompanyCommandHandler,
        repository=company_repository
    )

    activate_company_command_handler = providers.Factory(
        ActivateCompanyCommandHandler,
        repository=company_repository
    )

    delete_company_command_handler = providers.Factory(
        DeleteCompanyCommandHandler,
        repository=company_repository
    )

    # Company User Command Handlers
    add_company_user_command_handler = providers.Factory(
        AddCompanyUserCommandHandler,
        repository=company_user_repository
    )

    update_company_user_command_handler = providers.Factory(
        UpdateCompanyUserCommandHandler,
        repository=company_user_repository
    )

    activate_company_user_command_handler = providers.Factory(
        ActivateCompanyUserCommandHandler,
        repository=company_user_repository
    )

    deactivate_company_user_command_handler = providers.Factory(
        DeactivateCompanyUserCommandHandler,
        repository=company_user_repository
    )

    remove_company_user_command_handler = providers.Factory(
        RemoveCompanyUserCommandHandler,
        repository=company_user_repository
    )

    invite_company_user_command_handler = providers.Factory(
        InviteCompanyUserCommandHandler,
        invitation_repository=company_user_invitation_repository,
        company_user_repository=company_user_repository,
        company_repository=company_repository,
        email_service=email_service
    )

    accept_user_invitation_command_handler = providers.Factory(
        AcceptUserInvitationCommandHandler,
        invitation_repository=company_user_invitation_repository,
        company_user_repository=company_user_repository,
        user_repository=user_repository
    )

    assign_role_to_user_command_handler = providers.Factory(
        AssignRoleToUserCommandHandler,
        repository=company_user_repository,
        company_role_repository=company_role_repository
    )

    # CompanyRole Command Handlers
    create_role_command_handler = providers.Factory(
        CreateRoleCommandHandler,
        repository=company_role_repository
    )

    update_role_command_handler = providers.Factory(
        UpdateRoleCommandHandler,
        repository=company_role_repository
    )

    delete_role_command_handler = providers.Factory(
        DeleteRoleCommandHandler,
        repository=company_role_repository
    )

    # CompanyCandidate Command Handlers
    create_company_candidate_command_handler = providers.Factory(
        CreateCompanyCandidateCommandHandler,
        repository=company_candidate_repository,
        workflow_repository=candidate_application_workflow_repository,
        stage_repository=workflow_stage_repository
    )

    update_company_candidate_command_handler = providers.Factory(
        UpdateCompanyCandidateCommandHandler,
        repository=company_candidate_repository
    )

    confirm_company_candidate_command_handler = providers.Factory(
        ConfirmCompanyCandidateCommandHandler,
        repository=company_candidate_repository
    )

    reject_company_candidate_command_handler = providers.Factory(
        RejectCompanyCandidateCommandHandler,
        repository=company_candidate_repository
    )

    archive_company_candidate_command_handler = providers.Factory(
        ArchiveCompanyCandidateCommandHandler,
        repository=company_candidate_repository
    )

    transfer_ownership_command_handler = providers.Factory(
        TransferOwnershipCommandHandler,
        repository=company_candidate_repository
    )

    assign_workflow_command_handler = providers.Factory(
        AssignWorkflowCommandHandler,
        repository=company_candidate_repository
    )

    change_stage_command_handler = providers.Factory(
        ChangeStageCommandHandler,
        repository=company_candidate_repository
    )

    # CandidateComment Repository
    candidate_comment_repository = providers.Factory(
        CandidateCommentRepository,
        database=database
    )

    # CandidateComment Command Handlers
    create_candidate_comment_command_handler = providers.Factory(
        CreateCandidateCommentCommandHandler,
        repository=candidate_comment_repository
    )

    update_candidate_comment_command_handler = providers.Factory(
        UpdateCandidateCommentCommandHandler,
        repository=candidate_comment_repository
    )

    delete_candidate_comment_command_handler = providers.Factory(
        DeleteCandidateCommentCommandHandler,
        repository=candidate_comment_repository
    )

    mark_comment_as_pending_command_handler = providers.Factory(
        MarkCommentAsPendingCommandHandler,
        repository=candidate_comment_repository
    )

    mark_candidate_comment_as_reviewed_command_handler = providers.Factory(
        MarkCandidateCommentAsReviewedCommandHandler,
        repository=candidate_comment_repository
    )

    # CandidateComment Query Handlers
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

    # CandidateApplicationWorkflow Command Handlers
    create_workflow_command_handler = providers.Factory(
        CreateWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    update_workflow_command_handler = providers.Factory(
        UpdateWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    activate_workflow_command_handler = providers.Factory(
        ActivateWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    deactivate_workflow_command_handler = providers.Factory(
        DeactivateWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    archive_workflow_command_handler = providers.Factory(
        ArchiveWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    delete_workflow_command_handler = providers.Factory(
        DeleteWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    set_as_default_workflow_command_handler = providers.Factory(
        SetAsDefaultWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
    )

    unset_as_default_workflow_command_handler = providers.Factory(
        UnsetAsDefaultWorkflowCommandHandler,
        repository=candidate_application_workflow_repository
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

    # CustomField Command Handlers
    create_custom_field_command_handler = providers.Factory(
        CreateCustomFieldCommandHandler,
        repository=custom_field_repository
    )

    update_custom_field_command_handler = providers.Factory(
        UpdateCustomFieldCommandHandler,
        repository=custom_field_repository
    )

    delete_custom_field_command_handler = providers.Factory(
        DeleteCustomFieldCommandHandler,
        repository=custom_field_repository
    )

    reorder_custom_field_command_handler = providers.Factory(
        ReorderCustomFieldCommandHandler,
        repository=custom_field_repository
    )

    # FieldConfiguration Command Handlers
    configure_stage_field_command_handler = providers.Factory(
        ConfigureStageFieldCommandHandler,
        repository=field_configuration_repository
    )

    update_field_visibility_command_handler = providers.Factory(
        UpdateFieldVisibilityCommandHandler,
        repository=field_configuration_repository
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

    # FieldValidation Service
    field_validation_service = providers.Factory(
        FieldValidationService,
        validation_rule_repository=validation_rule_repository,
        custom_field_repository=custom_field_repository
    )

    # StagePermission Service (Phase 5)
    stage_permission_service = providers.Factory(
        StagePermissionService,
        position_stage_assignment_repository=position_stage_assignment_repository
    )

    # Phase 12: Candidate Stage Transition Handler
    candidate_stage_transition_handler = providers.Factory(
        CandidateStageTransitionHandler,
        application_repository=candidate_application_repository,
        stage_repository=workflow_stage_repository,
        workflow_repository=candidate_application_workflow_repository
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
        candidate_application_repository= candidate_application_repository,

    )

    # Status management command handlers have been removed
    # Use MoveJobPositionToStageCommandHandler instead

    # Job Position Workflow Command Handlers
    create_job_position_workflow_command_handler = providers.Factory(
        CreateJobPositionWorkflowCommandHandler,
        workflow_repository=job_position_workflow_repository
    )

    update_job_position_workflow_command_handler = providers.Factory(
        UpdateJobPositionWorkflowCommandHandler,
        workflow_repository=job_position_workflow_repository
    )

    delete_job_position_workflow_command_handler = providers.Factory(
        DeleteJobPositionWorkflowCommandHandler,
        repository=job_position_workflow_repository
    )

    move_job_position_to_stage_command_handler = providers.Factory(
        MoveJobPositionToStageCommandHandler,
        job_position_repository=job_position_repository,
        workflow_repository=job_position_workflow_repository
    )

    update_job_position_custom_fields_command_handler = providers.Factory(
        UpdateJobPositionCustomFieldsCommandHandler,
        job_position_repository=job_position_repository
    )

    create_job_position_comment_command_handler = providers.Factory(
        CreateJobPositionCommentCommandHandler,
        comment_repository=job_position_comment_repository,
        activity_repository=job_position_activity_repository
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

    # Phase 12: Phase Command Handlers
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
        workflow_repository=candidate_application_workflow_repository,
        stage_repository=workflow_stage_repository
    )

    # Buses - MOVED BEFORE HANDLERS
    query_bus = providers.Factory(QueryBus)
    command_bus = providers.Factory(CommandBus)

    # Candidate Query Handlers
    # get_candidate_by_id_query_handler = providers.Factory(
    #     GetCandidateByIdQueryHandler,
    #     candidate_repository=candidate_repository
    # )

    create_company_command_handler = providers.Factory(
        CreateCompanyCommandHandler,
        repository=company_repository,
        command_bus=command_bus
    )

    register_company_with_user_command_handler = providers.Factory(
        RegisterCompanyWithUserCommandHandler,
        user_repository=user_repository,
        company_repository=company_repository,
        company_user_repository=company_user_repository,
        command_bus=command_bus
    )

    link_user_to_company_command_handler = providers.Factory(
        LinkUserToCompanyCommandHandler,
        user_repository=user_repository,
        company_repository=company_repository,
        company_user_repository=company_user_repository,
        command_bus=command_bus
    )

    # Onboarding Command Handlers - SIMPLIFIED



    create_user_from_landing_command_handler = providers.Factory(
        CreateUserFromLandingCommandHandler,
        user_repository=user_repository,
        user_asset_repository=user_asset_repository,
        pdf_processing_service=pdf_processing_service,
        command_bus=command_bus
    )

    create_candidate_command_handler = providers.Factory(
        CreateCandidateCommandHandler,
        candidate_repository=candidate_repository,
        event_bus=event_bus
    )

    update_candidate_basic_command_handler = providers.Factory(
        UpdateCandidateCommandHandler,
        candidate_repository=candidate_repository
    )

    get_candidate_by_user_id_query_handler = providers.Factory(
        GetCandidateByUserIdQueryHandler,
        candidate_repository=candidate_repository
    )

    get_candidate_by_id_query_handler = providers.Factory(
        GetCandidateByIdQueryHandler,
        candidate_repository=candidate_repository
    )

    list_candidates_query_handler = providers.Factory(
        ListCandidatesQueryHandler,
        candidate_repository=candidate_repository
    )

    admin_list_candidates_query_handler = providers.Factory(
        AdminListCandidatesQueryHandler,
        candidate_repository=candidate_repository
    )

    # Candidate Experience, Education, Project Query Handlers
    get_experiences_by_candidate_id_query_handler = providers.Factory(
        GetExperiencesByCandidateIdQueryHandler,
        experience_repository=candidate_experience_repository
    )

    list_candidate_experiences_by_candidate_id_query_handler = providers.Factory(
        ListCandidateExperiencesByCandidateIdQueryHandler,
        candidate_experience_repository=candidate_experience_repository
    )

    get_educations_by_candidate_id_query_handler = providers.Factory(
        GetEducationsByCandidateIdQueryHandler,
        education_repository=candidate_education_repository
    )

    list_candidate_educations_by_candidate_id_query_handler = providers.Factory(
        ListCandidateEducationsByCandidateIdQueryHandler,
        candidate_education_repository=candidate_education_repository
    )

    get_projects_by_candidate_id_query_handler = providers.Factory(
        GetProjectsByCandidateIdQueryHandler,
        project_repository=candidate_project_repository
    )

    list_candidate_projects_by_candidate_id_query_handler = providers.Factory(
        ListCandidateProjectsByCandidateIdQueryHandler,
        candidate_project_repository=candidate_project_repository
    )

    # Individual Item Query Handlers
    get_experience_by_id_query_handler = providers.Factory(
        GetExperienceByIdQueryHandler,
        experience_repository=candidate_experience_repository
    )

    get_education_by_id_query_handler = providers.Factory(
        GetEducationByIdQueryHandler,
        education_repository=candidate_education_repository
    )

    get_project_by_id_query_handler = providers.Factory(
        GetProjectByIdQueryHandler,
        project_repository=candidate_project_repository
    )

    # Candidate Experience Command Handlers
    create_experience_command_handler = providers.Factory(
        CreateExperienceCommandHandler,
        experience_repository=candidate_experience_repository
    )

    update_experience_command_handler = providers.Factory(
        UpdateExperienceCommandHandler,
        experience_repository=candidate_experience_repository
    )

    delete_experience_command_handler = providers.Factory(
        DeleteExperienceCommandHandler,
        experience_repository=candidate_experience_repository
    )

    # Candidate Education Command Handlers
    create_education_command_handler = providers.Factory(
        CreateEducationCommandHandler,
        education_repository=candidate_education_repository
    )

    update_education_command_handler = providers.Factory(
        UpdateEducationCommandHandler,
        education_repository=candidate_education_repository
    )

    delete_education_command_handler = providers.Factory(
        DeleteEducationCommandHandler,
        education_repository=candidate_education_repository
    )

    # Candidate Project Command Handlers
    create_project_command_handler = providers.Factory(
        CreateProjectCommandHandler,
        project_repository=candidate_project_repository
    )

    update_project_command_handler = providers.Factory(
        UpdateProjectCommandHandler,
        project_repository=candidate_project_repository
    )

    delete_project_command_handler = providers.Factory(
        DeleteProjectCommandHandler,
        project_repository=candidate_project_repository
    )

    # Populate candidate from PDF analysis
    populate_candidate_from_pdf_analysis_command_handler = providers.Factory(
        PopulateCandidateFromPdfAnalysisCommandHandler,
        candidate_repository=candidate_repository,
        command_bus=command_bus
    )

    # Resume Command Handlers
    create_general_resume_command_handler = providers.Factory(
        'src.resume.application.commands.create_general_resume_command.CreateGeneralResumeCommandHandler',
        resume_repository=resume_repository,
        candidate_repository=candidate_repository,
        generation_service=resume_generation_service,
        query_bus=query_bus
    )

    update_resume_content_command_handler = providers.Factory(
        'src.resume.application.commands.update_resume_content_command.UpdateResumeContentCommandHandler',
        resume_repository=resume_repository
    )

    delete_resume_command_handler = providers.Factory(
        'src.resume.application.commands.delete_resume_command.DeleteResumeCommandHandler',
        resume_repository=resume_repository
    )

    # Resume Query Handlers
    get_resumes_by_candidate_query_handler = providers.Factory(
        'src.resume.application.queries.get_resumes_by_candidate_query.GetResumesByCandidateQueryHandler',
        resume_repository=resume_repository
    )

    get_resume_by_id_query_handler = providers.Factory(
        'src.resume.application.queries.get_resume_by_id_query.GetResumeByIdQueryHandler',
        resume_repository=resume_repository
    )

    get_resume_statistics_query_handler = providers.Factory(
        'src.resume.application.queries.get_resume_statistics_query.GetResumeStatisticsQueryHandler',
        resume_repository=resume_repository
    )

    # PDF Analysis Command Handler
    analyze_pdf_resume_command_handler = providers.Factory(
        AnalyzePDFResumeCommandHandler,
        async_job_service=async_job_service
    )

    create_candidate_application_command_handler = providers.Factory(
        CreateCandidateApplicationCommandHandler,
        candidate_application_repository=candidate_application_repository
    )

    update_application_status_command_handler = providers.Factory(
        UpdateApplicationStatusCommandHandler,
        candidate_application_repository=candidate_application_repository
    )

    # Phase 12.12: Move Candidate to Stage with Automatic Phase Transitions
    move_candidate_to_stage_command_handler = providers.Factory(
        MoveCandidateToStageCommandHandler,
        candidate_application_repository=candidate_application_repository,
        candidate_stage_repository=candidate_stage_repository,
        workflow_stage_repository=workflow_stage_repository,
        job_position_repository=job_position_repository
    )

    get_applications_by_candidate_id_query_handler = providers.Factory(
        GetApplicationsByCandidateIdQueryHandler,
        candidate_application_repository=candidate_application_repository
    )

    # Phase 6: Task Management Query Handlers
    get_my_assigned_tasks_query_handler = providers.Factory(
        GetMyAssignedTasksQueryHandler,
        application_repository=candidate_application_repository,
        stage_assignment_repository=position_stage_assignment_repository
    )

    # Phase 6: Task Management Command Handlers
    claim_task_command_handler = providers.Factory(
        ClaimTaskCommandHandler,
        application_repository=candidate_application_repository
    )

    unclaim_task_command_handler = providers.Factory(
        UnclaimTaskCommandHandler,
        application_repository=candidate_application_repository
    )

    # Phase 7: Email Template Query Handlers
    get_email_template_by_id_query_handler = providers.Factory(
        GetEmailTemplateByIdQueryHandler,
        repository=email_template_repository
    )

    list_email_templates_by_workflow_query_handler = providers.Factory(
        ListEmailTemplatesByWorkflowQueryHandler,
        repository=email_template_repository
    )

    list_email_templates_by_stage_query_handler = providers.Factory(
        ListEmailTemplatesByStageQueryHandler,
        repository=email_template_repository
    )

    get_email_templates_by_trigger_query_handler = providers.Factory(
        GetEmailTemplatesByTriggerQueryHandler,
        repository=email_template_repository
    )

    # Phase 7: Email Template Command Handlers
    create_email_template_command_handler = providers.Factory(
        CreateEmailTemplateCommandHandler,
        repository=email_template_repository
    )

    update_email_template_command_handler = providers.Factory(
        UpdateEmailTemplateCommandHandler,
        repository=email_template_repository
    )

    delete_email_template_command_handler = providers.Factory(
        DeleteEmailTemplateCommandHandler,
        repository=email_template_repository
    )

    activate_email_template_command_handler = providers.Factory(
        ActivateEmailTemplateCommandHandler,
        repository=email_template_repository
    )

    deactivate_email_template_command_handler = providers.Factory(
        DeactivateEmailTemplateCommandHandler,
        repository=email_template_repository
    )

    # Phase 7: Email Template Event Handler
    send_stage_transition_email_handler = providers.Factory(
        SendStageTransitionEmailHandler,
        email_template_repository=email_template_repository,
        command_bus=command_bus
    )

    # Phase 8: Talent Pool Query Handlers
    list_talent_pool_entries_query_handler = providers.Factory(
        ListTalentPoolEntriesQueryHandler,
        repository=talent_pool_repository
    )

    get_talent_pool_entry_by_id_query_handler = providers.Factory(
        GetTalentPoolEntryByIdQueryHandler,
        repository=talent_pool_repository
    )

    search_talent_pool_query_handler = providers.Factory(
        SearchTalentPoolQueryHandler,
        repository=talent_pool_repository
    )

    # Phase 8: Talent Pool Command Handlers
    add_to_talent_pool_command_handler = providers.Factory(
        AddToTalentPoolCommandHandler,
        repository=talent_pool_repository
    )

    update_talent_pool_entry_command_handler = providers.Factory(
        UpdateTalentPoolEntryCommandHandler,
        repository=talent_pool_repository
    )

    remove_from_talent_pool_command_handler = providers.Factory(
        RemoveFromTalentPoolCommandHandler,
        repository=talent_pool_repository
    )

    change_talent_pool_entry_status_command_handler = providers.Factory(
        ChangeTalentPoolEntryStatusCommandHandler,
        repository=talent_pool_repository
    )

    # Phase 9: Workflow Analytics Query Handlers
    get_workflow_analytics_query_handler = providers.Factory(
        GetWorkflowAnalyticsQueryHandler,
        database=database,
        workflow_repository=candidate_application_workflow_repository,
        stage_repository=workflow_stage_repository
    )

    get_stage_bottlenecks_query_handler = providers.Factory(
        GetStageBottlenecksQueryHandler,
        database=database,
        workflow_repository=candidate_application_workflow_repository,
        stage_repository=workflow_stage_repository
    )

    # Email Command Handler
    send_email_command_handler = providers.Factory(
        SendEmailCommandHandler,
        email_service=email_service
    )

    # Controllers
    interview_template_controller = providers.Factory(
        InterviewTemplateController,
        query_bus=query_bus,
        command_bus=command_bus
    )

    company_controller = providers.Factory(
        CompanyController,
        query_bus=query_bus,
        command_bus=command_bus
    )

    company_management_controller = providers.Factory(
        CompanyManagementController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    company_user_controller = providers.Factory(
        CompanyUserController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    # Invitation Controller
    from adapters.http.invitations.controllers.invitation_controller import (
        InvitationController
    )
    invitation_controller = providers.Factory(
        InvitationController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    company_role_controller = providers.Factory(
        CompanyRoleController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    company_candidate_controller = providers.Factory(
        CompanyCandidateController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    candidate_comment_controller = providers.Factory(
        CandidateCommentController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    candidate_application_workflow_controller = providers.Factory(
        WorkflowController,
        command_bus=command_bus,
        query_bus=query_bus,
        database=database
    )

    workflow_stage_controller = providers.Factory(
        WorkflowStageController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    custom_field_controller = providers.Factory(
        CustomFieldController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    custom_field_value_controller = providers.Factory(
        CustomFieldValueController,
        command_bus=command_bus,
        query_bus=query_bus,
        custom_field_value_repository=custom_field_value_repository
    )

    validation_rule_controller = providers.Factory(
        ValidationRuleController,
        command_bus=command_bus,
        query_bus=query_bus,
        validation_service=field_validation_service
    )

    job_position_controller = providers.Factory(
        JobPositionController,
        query_bus=query_bus,
        command_bus=command_bus
    )

    job_position_workflow_controller = providers.Factory(
        JobPositionWorkflowController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    job_position_comment_controller = providers.Factory(
        JobPositionCommentController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    # Phase 10: Public Position Controller
    public_position_controller = providers.Factory(
        PublicPositionController,
        query_bus=query_bus
    )

    # Phase 12: Phase Controller
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

    position_stage_assignment_controller = providers.Factory(
        PositionStageAssignmentController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    onboarding_controller = providers.Factory(
        OnboardingController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    candidate_controller = providers.Factory(
        CandidateController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    resume_controller = providers.Factory(
        'src.resume.presentation.controllers.resume_controller.ResumeController',
        command_bus=command_bus,
        query_bus=query_bus
    )

    admin_candidate_controller = providers.Factory(
        AdminCandidateController,
        query_bus=query_bus,
        command_bus=command_bus,
        user_repository=user_repository,
        candidate_repository=candidate_repository
    )

    application_controller = providers.Factory(
        ApplicationController,
        command_bus=command_bus,
        query_bus=query_bus,
        stage_permission_service=stage_permission_service,
        application_repository=candidate_application_repository
    )

    # Phase 6: Task Management Controller
    task_controller = providers.Factory(
        TaskController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    # Phase 7: Email Template Controller
    email_template_controller = providers.Factory(
        EmailTemplateController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    # Phase 8: Talent Pool Controller
    talent_pool_controller = providers.Factory(
        TalentPoolController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    # Phase 9: Workflow Analytics Controller
    workflow_analytics_controller = providers.Factory(
        WorkflowAnalyticsController,
        query_bus=query_bus
    )

    # Company Pages Module
    company_page_repository = providers.Factory(
        'src.company_page.infrastructure.repositories.company_page_repository.CompanyPageRepository',
        database=database
    )

    # Company Pages Commands
    create_company_page_command_handler = providers.Factory(
        'src.company_page.application.commands.create_company_page_command_handler.CreateCompanyPageCommandHandler',
        repository=company_page_repository
    )

    update_company_page_command_handler = providers.Factory(
        'src.company_page.application.commands.update_company_page_command_handler.UpdateCompanyPageCommandHandler',
        repository=company_page_repository
    )

    publish_company_page_command_handler = providers.Factory(
        'src.company_page.application.commands.publish_company_page_command_handler.PublishCompanyPageCommandHandler',
        repository=company_page_repository
    )

    archive_company_page_command_handler = providers.Factory(
        'src.company_page.application.commands.archive_company_page_command_handler.ArchiveCompanyPageCommandHandler',
        repository=company_page_repository
    )

    set_default_page_command_handler = providers.Factory(
        'src.company_page.application.commands.set_default_page_command_handler.SetDefaultPageCommandHandler',
        repository=company_page_repository
    )

    delete_company_page_command_handler = providers.Factory(
        'src.company_page.application.commands.delete_company_page_command_handler.DeleteCompanyPageCommandHandler',
        repository=company_page_repository
    )

    # Company Pages Queries
    get_company_page_by_id_query_handler = providers.Factory(
        'src.company_page.application.queries.get_company_page_by_id_query_handler.GetCompanyPageByIdQueryHandler',
        repository=company_page_repository
    )

    get_company_page_by_type_query_handler = providers.Factory(
        'src.company_page.application.queries.get_company_page_by_type_query_handler.GetCompanyPageByTypeQueryHandler',
        repository=company_page_repository
    )

    list_company_pages_query_handler = providers.Factory(
        'src.company_page.application.queries.list_company_pages_query_handler.ListCompanyPagesQueryHandler',
        repository=company_page_repository
    )

    get_public_company_page_query_handler = providers.Factory(
        'src.company_page.application.queries.get_public_company_page_query_handler.GetPublicCompanyPageQueryHandler',
        repository=company_page_repository
    )

    # Company Pages Controller
    company_page_controller = providers.Factory(
        'src.company_page.presentation.controllers.company_page_controller.CompanyPageController',
        command_bus=command_bus,
        query_bus=query_bus
    )

    interview_controller = providers.Factory(
        InterviewController,
        command_bus=command_bus,
        query_bus=query_bus
    )

    user_controller = providers.Factory(
        UserController,
        command_bus=command_bus,
        query_bus=query_bus
    )