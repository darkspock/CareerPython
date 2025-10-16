"""
Global admin authentication middleware for /admin routes
"""

import json
from typing import Callable, Any
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.shared.infrastructure.middleware.admin_auth_middleware import AdminAuthMiddleware


class AdminAuthGlobalMiddleware(BaseHTTPMiddleware):
    """
    Global middleware to handle admin authentication for all /admin routes
    """

    def __init__(self, app: Any, admin_auth_middleware: AdminAuthMiddleware) -> None:
        super().__init__(app)
        self.admin_auth = admin_auth_middleware

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only apply to /admin routes
        if not request.url.path.startswith("/admin"):
            response: Response = await call_next(request)
            return response

        # Skip health check endpoint (no auth needed)
        if request.url.path == "/admin/health":
            health_response: Response = await call_next(request)
            return health_response

        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Authorization header required",
                    "type": "authentication_required"
                }
            )

        try:
            # Extract Bearer token
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authentication scheme")
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid authorization header format. Use: Bearer <token>",
                    "type": "invalid_token_format"
                }
            )

        try:
            # Validate token and get admin user
            current_admin = self.admin_auth.get_current_admin_user(token)

            # Add user to request state for access in endpoints
            request.state.current_admin = current_admin

            # Continue to the actual endpoint
            auth_response: Response = await call_next(request)
            return auth_response

        except HTTPException as e:
            # Return the specific HTTP exception from admin auth
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "type": "admin_authentication_failed"
                }
            )
        except Exception:
            # Catch any other errors
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error during authentication",
                    "type": "authentication_error"
                }
            )
