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
from adapters.http.shared.routes.user_router import user_router
from adapters.http.shared.routes.ai_test_router import router as ai_test_router

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
app.include_router(resume_router)  # Register resume router first
app.include_router(file_router)  # File operations (PDF analysis)
app.include_router(job_router)  # Job status polling for frontend
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
    "adapters.http.shared.routes.user_router",
])