"""
Dependency to get current admin user from request state
"""

from typing import Optional

from fastapi import Request, HTTPException, status

from adapters.http.auth.schemas.user import UserResponse


def get_current_admin_from_state(request: Request) -> UserResponse:
    """
    Get current admin user from request state (set by AdminAuthGlobalMiddleware)

    Args:
        request: FastAPI request object

    Returns:
        UserResponse: Current authenticated admin user

    Raises:
        HTTPException: If user is not found in state (shouldn't happen if middleware works)
    """
    current_admin: Optional[UserResponse] = getattr(request.state, 'current_admin', None)

    if not current_admin:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin user not found in request state. Middleware may not be configured correctly."
        )

    return current_admin


def get_current_admin_user() -> UserResponse:
    """
    This is a placeholder. The actual implementation will need to be handled
    differently since we're using middleware now.
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="This function should not be called directly when using middleware"
    )
