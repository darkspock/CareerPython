"""Interview Container - Interview Management Bounded Context"""
from dependency_injector import containers, providers
from adapters.http.company_app.interview.controllers.interview_controller import InterviewController
from adapters.http.admin_app.controllers.inverview_template_controller import InterviewTemplateController

# Interview Template Infrastructure
from src.interview_bc.interview_template.infrastructure import InterviewTemplateRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository import InterviewTemplateSectionRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import InterviewTemplateQuestionRepository

# Interview Management Infrastructure
from src.interview_bc.interview.Infrastructure.repositories.interview_repository import SQLAlchemyInterviewRepository as InterviewRepository
from src.interview_bc.interview.Infrastructure.repositories.interview_answer_repository import SQLAlchemyInterviewAnswerRepository as InterviewAnswerRepository
from src.interview_bc.interview.Infrastructure.repositories.interview_interviewer_repository import SQLAlchemyInterviewInterviewerRepository as InterviewInterviewerRepository

# Interview Application Services
from src.interview_bc.interview.application.services.interview_permission_service import InterviewPermissionService

# Interview Template Application Layer - Commands
from src.interview_bc.interview_template.application.commands.create_interview_template import CreateInterviewTemplateCommandHandler
from src.interview_bc.interview_template.application import UpdateInterviewTemplateCommandHandler
from src.interview_bc.interview_template.application.commands.enable_interview_template import EnableInterviewTemplateCommandHandler
from src.interview_bc.interview_template.application.commands.disable_interview_template import DisableInterviewTemplateCommandHandler
from src.interview_bc.interview_template.application.commands.create_interview_template_section import CreateInterviewTemplateSectionCommandHandler
from src.interview_bc.interview_template.application.commands.update_interview_template_section import UpdateInterviewTemplateSectionCommandHandler
from src.interview_bc.interview_template.application.commands.enable_interview_template_section import EnableInterviewTemplateSectionCommandHandler
from src.interview_bc.interview_template.application.commands.disable_interview_template_section import DisableInterviewTemplateSectionCommandHandler
from src.interview_bc.interview_template.application.commands.delete_interview_template_section import DeleteInterviewTemplateSectionCommandHandler
from src.interview_bc.interview_template.application.commands.move_section_up import MoveSectionUpCommandHandler
from src.interview_bc.interview_template.application.commands.move_section_down import MoveSectionDownCommandHandler
from src.interview_bc.interview_template.application.commands.create_interview_template_question import CreateInterviewTemplateQuestionCommandHandler
from src.interview_bc.interview_template.application.commands.update_interview_template_question import UpdateInterviewTemplateQuestionCommandHandler
from src.interview_bc.interview_template.application.commands.enable_interview_template_question import EnableInterviewTemplateQuestionCommandHandler
from src.interview_bc.interview_template.application.commands.disable_interview_template_question import DisableInterviewTemplateQuestionCommandHandler
from src.interview_bc.interview_template.application.commands.delete_interview_template import DeleteInterviewTemplateCommandHandler

# Interview Template Application Layer - Queries
from src.interview_bc.interview_template.application.queries.list_interview_templates import ListInterviewTemplatesQueryHandler
from src.interview_bc.interview_template.application.queries.get_interview_template_by_id import GetInterviewTemplateByIdQueryHandler
from src.interview_bc.interview_template.application.queries.get_interview_template_full_by_id import GetInterviewTemplateFullByIdQueryHandler
from src.interview_bc.interview_template.application.queries.get_questions_by_section import GetQuestionsBySectionQueryHandler

# Interview Management Application Layer - Commands
from src.interview_bc.interview.application.commands.create_interview import CreateInterviewCommandHandler
from src.interview_bc.interview.application.commands.update_interview import UpdateInterviewCommandHandler
from src.interview_bc.interview.application.commands.start_interview import StartInterviewCommandHandler
from src.interview_bc.interview.application.commands.finish_interview import FinishInterviewCommandHandler
from src.interview_bc.interview.application.commands.create_interview_answer import CreateInterviewAnswerCommandHandler
from src.interview_bc.interview.application.commands.update_interview_answer import UpdateInterviewAnswerCommandHandler
from src.interview_bc.interview.application.commands.score_interview_answer import ScoreInterviewAnswerCommandHandler
from src.interview_bc.interview.application.commands.generate_interview_link import GenerateInterviewLinkCommandHandler
from src.interview_bc.interview.application.commands.submit_interview_answer_by_token import SubmitInterviewAnswerByTokenCommandHandler
from src.interview_bc.interview.application.commands.invite_interviewer import InviteInterviewerCommandHandler
from src.interview_bc.interview.application.commands.accept_interviewer_invitation import AcceptInterviewerInvitationCommandHandler

