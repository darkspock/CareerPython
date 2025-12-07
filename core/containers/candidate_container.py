"""Candidate Container - Candidate Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.candidate_app.controllers.candidate import CandidateController
from adapters.http.candidate_app.controllers.application_controller import ApplicationController
from adapters.http.candidate_app.controllers.onboarding_controller import OnboardingController
from adapters.http.candidate_app.controllers.resume_controller import ResumeController
from adapters.http.admin_app.controllers.admin_candidate_controller import AdminCandidateController
from adapters.http.candidate_app.application_answers.controllers.application_answer_controller import ApplicationAnswerController

# Candidate Infrastructure
from src.candidate_bc.candidate.infrastructure.repositories.candidate_repository import SQLAlchemyCandidateRepository
from src.candidate_bc.candidate.infrastructure.repositories.candidate_experience_repository import SQLAlchemyCandidateExperienceRepository
from src.candidate_bc.candidate.infrastructure.repositories.candidate_education_repository import SQLAlchemyCandidateEducationRepository
from src.candidate_bc.candidate.infrastructure.repositories.candidate_project_repository import SQLAlchemyCandidateProjectRepository
from src.company_bc.candidate_application.infrastructure.repositories.candidate_application_repository import SQLAlchemyCandidateApplicationRepository
from src.company_bc.candidate_application.infrastructure.repositories.application_question_answer_repository import ApplicationQuestionAnswerRepository
from src.company_bc.candidate_application_stage.infrastructure.repositories.candidate_application_stage_repository import CandidateApplicationStageRepository

# Candidate Application Layer - Commands
from src.candidate_bc.candidate.application.commands.create_candidate import CreateCandidateCommandHandler
from src.candidate_bc.candidate.application.commands.update_candidate_basic import UpdateCandidateCommandHandler
from src.candidate_bc.candidate.application.commands.create_experience import CreateExperienceCommandHandler
from src.candidate_bc.candidate.application.commands.update_experience import UpdateExperienceCommandHandler
from src.candidate_bc.candidate.application.commands.delete_experience import DeleteExperienceCommandHandler
from src.candidate_bc.candidate.application.commands.create_education import CreateEducationCommandHandler
from src.candidate_bc.candidate.application.commands.update_education import UpdateEducationCommandHandler
from src.candidate_bc.candidate.application.commands.delete_education import DeleteEducationCommandHandler
from src.candidate_bc.candidate.application.commands.create_project import CreateProjectCommandHandler
from src.candidate_bc.candidate.application.commands.update_project import UpdateProjectCommandHandler
from src.candidate_bc.candidate.application.commands.delete_project import DeleteProjectCommandHandler
from src.candidate_bc.candidate.application.commands.populate_candidate_from_pdf_analysis import PopulateCandidateFromPdfAnalysisCommandHandler

# Candidate Application Layer - Queries
from src.candidate_bc.candidate.application import GetCandidateByUserIdQueryHandler
from src.candidate_bc.candidate.application.queries.get_candidate_by_id import GetCandidateByIdQueryHandler
from src.candidate_bc.candidate.application.queries.get_candidate_by_email import GetCandidateByEmailQueryHandler
from src.candidate_bc.candidate.application.queries.list_candidates import ListCandidatesQueryHandler
from src.candidate_bc.candidate.application.queries.admin_list_candidates import AdminListCandidatesQueryHandler
from src.candidate_bc.candidate.application.queries.get_experiences_by_candidate_id import GetExperiencesByCandidateIdQueryHandler
from src.candidate_bc.candidate.application.queries.list_candidate_experiences_by_candidate_id import ListCandidateExperiencesByCandidateIdQueryHandler
from src.candidate_bc.candidate.application.queries.get_educations_by_candidate_id import GetEducationsByCandidateIdQueryHandler
from src.candidate_bc.candidate.application import ListCandidateEducationsByCandidateIdQueryHandler
from src.candidate_bc.candidate.application.queries.get_projects_by_candidate_id import GetProjectsByCandidateIdQueryHandler
from src.candidate_bc.candidate.application.queries.list_candidate_projects_by_candidate_id import ListCandidateProjectsByCandidateIdQueryHandler
from src.candidate_bc.candidate.application.queries.get_experience_by_id import GetExperienceByIdQueryHandler
from src.candidate_bc.candidate.application import GetEducationByIdQueryHandler
from src.candidate_bc.candidate.application import GetProjectByIdQueryHandler

# Candidate Application Commands
from src.company_bc.candidate_application.application.commands.create_candidate_application import CreateCandidateApplicationCommandHandler
from src.company_bc.candidate_application.application.commands.update_application_status import UpdateApplicationStatusCommandHandler
from src.company_bc.candidate_application.application.commands.move_candidate_to_stage_command import MoveCandidateToStageCommandHandler
from src.company_bc.candidate_application.application.commands.claim_task_command import ClaimTaskCommandHandler
from src.company_bc.candidate_application.application.commands.unclaim_task_command import UnclaimTaskCommandHandler

# Candidate Application Queries
from src.company_bc.candidate_application.application.queries.get_applications_by_candidate_id import GetApplicationsByCandidateIdQueryHandler
from src.company_bc.candidate_application.application.queries.get_my_assigned_tasks_query import GetMyAssignedTasksQueryHandler

# Application Question Answer Commands
from src.company_bc.candidate_application.application.commands.question_answer.save_application_answers_command import SaveApplicationAnswersCommandHandler
from src.company_bc.candidate_application.application.commands.question_answer.evaluate_application_answers_command import EvaluateApplicationAnswersCommandHandler

# Application Question Answer Queries
from src.company_bc.candidate_application.application.queries.question_answer.list_application_answers_query import ListApplicationAnswersQueryHandler

# Resume (using string imports for lazy loading)
RESUME_REPOSITORY_PATH = 'src.candidate_bc.resume.infrastructure.repositories.resume_repository.SQLAlchemyResumeRepository'
RESUME_GENERATION_SERVICE_PATH = 'src.candidate_bc.resume.application.services.resume_generation_service.ResumeGenerationService'
CREATE_GENERAL_RESUME_HANDLER_PATH = 'src.candidate_bc.resume.application.commands.create_general_resume_command.CreateGeneralResumeCommandHandler'
UPDATE_RESUME_CONTENT_HANDLER_PATH = 'src.candidate_bc.resume.application.commands.update_resume_content_command.UpdateResumeContentCommandHandler'
DELETE_RESUME_HANDLER_PATH = 'src.candidate_bc.resume.application.commands.delete_resume_command.DeleteResumeCommandHandler'
GET_RESUMES_BY_CANDIDATE_HANDLER_PATH = 'src.candidate_bc.resume.application.queries.get_resumes_by_candidate_query.GetResumesByCandidateQueryHandler'
GET_RESUME_BY_ID_HANDLER_PATH = 'src.candidate_bc.resume.application.queries.get_resume_by_id_query.GetResumeByIdQueryHandler'
GET_RESUME_STATISTICS_HANDLER_PATH = 'src.candidate_bc.resume.application.queries.get_resume_statistics_query.GetResumeStatisticsQueryHandler'

# PDF Analysis
from src.candidate_bc.resume.application.commands.analyze_pdf_resume_command import AnalyzePDFResumeCommandHandler


class CandidateContainer(containers.DeclarativeContainer):
    """Container para Candidate Bounded Context"""
    
    # Dependencias compartidas
    shared = providers.DependenciesContainer()
    
    # Repositories
    candidate_repository = providers.Factory(
        SQLAlchemyCandidateRepository,
        database=shared.database
    )
    
    candidate_experience_repository = providers.Factory(
        SQLAlchemyCandidateExperienceRepository,
        database=shared.database
    )
    
    candidate_education_repository = providers.Factory(
        SQLAlchemyCandidateEducationRepository,
        database=shared.database
    )
    
    candidate_project_repository = providers.Factory(
        SQLAlchemyCandidateProjectRepository,
        database=shared.database
    )
    
    candidate_application_repository = providers.Factory(
        SQLAlchemyCandidateApplicationRepository,
        database=shared.database
    )
    
    candidate_stage_repository = providers.Factory(
        CandidateApplicationStageRepository,
        session=shared.database.provided.session
    )

    application_question_answer_repository = providers.Factory(
        ApplicationQuestionAnswerRepository,
        session=shared.database.provided.session
    )

    resume_repository = providers.Factory(
        RESUME_REPOSITORY_PATH,
        database=shared.database
    )
    
    resume_generation_service = providers.Factory(
        RESUME_GENERATION_SERVICE_PATH
    )
    
    # Candidate Query Handlers
    get_candidate_by_user_id_query_handler = providers.Factory(
        GetCandidateByUserIdQueryHandler,
        candidate_repository=candidate_repository
    )
    
    get_candidate_by_id_query_handler = providers.Factory(
        GetCandidateByIdQueryHandler,
        candidate_repository=candidate_repository
    )
    
    get_candidate_by_email_query_handler = providers.Factory(
        GetCandidateByEmailQueryHandler,
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
    
    # Candidate Experience Query Handlers
    get_experiences_by_candidate_id_query_handler = providers.Factory(
        GetExperiencesByCandidateIdQueryHandler,
        experience_repository=candidate_experience_repository
    )
    
    list_candidate_experiences_by_candidate_id_query_handler = providers.Factory(
        ListCandidateExperiencesByCandidateIdQueryHandler,
        candidate_experience_repository=candidate_experience_repository
    )
    
    get_experience_by_id_query_handler = providers.Factory(
        GetExperienceByIdQueryHandler,
        experience_repository=candidate_experience_repository
    )
    
    # Candidate Education Query Handlers
    get_educations_by_candidate_id_query_handler = providers.Factory(
        GetEducationsByCandidateIdQueryHandler,
        education_repository=candidate_education_repository
    )
    
    list_candidate_educations_by_candidate_id_query_handler = providers.Factory(
        ListCandidateEducationsByCandidateIdQueryHandler,
        candidate_education_repository=candidate_education_repository
    )
    
    get_education_by_id_query_handler = providers.Factory(
        GetEducationByIdQueryHandler,
        education_repository=candidate_education_repository
    )
    
    # Candidate Project Query Handlers
    get_projects_by_candidate_id_query_handler = providers.Factory(
        GetProjectsByCandidateIdQueryHandler,
        project_repository=candidate_project_repository
    )
    
    list_candidate_projects_by_candidate_id_query_handler = providers.Factory(
        ListCandidateProjectsByCandidateIdQueryHandler,
        candidate_project_repository=candidate_project_repository
    )
    
    get_project_by_id_query_handler = providers.Factory(
        GetProjectByIdQueryHandler,
        project_repository=candidate_project_repository
    )
    
    # Candidate Command Handlers
    create_candidate_command_handler = providers.Factory(
        CreateCandidateCommandHandler,
        candidate_repository=candidate_repository,
        event_bus=shared.event_bus
    )
    
    update_candidate_basic_command_handler = providers.Factory(
        UpdateCandidateCommandHandler,
        candidate_repository=candidate_repository
    )
    
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
    
    populate_candidate_from_pdf_analysis_command_handler = providers.Factory(
        PopulateCandidateFromPdfAnalysisCommandHandler,
        candidate_repository=candidate_repository,
        command_bus=shared.command_bus
    )
    
    # Resume Command Handlers
    create_general_resume_command_handler = providers.Factory(
        CREATE_GENERAL_RESUME_HANDLER_PATH,
        resume_repository=resume_repository,
        candidate_repository=candidate_repository,
        generation_service=resume_generation_service,
        query_bus=shared.query_bus
    )
    
    update_resume_content_command_handler = providers.Factory(
        UPDATE_RESUME_CONTENT_HANDLER_PATH,
        resume_repository=resume_repository
    )
    
    delete_resume_command_handler = providers.Factory(
        DELETE_RESUME_HANDLER_PATH,
        resume_repository=resume_repository
    )
    
    # Resume Query Handlers
    get_resumes_by_candidate_query_handler = providers.Factory(
        GET_RESUMES_BY_CANDIDATE_HANDLER_PATH,
        resume_repository=resume_repository
    )
    
    get_resume_by_id_query_handler = providers.Factory(
        GET_RESUME_BY_ID_HANDLER_PATH,
        resume_repository=resume_repository
    )
    
    get_resume_statistics_query_handler = providers.Factory(
        GET_RESUME_STATISTICS_HANDLER_PATH,
        resume_repository=resume_repository
    )
    
    # PDF Analysis Command Handler
    analyze_pdf_resume_command_handler = providers.Factory(
        AnalyzePDFResumeCommandHandler,
        async_job_service=shared.async_job_service
    )
    
    # Candidate Application Command Handlers
    create_candidate_application_command_handler = providers.Factory(
        CreateCandidateApplicationCommandHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    update_application_status_command_handler = providers.Factory(
        UpdateApplicationStatusCommandHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    move_candidate_to_stage_command_handler = providers.Factory(
        MoveCandidateToStageCommandHandler,
        candidate_application_repository=candidate_application_repository,
        candidate_stage_repository=candidate_stage_repository,
        workflow_stage_repository=shared.workflow_stage_repository,
        job_position_repository=shared.job_position_repository
    )
    
    claim_task_command_handler = providers.Factory(
        ClaimTaskCommandHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    unclaim_task_command_handler = providers.Factory(
        UnclaimTaskCommandHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    # Candidate Application Query Handlers
    get_applications_by_candidate_id_query_handler = providers.Factory(
        GetApplicationsByCandidateIdQueryHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    get_my_assigned_tasks_query_handler = providers.Factory(
        GetMyAssignedTasksQueryHandler,
        candidate_application_repository=candidate_application_repository
    )
    
    # Controllers
    candidate_controller = providers.Factory(
        CandidateController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    application_controller = providers.Factory(
        ApplicationController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    onboarding_controller = providers.Factory(
        OnboardingController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    resume_controller = providers.Factory(
        ResumeController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )
    
    admin_candidate_controller = providers.Factory(
        AdminCandidateController,
        query_bus=shared.query_bus,
        command_bus=shared.command_bus
    )

    # Application Question Answer Query Handlers
    list_application_answers_query_handler = providers.Factory(
        ListApplicationAnswersQueryHandler,
        repository=application_question_answer_repository
    )

    # Application Question Answer Command Handlers
    save_application_answers_command_handler = providers.Factory(
        SaveApplicationAnswersCommandHandler,
        repository=application_question_answer_repository
    )

    evaluate_application_answers_command_handler = providers.Factory(
        EvaluateApplicationAnswersCommandHandler,
        answer_repository=application_question_answer_repository,
        application_repository=candidate_application_repository,
        question_repository=shared.application_question_repository,
        workflow_repository=shared.workflow_repository,
        job_position_repository=shared.job_position_repository
    )

    # Application Answer Controller
    application_answer_controller = providers.Factory(
        ApplicationAnswerController,
        query_bus=shared.query_bus,
        command_bus=shared.command_bus
    )

