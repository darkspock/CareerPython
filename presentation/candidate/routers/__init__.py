# SIMPLIFIED - Only import what we need for now
# from .candidate_router import candidate_router
# from presentation.shared.routes.user_router import user_router
# from presentation.shared.routes.auth_router import auth_router
# from .home_router import home_router
# from .interview_router import interview_router
# from .profile_router import router as profile_router
from .landing_router import router as landing_router
# from .ai_enhancement_router import router as ai_enhancement_router
# from .pdf_processing_router import router as pdf_processing_router
# from .resume_preview_export_router import router as resume_preview_export_router
# from presentation.admin.routes.admin_router import router as admin_router

__all__ = ["landing_router"]
