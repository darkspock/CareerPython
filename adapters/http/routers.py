# COMENTADO - Solo admin interview templates por ahora
# from presentation.candidate.routers import candidate_router
# from presentation.shared.routes.user_router import user_router
# Removed: auth_router (T011 completed)
from adapters.http.admin.routes.admin_router import router as admin_router
from adapters.http.company.routers.company_router import router as company_router
from adapters.http.company.routers.company_user_router import router as company_user_router
from adapters.http.company_candidate.routers.company_candidate_router import router as company_candidate_router
from adapters.http.company_workflow.routers.company_workflow_router import router as company_workflow_router
from adapters.http.company_workflow.routers.workflow_stage_router import router as workflow_stage_router
# from presentation.candidate.routers.home_router import home_router
# from presentation.candidate.routers import interview_router
# from presentation.candidate.routers.profile_router import router as profile_router
# from presentation.candidate.routers.landing_router import landing_router
# from presentation.candidate.routers import router as subscription_router
# from presentation.candidate.routers.resume_export_router import router as resume_export_router
# from presentation.candidate.routers import router as resume_management_router
# from presentation.candidate.routers import router as job_application_router
# from presentation.candidate.routers import router as analytics_router
# from presentation.candidate.routers import monitoring_router
# from presentation.candidate.routers import router as email_admin_router

__all__ = [
    "admin_router",
    "company_router",
    "company_user_router",
    "company_candidate_router",
    "company_workflow_router",
    "workflow_stage_router",
    # COMENTADO - Solo admin interview templates por ahora
    # "candidate_router",
    # "user_router",
    # "auth_router",
    # "home_router",
    # "interview_router",
    # "profile_router",
    # "landing_router",
    # "subscription_router",
    # "resume_export_router",
    # "resume_management_router",
    # "job_application_router",
    # "analytics_router",
    # "monitoring_router",
    # "email_admin_router"
]
