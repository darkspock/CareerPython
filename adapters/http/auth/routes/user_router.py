from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from adapters.http.auth.controllers.user import UserController
from adapters.http.auth.schemas.token import PasswordResetResponse, PasswordResetRequest, UserExistsResponse, \
    PasswordResetConfirm
from adapters.http.auth.schemas.user import UserResponse, UserCreate, UserAutoCreateResponse, UserAutoCreateRequest, \
    UserLanguageResponse, UserLanguageUpdateResponse, UserLanguageRequest
from adapters.http.auth.services.authentication_service import get_current_user
from core.container import Container

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/", response_model=UserResponse)
@inject
def create_user(
        user_data: UserCreate,
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> UserResponse:
    """Crea un nuevo usuario"""
    return controller.create_user(user_data)


@user_router.post("/auto-create", response_model=UserAutoCreateResponse)
@inject
async def create_user_automatically(
        request: UserAutoCreateRequest,
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> UserAutoCreateResponse:
    """Create user automatically for PDF upload with random password"""
    return await controller.create_user_automatically(request)


@user_router.post("/password-reset/request", response_model=PasswordResetResponse)
@inject
async def request_password_reset(
        request: PasswordResetRequest,
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> PasswordResetResponse:
    """Request password reset for existing user"""
    return await controller.request_password_reset(request)


@user_router.post("/password-reset/confirm", response_model=PasswordResetResponse)
@inject
def reset_password(
        request: PasswordResetConfirm,
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> PasswordResetResponse:
    """Reset password using valid reset token"""
    return controller.reset_password(request)


@user_router.get("/exists", response_model=UserExistsResponse)
@inject
def check_user_exists(
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])],
        email: str = Query(..., description="Email to check")
) -> UserExistsResponse:
    """Check if user exists by email"""
    return controller.check_user_exists(email)


@user_router.get("/me/language", response_model=UserLanguageResponse)
@inject
def get_user_language(
        current_user: Annotated[UserResponse, Depends(get_current_user)],
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> UserLanguageResponse:
    """Get current user's preferred language"""
    language_code = controller.get_user_language(current_user.id)
    return UserLanguageResponse(language_code=language_code)


@user_router.put("/me/language", response_model=UserLanguageUpdateResponse)
@inject
def update_user_language(
        request: UserLanguageRequest,
        current_user: Annotated[UserResponse, Depends(get_current_user)],
        controller: Annotated[UserController, Depends(Provide[Container.user_controller])]
) -> UserLanguageUpdateResponse:
    """Update current user's preferred language"""
    result = controller.update_user_language(current_user.id, request.language_code)
    return UserLanguageUpdateResponse(**result)