# Interview Management Application Layer - Queries
from src.interview_bc.interview.application.queries.list_interviews import ListInterviewsQueryHandler
from src.interview_bc.interview.application.queries.get_interview_by_id import GetInterviewByIdQueryHandler
from src.interview_bc.interview.application.queries.get_interviews_by_candidate import GetInterviewsByCandidateQueryHandler
from src.interview_bc.interview.application.queries.get_scheduled_interviews import GetScheduledInterviewsQueryHandler
from src.interview_bc.interview.application.queries.get_interviews_by_date_range import GetInterviewsByDateRangeQueryHandler
from src.interview_bc.interview.application.queries.get_overdue_interviews import GetOverdueInterviewsQueryHandler
from src.interview_bc.interview.application.queries.get_interview_statistics import GetInterviewStatisticsQueryHandler
from src.interview_bc.interview.application.queries.get_interview_score_summary import GetInterviewScoreSummaryQueryHandler
from src.interview_bc.interview.application.queries.get_answers_by_interview import GetAnswersByInterviewQueryHandler
from src.interview_bc.interview.application.queries.get_interview_answer_by_id import GetInterviewAnswerByIdQueryHandler
from src.interview_bc.interview.application.queries.get_pending_interviews_by_candidate_and_stage import GetPendingInterviewsByCandidateAndStageQueryHandler
from src.interview_bc.interview.application.queries.get_interview_by_token import GetInterviewByTokenQueryHandler
from src.interview_bc.interview.application.queries.get_interview_questions_by_token import GetInterviewQuestionsByTokenQueryHandler
from src.interview_bc.interview.application.queries.get_interviewers_by_interview import GetInterviewersByInterviewQueryHandler


