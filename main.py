"""
FastAPI app minimal - Solo admin interview templates
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Solo imports esenciales
from core.container import Container

# Initialize Dramatiq broker for web service
from adapters.http.admin.routes.admin_router import router as admin_router
from adapters.http.candidate.routers.landing_router import router as landing_router
from adapters.http.candidate.routers.candidate_router import candidate_router
from adapters.http.candidate.routers.resume_router import router as resume_router
from adapters.http.candidate.routers.file_router import file_router
from adapters.http.candidate.routers.job_router import job_router
from adapters.http.company.routers.company_router import router as company_router
from adapters.http.company.routers.company_user_router import router as company_user_router
from adapters.http.company.routers.company_role_router import router as company_role_router
from adapters.http.company.routers.company_candidate_application_router import router as company_candidate_application_router
from adapters.http.company.routers.enum_router import router as company_enum_router
from adapters.http.company.routers.task_router import router as task_router
from adapters.http.company.routers.email_template_router import router as email_template_router
from src.talent_pool.presentation.routers.talent_pool_router import router as talent_pool_router
from src.workflow_analytics.presentation.routers.workflow_analytics_router import router as workflow_analytics_router
from adapters.http.company_candidate.routers.company_candidate_router import router as company_candidate_router
from adapters.http.company_workflow.routers.company_workflow_router import router as company_workflow_router
from adapters.http.company_workflow.routers.workflow_stage_router import router as workflow_stage_router
from adapters.http.company_workflow.routers.custom_field_router import router as custom_field_router
from src.field_validation.presentation.routers.validation_rule_router import router as validation_rule_router
from src.position_stage_assignment.presentation.routers import router as position_stage_assignment_router
from adapters.http.shared.routes.user_router import user_router
from adapters.http.shared.routes.ai_test_router import router as ai_test_router
# Phase 10: Public Position Router
from src.job_position.presentation.routers.public_position_router import router as public_position_router
# Phase 12: Phase Router
from src.phase.presentation.routers.phase_router import router as phase_router

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
app.include_router(company_workflow_router)  # Company workflow management
app.include_router(workflow_stage_router)  # Workflow stage management
app.include_router(custom_field_router)  # Custom field management
app.include_router(validation_rule_router)  # Field validation rules
app.include_router(position_stage_assignment_router)  # Position stage assignment management
app.include_router(phase_router)  # Phase 12: Phase management
app.include_router(candidate_router)
app.include_router(user_router)
app.include_router(ai_test_router)  # Direct AI testing

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
    "adapters.http.admin.routes.admin_router",
    "adapters.http.candidate.routers.landing_router",
    "adapters.http.candidate.routers.candidate_router",
    "adapters.http.candidate.routers.resume_router",
    "adapters.http.candidate.routers.file_router",
    "adapters.http.candidate.routers.job_router",
    "adapters.http.company.routers.company_router",
    "adapters.http.company.routers.company_user_router",
    "adapters.http.company.routers.company_role_router",
    "adapters.http.company.routers.company_candidate_application_router",
    "adapters.http.company_candidate.routers.company_candidate_router",
    "adapters.http.company_workflow.routers.company_workflow_router",
    "adapters.http.company_workflow.routers.workflow_stage_router",
    "adapters.http.company_workflow.routers.custom_field_router",
    "src.field_validation.presentation.routers.validation_rule_router",
    "src.position_stage_assignment.presentation.routers.position_stage_assignment_router",
    "src.workflow_analytics.presentation.routers.workflow_analytics_router",
    "src.job_position.presentation.routers.public_position_router",  # Phase 10: Public position endpoints
    "src.phase.presentation.routers.phase_router",  # Phase 12: Phase management
    "adapters.http.shared.routes.user_router",
])