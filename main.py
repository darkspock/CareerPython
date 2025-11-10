"""
FastAPI app minimal - Solo admin interview templates
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from adapters.http.candidate_app.routers.position_stage_assignment_router import router as position_stage_assignment_router
from adapters.http.candidate_app.routers.file_attachment_router import router as file_attachment_router
from adapters.http.company_app.job_position.routers.public_position_router import router as public_position_router
from adapters.http.shared.field_validation.routers.validation_rule_router import router as validation_rule_router
# Solo imports esenciales
from core.container import Container

# Initialize Dramatiq broker for web service
from adapters.http.admin_app.routes.admin_router import router as admin_router
from adapters.http.candidate_app.routers.landing_router import router as landing_router
from adapters.http.candidate_app.routers.candidate_router import candidate_router
from adapters.http.candidate_app.routers.resume_router import router as resume_router
from adapters.http.candidate_app.routers.file_router import file_router
from adapters.http.candidate_app.routers.job_router import job_router
from adapters.http.company_app.company.routers.company_router import router as company_router
from adapters.http.company_app.company.routers.company_registration_router import router as company_registration_router, users_router as users_public_router
from adapters.http.company_app.company.routers.company_user_router import router as company_user_router
from adapters.http.company_app.company.routers.company_role_router import router as company_role_router
from adapters.http.company_app.company.routers.company_candidate_application_router import router as company_candidate_application_router
from adapters.http.company_app.company.routers.enum_router import router as company_enum_router
from adapters.http.company_app.company.routers.task_router import router as task_router
from adapters.http.company_app.company.routers.email_template_router import router as email_template_router
from adapters.http.company_app.talent_pool.routers.talent_pool_router import router as talent_pool_router
from adapters.http.shared.workflow_analytics.routers.workflow_analytics_router import router as workflow_analytics_router
from adapters.http.company_app.company_candidate.routers.company_candidate_router import router as company_candidate_router
from adapters.http.shared.workflow.routers.workflow_router import router as candidate_application_workflow_router
from adapters.http.shared.workflow.routers.workflow_stage_router import router as workflow_stage_router
from adapters.http.shared.customization.routers.entity_customization_router import router as entity_customization_router
from adapters.http.company_app.company.routers.candidate_comment_router import router as candidate_comment_router
from adapters.http.company_app.company.routers.job_position_comment_router import router as job_position_comment_router
from adapters.http.company_app.company.routers.candidate_review_router import router as candidate_review_router
from adapters.http.company_app.company_page.routers.company_page_router import router as company_page_router
from adapters.http.company_app.company_page.routers.public_company_page_router import router as public_company_page_router
from adapters.http.auth.routes.user_router import user_router
from adapters.http.auth.routes.ai_test_router import router as ai_test_router
from adapters.http.auth.invitations.routers.invitation_router import router as invitation_router
# Phase 10: Public Position Router
# Phase 12: Phase Router
from adapters.http.shared.phase.routers.phase_router import router as phase_router

# Crear tablas - COMENTADO temporalmente para aislamiento
# Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI mínima
app = FastAPI(
    title="Admin Panel - Interview Templates",
    description="Panel de administración mínimo - Solo plantillas de entrevista",
    version="1.0.0-minimal"
)

# Configurar CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Vite alternative port
        "http://localhost:5175"   # Vite alternative port 2
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)

# Incluir routers esenciales
# IMPORTANT: Resume router must be registered BEFORE candidate router
# to prevent the generic /{candidate_id} route from catching /resume paths
app.include_router(admin_router)
app.include_router(landing_router)
app.include_router(public_position_router)  # Phase 10: Public job board (no auth required)
app.include_router(resume_router)  # Register resume router first
app.include_router(file_router)  # File operations (PDF analysis)
app.include_router(job_router)  # Job status polling for frontend
app.include_router(company_registration_router)  # Public company registration (no auth)
app.include_router(users_public_router)  # Public users endpoints (check-email)
app.include_router(company_router)  # Company management
app.include_router(company_user_router)  # Company user management
app.include_router(company_role_router)  # Company role management
app.include_router(company_candidate_application_router)  # Company candidate application management
app.include_router(company_enum_router)  # Company enums
app.include_router(task_router)  # Phase 6: Task Management
app.include_router(email_template_router)  # Phase 7: Email Template Management
app.include_router(talent_pool_router)  # Phase 8: Talent Pool Management
app.include_router(workflow_analytics_router)  # Phase 9: Workflow Analytics
app.include_router(company_candidate_router)  # Company candidate management
app.include_router(candidate_application_workflow_router)  # Company workflow management
app.include_router(workflow_stage_router)  # Workflow stage management
app.include_router(entity_customization_router)  # Entity customization management
app.include_router(candidate_comment_router)  # Candidate comment management
app.include_router(candidate_review_router)  # Candidate review management
app.include_router(job_position_comment_router)  # Job position comment management
app.include_router(validation_rule_router)  # Field validation rules
app.include_router(position_stage_assignment_router)  # Position stage assignment management
app.include_router(company_page_router)  # Company pages management
app.include_router(public_company_page_router)  # Public company pages
app.include_router(file_attachment_router)  # File attachment management
app.include_router(phase_router)  # Phase 12: Phase management
app.include_router(candidate_router)
app.include_router(user_router)
app.include_router(invitation_router)  # Public invitation endpoints
app.include_router(ai_test_router)  # Direct AI testing

# Mount static files for uploads (local storage)
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Root endpoint básico
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Admin Panel - Interview Templates Only",
        "version": "1.0.0-minimal",
        "docs": "/docs",
        "admin": "/admin"
    }

# Health check básico
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "admin-interview-templates"}

# CORS test endpoint
@app.get("/cors-test", tags=["test"])
async def cors_test():
    return {"message": "CORS is working!", "timestamp": "2025-10-10"}

# Configurar el contenedor mínimo
container = Container()
app.container = container

# Wire solo el admin router y onboarding
container.wire(modules=[
    "adapters.http.admin_app.routes.admin_router",
    "adapters.http.candidate_app.routers.landing_router",
    "adapters.http.candidate_app.routers.candidate_router",
    "adapters.http.candidate_app.routers.resume_router",
    "adapters.http.candidate_app.routers.file_router",
    "adapters.http.candidate_app.routers.job_router",
    "adapters.http.company_app.company.routers.company_registration_router",  # Public registration (includes users_router)
    "adapters.http.company_app.company.routers.company_router",
    "adapters.http.company_app.company.routers.company_user_router",
    "adapters.http.company_app.company.routers.company_role_router",
    "adapters.http.company_app.company.routers.company_candidate_application_router",
    "adapters.http.company_app.company_candidate.routers.company_candidate_router",
    "adapters.http.company_app.talent_pool.routers.talent_pool_router",
    "adapters.http.shared.workflow.routers.workflow_router",
    "adapters.http.shared.workflow.routers.workflow_stage_router",
    "adapters.http.shared.customization.routers.entity_customization_router",
    "adapters.http.company_app.company.routers.candidate_comment_router",
    "adapters.http.company_app.company.routers.candidate_review_router",
    "adapters.http.company_app.company.routers.job_position_comment_router",
    "adapters.http.shared.field_validation.routers.validation_rule_router",
    "adapters.http.candidate_app.routers.position_stage_assignment_router",
    "adapters.http.shared.workflow_analytics.routers.workflow_analytics_router",
    "adapters.http.company_app.job_position.routers.public_position_router",  # Phase 10: Public position endpoints
    "adapters.http.shared.phase.routers.phase_router",  # Phase 12: Phase management
    "adapters.http.company_app.company_page.routers.company_page_router",  # Company Pages management
    "adapters.http.company_app.company_page.routers.public_company_page_router",  # Public Company Pages
    "adapters.http.candidate_app.routers.file_attachment_router",  # File attachment management
    "adapters.http.auth.routes.user_router",
    "adapters.http.auth.invitations.routers.invitation_router",
])