class InterviewContainer(containers.DeclarativeContainer):
    """Container para Interview Bounded Context"""

    # Dependencias compartidas
    shared = providers.DependenciesContainer()

    # Repositories
    interview_template_repository = providers.Factory(
        InterviewTemplateRepository,
        database=shared.database
    )

    interview_template_section_repository = providers.Factory(
        InterviewTemplateSectionRepository,
        database=shared.database
    )

    interview_template_question_repository = providers.Factory(
        InterviewTemplateQuestionRepository,
        database=shared.database
    )

    interview_repository = providers.Factory(
        InterviewRepository,
        database=shared.database
    )

    interview_answer_repository = providers.Factory(
        InterviewAnswerRepository,
        database=shared.database
    )

    interview_interviewer_repository = providers.Factory(
        InterviewInterviewerRepository,
        database=shared.database
    )

    # Domain Services
    interview_permission_service = providers.Factory(
        InterviewPermissionService,
        company_user_repository=shared.company_user_repository,
        company_role_repository=shared.company_role_repository,
        job_position_repository=shared.job_position_repository
    )

    # Interview Template Query Handlers
    list_interview_templates_query_handler = providers.Factory(
        ListInterviewTemplatesQueryHandler,
        repository=interview_template_repository
    )

    get_interview_template_by_id_query_handler = providers.Factory(
        GetInterviewTemplateByIdQueryHandler,
        repository=interview_template_repository
    )

    get_interview_template_full_by_id_query_handler = providers.Factory(
        GetInterviewTemplateFullByIdQueryHandler,
        repository=interview_template_repository,
        section_repository=interview_template_section_repository,
        question_repository=interview_template_question_repository
    )

    get_questions_by_section_query_handler = providers.Factory(
        GetQuestionsBySectionQueryHandler,
        repository=interview_template_question_repository
    )

    # Interview Template Command Handlers
    create_interview_template_command_handler = providers.Factory(
        CreateInterviewTemplateCommandHandler,
        repository=interview_template_repository
    )

    update_interview_template_command_handler = providers.Factory(
        UpdateInterviewTemplateCommandHandler,
        repository=interview_template_repository
    )

    enable_interview_template_command_handler = providers.Factory(
        EnableInterviewTemplateCommandHandler,
        repository=interview_template_repository
    )

    disable_interview_template_command_handler = providers.Factory(
        DisableInterviewTemplateCommandHandler,
        repository=interview_template_repository
    )

    create_interview_template_section_command_handler = providers.Factory(
        CreateInterviewTemplateSectionCommandHandler,
        repository=interview_template_section_repository,
        template_repository=interview_template_repository
    )

    update_interview_template_section_command_handler = providers.Factory(
        UpdateInterviewTemplateSectionCommandHandler,
        repository=interview_template_section_repository
    )

    enable_interview_template_section_command_handler = providers.Factory(
        EnableInterviewTemplateSectionCommandHandler,
        repository=interview_template_section_repository
    )

    disable_interview_template_section_command_handler = providers.Factory(
        DisableInterviewTemplateSectionCommandHandler,
        repository=interview_template_section_repository
    )

    delete_interview_template_section_command_handler = providers.Factory(
        DeleteInterviewTemplateSectionCommandHandler,
        repository=interview_template_section_repository
    )

    move_section_up_command_handler = providers.Factory(
        MoveSectionUpCommandHandler,
        repository=interview_template_section_repository
    )

    move_section_down_command_handler = providers.Factory(
        MoveSectionDownCommandHandler,
        repository=interview_template_section_repository
    )

    create_interview_template_question_command_handler = providers.Factory(
        CreateInterviewTemplateQuestionCommandHandler,
        repository=interview_template_question_repository,
        section_repository=interview_template_section_repository
    )

    update_interview_template_question_command_handler = providers.Factory(
        UpdateInterviewTemplateQuestionCommandHandler,
        repository=interview_template_question_repository
    )

    enable_interview_template_question_command_handler = providers.Factory(
        EnableInterviewTemplateQuestionCommandHandler,
        repository=interview_template_question_repository
    )

    disable_interview_template_question_command_handler = providers.Factory(
        DisableInterviewTemplateQuestionCommandHandler,
        repository=interview_template_question_repository
    )

    delete_interview_template_command_handler = providers.Factory(
        DeleteInterviewTemplateCommandHandler,
        template_repository=interview_template_repository,
        section_repository=interview_template_section_repository
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

    get_interviews_by_date_range_query_handler = providers.Factory(
        GetInterviewsByDateRangeQueryHandler,
        interview_repository=interview_repository
    )

    get_overdue_interviews_query_handler = providers.Factory(
        GetOverdueInterviewsQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_statistics_query_handler = providers.Factory(
        GetInterviewStatisticsQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_score_summary_query_handler = providers.Factory(
        GetInterviewScoreSummaryQueryHandler,
        interview_repository=interview_repository,
        answer_repository=interview_answer_repository
    )

    get_answers_by_interview_query_handler = providers.Factory(
        GetAnswersByInterviewQueryHandler,
        answer_repository=interview_answer_repository
    )

    get_interview_answer_by_id_query_handler = providers.Factory(
        GetInterviewAnswerByIdQueryHandler,
        answer_repository=interview_answer_repository
    )

    get_pending_interviews_by_candidate_and_stage_query_handler = providers.Factory(
        GetPendingInterviewsByCandidateAndStageQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_by_token_query_handler = providers.Factory(
        GetInterviewByTokenQueryHandler,
        interview_repository=interview_repository
    )

    get_interview_questions_by_token_query_handler = providers.Factory(
        GetInterviewQuestionsByTokenQueryHandler,
        interview_repository=interview_repository,
        answer_repository=interview_answer_repository,
        query_bus=shared.query_bus
    )

    get_interviewers_by_interview_query_handler = providers.Factory(
        GetInterviewersByInterviewQueryHandler,
        repository=interview_interviewer_repository
    )

    # Interview Management Command Handlers
    create_interview_command_handler = providers.Factory(
        CreateInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=shared.event_bus
    )

    update_interview_command_handler = providers.Factory(
        UpdateInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=shared.event_bus
    )

    start_interview_command_handler = providers.Factory(
        StartInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=shared.event_bus
    )

    finish_interview_command_handler = providers.Factory(
        FinishInterviewCommandHandler,
        interview_repository=interview_repository,
        event_bus=shared.event_bus
    )

    create_interview_answer_command_handler = providers.Factory(
        CreateInterviewAnswerCommandHandler,
        answer_repository=interview_answer_repository,
        interview_repository=interview_repository
    )

    update_interview_answer_command_handler = providers.Factory(
        UpdateInterviewAnswerCommandHandler,
        answer_repository=interview_answer_repository
    )

    score_interview_answer_command_handler = providers.Factory(
        ScoreInterviewAnswerCommandHandler,
        answer_repository=interview_answer_repository,
        interview_repository=interview_repository
    )

    generate_interview_link_command_handler = providers.Factory(
        GenerateInterviewLinkCommandHandler,
        interview_repository=interview_repository,
        event_bus=shared.event_bus
    )

    submit_interview_answer_by_token_command_handler = providers.Factory(
        SubmitInterviewAnswerByTokenCommandHandler,
        interview_repository=interview_repository,
        answer_repository=interview_answer_repository,
        event_bus=shared.event_bus
    )

    invite_interviewer_command_handler = providers.Factory(
        InviteInterviewerCommandHandler,
        interview_repository=interview_repository,
        interviewer_repository=interview_interviewer_repository,
        event_bus=shared.event_bus
    )

    accept_interviewer_invitation_command_handler = providers.Factory(
        AcceptInterviewerInvitationCommandHandler,
        interviewer_repository=interview_interviewer_repository,
        event_bus=shared.event_bus
    )

    # Controllers
    interview_template_controller = providers.Factory(
        InterviewTemplateController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

    interview_controller = providers.Factory(
        InterviewController,
        command_bus=shared.command_bus,
        query_bus=shared.query_bus
    )

