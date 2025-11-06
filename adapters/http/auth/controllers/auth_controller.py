from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from adapters.http.auth.schemas.auth_response import LoginResponse
from src.user.application.queries.authenticate_user_query import AuthenticateUserQuery, AuthenticateUserQueryHandler


class AuthController:
    """Controller for authentication endpoints following DDD pattern"""

    def __init__(self, authenticate_user_handler: AuthenticateUserQueryHandler):
        self.authenticate_user_handler = authenticate_user_handler

    def login(self, form_data: OAuth2PasswordRequestForm) -> LoginResponse:
        """
        Login endpoint that follows DDD pattern:
        Controller -> Query Handler -> DTO -> Response Schema
        """
        # Create query
        query = AuthenticateUserQuery(
            email=form_data.username,  # OAuth2 uses 'username' field for email
            password=form_data.password
        )

        # Execute query through handler
        authenticated_user_dto = self.authenticate_user_handler.handle(query)

        # Check if authentication failed
        if not authenticated_user_dto:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert DTO to Response schema
        return LoginResponse.from_dto(authenticated_user_dto)
