from dependency_injector import containers, providers

from core.database import SQLAlchemyDatabase
from core.event_bus import EventBus

# Solo imports esenciales para admin e interview templates
from adapters.http.admin.controllers.inverview_template_controller import InterviewTemplateController
from adapters.http.admin.controllers.company_controller import CompanyController
from adapters.http.admin.controllers import JobPositionController
from adapters.http.admin.controllers.interview_controller import InterviewController
from adapters.http.shared.controllers.user import UserController

# Onboarding Controller
from adapters.http.candidate import OnboardingController
from adapters.http.candidate.controllers.candidate import CandidateController
from adapters.http.candidate.controllers.application_controller import ApplicationController

# Admin Controllers
from adapters.http.admin.controllers.admin_candidate_controller import AdminCandidateController

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

# Company Application Layer
from src.company.application.commands.create_company import CreateCompanyCommandHandler
from src.company.application.commands.update_company import UpdateCompanyCommandHandler
from src.company.application.commands.approve_company import ApproveCompanyCommandHandler
from src.company.application.commands.reject_company import RejectCompanyCommandHandler
from src.company.application.commands.activate_company import ActivateCompanyCommandHandler
from src.company.application.commands.deactivate_company import DeactivateCompanyCommandHandler
from src.company.application.commands.delete_company import DeleteCompanyCommandHandler
from src.company.application.queries.list_companies import ListCompaniesQueryHandler
from src.company.application.queries.get_company_by_id import GetCompanyByIdQueryHandler
from src.company.application.queries.get_companies_stats import GetCompaniesStatsQueryHandler

# Company Infrastructure
from src.company.infrastructure.repositories.company_repository import CompanyRepository

# Job Position Application Layer
from src.job_position.application.commands.create_job_position import CreateJobPositionCommandHandler
from src.job_position.application.commands.update_job_position import UpdateJobPositionCommandHandler
from src.job_position.application.commands.delete_job_position import DeleteJobPositionCommandHandler
from src.job_position.application.queries.list_job_positions import ListJobPositionsQueryHandler
from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQueryHandler
from src.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQueryHandler

# Job Position Infrastructure
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepository

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
from src.candidate_application.infrastructure.repositories.candidate_application_repository import SQLAlchemyCandidateApplicationRepository

# Email Services
from src.notification.infrastructure.services.smtp_email_service import SMTPEmailService
from src.notification.infrastructure.services.mailgun_service import MailgunService
from src.notification.application.handlers.send_email_command_handler import SendEmailCommandHandler

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

    # Company Repository
    company_repository = providers.Factory(
        CompanyRepository,
        database=database
    )

    # Job Position Repository
    job_position_repository = providers.Factory(
        JobPositionRepository,
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
    list_companies_query_handler = providers.Factory(
        ListCompaniesQueryHandler,
        company_repository=company_repository
    )

    get_company_by_id_query_handler = providers.Factory(
        GetCompanyByIdQueryHandler,
        company_repository=company_repository
    )

    get_companies_stats_query_handler = providers.Factory(
        GetCompaniesStatsQueryHandler,
        company_repository=company_repository
    )

    # Job Position Query Handlers
    list_job_positions_query_handler = providers.Factory(
        ListJobPositionsQueryHandler,
        job_position_repository=job_position_repository
    )

    get_job_position_by_id_query_handler = providers.Factory(
        GetJobPositionByIdQueryHandler,
        job_position_repository=job_position_repository
    )

    get_job_positions_stats_query_handler = providers.Factory(
        GetJobPositionsStatsQueryHandler,
        job_position_repository=job_position_repository
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
    create_company_command_handler = providers.Factory(
        CreateCompanyCommandHandler,
        company_repository=company_repository
    )

    update_company_command_handler = providers.Factory(
        UpdateCompanyCommandHandler,
        company_repository=company_repository
    )

    approve_company_command_handler = providers.Factory(
        ApproveCompanyCommandHandler,
        company_repository=company_repository
    )

    reject_company_command_handler = providers.Factory(
        RejectCompanyCommandHandler,
        company_repository=company_repository
    )

    activate_company_command_handler = providers.Factory(
        ActivateCompanyCommandHandler,
        company_repository=company_repository
    )

    deactivate_company_command_handler = providers.Factory(
        DeactivateCompanyCommandHandler,
        company_repository=company_repository
    )

    delete_company_command_handler = providers.Factory(
        DeleteCompanyCommandHandler,
        company_repository=company_repository
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
        job_position_repository=job_position_repository
    )

    # Buses - MOVED BEFORE HANDLERS
    query_bus = providers.Factory(QueryBus)
    command_bus = providers.Factory(CommandBus)

    # Candidate Query Handlers
    # get_candidate_by_id_query_handler = providers.Factory(
    #     GetCandidateByIdQueryHandler,
    #     candidate_repository=candidate_repository
    # )

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

    get_applications_by_candidate_id_query_handler = providers.Factory(
        GetApplicationsByCandidateIdQueryHandler,
        candidate_application_repository=candidate_application_repository
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

    job_position_controller = providers.Factory(
        JobPositionController,
        query_bus=query_bus,
        command_bus=command_bus
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