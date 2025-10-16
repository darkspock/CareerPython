from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
def read_root() -> dict[str, str]:
    """Endpoint raíz"""
    return {
        "message": "CareerPython API - SOLID Architecture",
        "version": "2.0.0",
        "architecture": "SOLID Principles"
    }


@home_router.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "architecture": "SOLID"}
